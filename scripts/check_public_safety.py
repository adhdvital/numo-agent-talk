#!/usr/bin/env python3
"""Gate for a public skill repo: refuse to publish text that leaks or injects.

Installed at scripts/check_public_safety.py. Run it before any publish and in the public repo CI.

Usage:
    python3 check_public_safety.py skills/numo-agent-talk README.md .github
    python3 check_public_safety.py --ci skills/numo-agent-talk README.md
    python3 check_public_safety.py --style skills/numo-agent-talk
    python3 check_public_safety.py --self-test

Targets are explicit. There is no default target set: a pipeline that forgets
the list gets an error, not a green run over the wrong tree.

Exit codes: 0 clean, 1 findings, 2 usage error.

Full run prints  file:line:col  rule  evidence.
CI run (--ci) prints  file:line  rule  and never the text of the finding, so a
private name never lands in a public log.

Third party names come only from the file named by SKILL_DENY_NAMES. The list
itself stays private and is never committed.
"""

import argparse
import os
import re
import sys
import unicodedata
from pathlib import Path

TEXT_SUFFIXES = {".md", ".markdown", ".txt", ".json", ".yml", ".yaml", ".py", ".sh", ".toml"}

# Addresses and hosts that are documentation placeholders, not real contacts.
ALLOW_EMAILS = {"security@example.com", "noreply@example.com", "you@example.com"}
ALLOW_SUBSTR = ("example.com", "example.org", "example.net", "your-name", "user@host")

# Base rules. Every rule names the banned shape; the right shape sits in the comment.
BASE_RULES = [
    # Secrets. Right way: a placeholder like <API_KEY> or a pointer to a vault item by name.
    ("secret-vault-ref", re.compile(r"\bop://")),
    ("secret-openai", re.compile(r"\bs" + r"k-[A-Za-z0-9_-]{16,}")),
    ("secret-github", re.compile(r"\b(?:ghp|gho|ghu|ghs|ghr)_[A-Za-z0-9]{20,}|\bgithub_pat_[A-Za-z0-9_]{20,}")),
    ("secret-slack", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}")),
    ("secret-bearer", re.compile(r"(?i)\bBear" + r"er\s+[A-Za-z0-9._~+/=-]{12,}")),
    ("secret-aws", re.compile(r"\b(?:AKIA|ASIA)[0-9A-Z]{16}\b")),
    ("secret-google", re.compile(r"\bAIza[0-9A-Za-z_-]{35}\b")),
    ("secret-jwt", re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}")),
    ("secret-pem", re.compile(r"-----BE" + r"GIN [A-Z ]*PRIVATE KEY-----")),
    ("secret-assign", re.compile(
        r"(?i)\b(?:api[_-]?key|access[_-]?token|auth[_-]?token|client[_-]?secret|password|passwd)\b"
        r"\s*[:=]\s*(?:['\"][^'\"\s]{8,}|[^\s'\"<][^\s'\"]{7,})")),
    # Private paths. Right way: ~/path or <home>/path.
    ("private-path", re.compile(r"/Users/(?!<)[A-Za-z0-9._-]+|/home/(?!<)[A-Za-z0-9._-]+|C:\\Users\\[A-Za-z0-9._-]+")),
    # Contacts. Right way: example.com addresses, no phone numbers at all.
    ("email", re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")),
    ("phone", re.compile(r"(?<![\w/.-])\+\d{1,3}[\s().-]?\d{2,4}[\s().-]?\d{2,4}[\s().-]?\d{2,4}(?![\w-])")),
    # Internal infrastructure. Right way: describe the tool by kind, not by link.
    ("internal-url", re.compile(
        r"(?i)\b(?:linear\.app/|notion\.so/|docs\.google\.com/|drive\.google\.com/|app\.slack\.com/"
        r"|\blocalhost\b|127\.0\.0\.1|192\.168\.\d+\.\d+|10\.\d+\.\d+\.\d+"
        r"|[A-Za-z0-9.-]+\.(?:internal|local|lan|corp|intranet)\b"
        r"|numo-ai-hub)")),
    # Agent privileges. Right way: the skill asks, the human approves.
    ("privilege-escalation", re.compile(
        r"(?i)dangerously-skip-permissions|--yolo\b|bypassPermissions|skip (?:the )?(?:permission|confirmation)"
        r"|disable (?:the )?(?:sandbox|permission)|add to .{0,20}allow.?list|autoApprove")),
    # Sending from a drafting skill. Right way: show a draft, wait for a yes.
    ("agency-send", re.compile(
        r"(?i)\b(?:send the (?:email|message)|post it to|publish (?:it|the post)|git push|gh pr create)\b")),
    # Smuggled instructions. Right way: plain visible text.
    ("hidden-char", re.compile(
        r"[\u00ad\u200b-\u200f\u2060-\u2064\u206a-\u206f\ufeff\u202a-\u202e\u2066-\u2069"
        r"\ufe00-\ufe0f\U000e0000-\U000e007f]")),
    ("html-comment", re.compile(r"<!--")),
]

# Style shapes, checked only with --style. The style gate proper is check_style.py.
STYLE_RULES = [
    ("long-dash", re.compile(r"[\u2014\u2013\u2015\u2212]")),
]


def load_name_denylist():
    """Third party names, only from SKILL_DENY_NAMES. No names live in this file."""
    path = os.environ.get("SKILL_DENY_NAMES")
    if not path:
        return None
    p = Path(path)
    if not p.exists():
        raise SystemExit(f"SKILL_DENY_NAMES points at a missing file: {path}")
    words = [w.strip() for w in p.read_text(encoding="utf-8").splitlines()
             if w.strip() and not w.lstrip().startswith("#")]
    if not words:
        return None
    return re.compile("|".join(re.escape(w) for w in sorted(words, key=len, reverse=True)), re.IGNORECASE)


def evidence_for(rule, hit):
    if rule == "third-party-name":
        return "[redacted]"
    if rule == "hidden-char":
        ch = hit[0]
        return "U+%04X %s" % (ord(ch), unicodedata.name(ch, "unnamed"))
    return hit[:60]


def scan_text(text, label, rules, names=None):
    """Scan one blob. Returns a list of (label, line, col, rule, evidence)."""
    findings = []
    for lineno, line in enumerate(text.splitlines(), 1):
        for rule, rx in rules:
            for m in rx.finditer(line):
                hit = m.group(0)
                if rule == "email":
                    low = hit.lower()
                    if low in ALLOW_EMAILS or any(a in low for a in ALLOW_SUBSTR):
                        continue
                findings.append((label, lineno, m.start() + 1, rule, evidence_for(rule, hit)))
        if names:
            for m in names.finditer(line):
                findings.append((label, lineno, m.start() + 1, "third-party-name", "[redacted]"))
    return findings


SKIP_DIRS = {".git", "node_modules", "__pycache__", ".venv"}


def iter_files(targets):
    """Every regular file under every target. Binaries are reported, never skipped in silence."""
    for t in targets:
        p = Path(t)
        if p.is_dir():
            for f in sorted(p.rglob("*")):
                if not f.is_file():
                    continue
                if SKIP_DIRS.intersection(f.parts):
                    continue
                yield f
        elif p.is_file():
            yield p
        else:
            raise SystemExit(f"target does not exist: {t}")


def scan_targets(targets, rules, names):
    """Returns (findings, scanned_count). A caller that prints one without the other lies about coverage."""
    findings = []
    scanned = 0
    for f in iter_files(targets):
        scanned += 1
        try:
            text = f.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            findings.append((str(f), 0, 0, "binary-file", "not valid UTF-8 text"))
            continue
        findings.extend(scan_text(text, str(f), rules, names))
    return findings, scanned


CLEAN_SAMPLE = """---
name: numo-agent-talk
description: Writes in one human voice.
---

# Voice

Read the local file if the workspace has one, otherwise use the base rules.
Write to security@example.com when you find a leak.
Paths look like ~/notes/voice.md, never a home directory of one person.
"""

# Fake credentials below are assembled at runtime so this file itself never
# contains a literal that a secret scanner would flag.
DIRTY_SAMPLE = """Key: op://Claude MCP/thing/credential
token {sk}
github {gh}
slack {xo}
header Authorization: {be}
aws {aws}
google {goog}
jwt {jwt}
pem {pem}
unquoted {plain}
tag block here: a{tag}b
path /Users/someone/Documents/notes.md
mail person@company.com
phone +380 67 123 4567
board https://linear.app/team/issue/ABC-1
run claude --dangerously-skip-permissions
then send the email yourself
zero width here: a\u200bb
<!-- hidden note -->
""".format(
    sk="s" + "k-abcdefghijklmnopqrstuvwxyz012345",
    gh="gh" + "p_abcdefghijklmnopqrstuvwxyz0123456789",
    xo="xo" + "xb-1234567890-abcdefghij",
    be="Bear" + "er abcdefghijklmnopqrstuvwxyz",
    aws="AK" + "IAQWERTYUIOPASDFGH",
    goog="AIz" + "aSyA12345678901234567890123456789012",
    jwt="ey" + "JhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abcdefghijklmnop",
    pem="-----BE" + "GIN RSA PRIVATE KEY-----",
    plain="api_key=Zq7Lm2Rt9Vx4Kw8P",
    tag="\U000e0041",
)

DIRTY_STYLE_SAMPLE = "text with a long dash \u2014 and a short one \u2013 inside\n"


def self_test():
    """Two blobs in memory: one clean, one dirty. Prints a verdict, returns exit code."""
    ok = True
    clean = scan_text(CLEAN_SAMPLE, "<clean>", BASE_RULES, None)
    if clean:
        ok = False
        print("self-test FAIL: clean sample produced findings")
        for label, ln, col, rule, ev in clean:
            print(f"  {label}:{ln}:{col}  {rule}  {ev}")
    else:
        print("self-test: clean sample, 0 findings, ok")

    dirty = scan_text(DIRTY_SAMPLE, "<dirty>", BASE_RULES, None)
    got = {rule for _, _, _, rule, _ in dirty}
    want = {
        "secret-vault-ref", "secret-openai", "secret-github", "secret-slack", "secret-bearer",
        "secret-aws", "secret-google", "secret-jwt", "secret-pem", "secret-assign",
        "private-path", "email", "phone", "internal-url", "privilege-escalation",
        "agency-send", "hidden-char", "html-comment",
    }
    missing = sorted(want - got)
    if missing:
        ok = False
        print("self-test FAIL: dirty sample missed rules: " + ", ".join(missing))
    else:
        print(f"self-test: dirty sample, {len(dirty)} findings, all {len(want)} expected rules fired, ok")

    style = scan_text(DIRTY_STYLE_SAMPLE, "<dirty-style>", STYLE_RULES, None)
    if len(style) != 2:
        ok = False
        print(f"self-test FAIL: style sample gave {len(style)} findings, wanted 2")
    else:
        print("self-test: style sample, 2 dash findings, ok")

    names_file = Path(os.environ.get("TMPDIR", "/tmp")) / "check_public_safety_selftest_names.txt"
    names_file.write_text("Bilbo Baggins\n# comment\n", encoding="utf-8")
    prev = os.environ.get("SKILL_DENY_NAMES")
    os.environ["SKILL_DENY_NAMES"] = str(names_file)
    try:
        names = load_name_denylist()
        hits = scan_text("A note about Bilbo Baggins here.\n", "<names>", [], names)
        if len(hits) != 1 or hits[0][4] != "[redacted]":
            ok = False
            print("self-test FAIL: denylist did not fire, or leaked the name")
        else:
            print("self-test: denylist fired once, evidence redacted, ok")
    finally:
        if prev is None:
            os.environ.pop("SKILL_DENY_NAMES", None)
        else:
            os.environ["SKILL_DENY_NAMES"] = prev
        names_file.unlink(missing_ok=True)

    print("SELF-TEST OK" if ok else "SELF-TEST FAILED")
    return 0 if ok else 1


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="check_public_safety.py",
        description="Public safety gate: secrets, private paths, contacts, internal links, injection.",
        add_help=True,
    )
    parser.add_argument("targets", nargs="*", help="explicit files and folders to scan")
    parser.add_argument("--ci", action="store_true",
                        help="print file, line and rule name without the text of the finding")
    parser.add_argument("--style", action="store_true",
                        help="also check the long and the short dash")
    parser.add_argument("--no-names", action="store_true", dest="no_names",
                        help="scan without the third party name list, and say so")
    parser.add_argument("--self-test", action="store_true", dest="self_test",
                        help="run the built in samples and exit")
    args = parser.parse_args(argv)

    if args.self_test:
        return self_test()

    if not args.targets:
        parser.print_usage(sys.stderr)
        print(
            "error: name the targets. There is no default set.\n"
            "  example: python3 check_public_safety.py skills/numo-agent-talk README.md .github",
            file=sys.stderr,
        )
        return 2

    rules = BASE_RULES + (STYLE_RULES if args.style else [])

    # The name list runs in every mode. --ci changes only what is printed, never what is checked:
    # evidence for this rule is the literal [redacted], so a name cannot reach a public log either way.
    try:
        names = load_name_denylist()
    except SystemExit as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    if names is None:
        if not args.no_names:
            print(
                "error: SKILL_DENY_NAMES is not set or is empty, so third party names are unchecked.\n"
                "  set it to a file with one name per line, or pass --no-names to accept that gap.",
                file=sys.stderr,
            )
            return 2
        print("note: scanning without the third party name list (--no-names)", file=sys.stderr)

    findings, scanned = scan_targets(args.targets, rules, names)
    for label, ln, col, rule, ev in findings:
        if args.ci:
            print(f"{label}:{ln}  {rule}")
        else:
            print(f"{label}:{ln}:{col}  {rule}  {ev}")
    print(f"{len(findings)} finding(s) in {scanned} file(s)")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
