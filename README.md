# numo-agent-talk

A skill that teaches your agent to write like a person: short, clear, and from an equal footing. Chat replies, posts,
emails, messages.

Українська версія нижче.

## Before and after

**A reply in chat.**

> Before. So, to summarize: I have analyzed the situation and it seems I can say the problem is probably in the
> configuration. This is a fairly common situation that often arises in similar cases. Overall, I would recommend, if
> possible, checking the settings, though the final decision is of course yours.

> After. The deploy failed: the config still points at the old domain. Fixing it and restarting, three minutes.
> If the domain changed on purpose, say so and I will update the rest of the links.

**A message to a friend.**

> Before. Hi! Sorry to bother you, and sorry for writing so late. I just wanted to ask whether you might possibly have
> a free minute, if that is convenient for you at all, to look at my text. Thanks so much in advance!

> After. Hey. Can you read my text by Thursday? One thing interests me: whether the first half makes sense.
> If you cannot, say so and I will ask someone else.

**A follow-up to a client.**

> Before. Good afternoon! Sorry to disturb you. I just wanted to check whether you have had a chance to look at the
> integration proposal we sent last week. We understand you are very busy, so thank you in advance for any feedback,
> it is extremely valuable to us.

> After. Resending the integration proposal. Review the timeline section by Friday and tell me what does not work.
> If it looks fine, we start Monday.

## Install

**Claude Code.** Two commands in the chat, not in your terminal:

```
/plugin marketplace add adhdvital/numo-agent-talk
/plugin install numo-agent-talk@numo-agent-talk
```

**Codex and Cursor.** Clone this repo and copy one folder:

```bash
git clone https://github.com/adhdvital/numo-agent-talk.git
cp -R numo-agent-talk/skills/numo-agent-talk ~/.agents/skills/
```

Put it in `~/.agents/skills/` to use it everywhere, or in your project's `.agents/skills/` to keep it to one project.

## How to use it

Ask in plain words: rewrite this, it sounds like AI slop. Shorten this email. Draft a post about the launch. Check this
text and tell me what is wrong. The skill picks the mode itself and stops before anything is sent, because a human
sends.

## What it changes

Ten rules run on every text. The first sentence carries the point, because everything before it gets lost. A short
answer lives in four lines. Status comes from the absence of apologies, so no "sorry to bother you", no "just", no
hedging in front of your own opinion. Numbers stay exact, because a rounded fact reads as a lie. Every claim carries a
source or an honest "from memory". The full set, with the reasoning behind each rule, is in
[SKILL.md](skills/numo-agent-talk/SKILL.md).

## Why a skill and not a prompt

A prompt lives for one session and dies. A skill triggers itself on the right words, keeps the rules in one place,
reads your personal style file, and stops before sending. Rules that explain why are followed more reliably than a list
of bans, and a pair of before-and-after examples beats any instruction.

## Make it sound like you

Ask the agent to set it up. It writes a local `.writing-local.md` with your tone, your languages, your channels, and
your own before-and-after pairs. Without that file the skill still works on full defaults; the file only adds your
voice on top. It is personal, so it stays in `.gitignore`.

## Sources

The method stands on 25 books about writing and status. The core six: The Elements of Style (Strunk, White), Smart
Brevity (VandeHei, Allen, Schwartz), Never Split the Difference (Voss), Pitch Anything (Klaff), Impro (Johnstone), and
"Пиши, сокращай" (Ilyahov, Sarycheva). The full canon, with the key rules of each book, is in
[references/library.md](skills/numo-agent-talk/references/library.md).

## License and security

MIT for the skill and its structure. The rule texts are additionally available under CC BY 4.0 if you need attribution.
Vulnerabilities go to [SECURITY.md](SECURITY.md), contributions to [CONTRIBUTING.md](CONTRIBUTING.md).

---

# numo-agent-talk

Скіл, який вчить твого агента писати по-людськи: коротко, ясно і з позиції рівного. Чат, пости, листи, повідомлення.

## Було і стало

**Відповідь у чаті.**

> Було. Отже, підсумовуючи: варто зазначити, що я проаналізував ситуацію і, здається, можу сказати, що проблема,
> ймовірно, полягає в конфігурації. Це досить поширена ситуація, яка часто виникає в подібних випадках. Загалом,
> я б рекомендував, якщо це можливо, перевірити налаштування, хоча остаточне рішення, звісно, за вами.

> Стало. Впав деплой: у конфігу стоїть старий домен. Правлю і перезапускаю, це три хвилини.
> Якщо домен змінили навмисно, скажи, і я підлаштую решту посилань.

**Повідомлення другу.**

> Було. Привіт! Вибач, що турбую, і вибач, що так пізно пишу. Просто хотів дізнатись, чи не міг би ти, якщо в тебе
> раптом буде вільна хвилинка і якщо тобі це взагалі зручно, глянути мій текст. Заздалегідь дуже дякую!

> Стало. Привіт. Глянеш мій текст до четверга? Цікавить одне: чи зрозуміла перша половина.
> Не встигаєш, скажи, віддам іншому.

**Нагадування клієнту.**

> Було. Доброго дня! Вибачте, що турбую. Просто хотів поцікавитись, чи не могли б ви, якщо буде можливість,
> подивитись нашу пропозицію по інтеграції, яку ми надсилали минулого тижня. Ми розуміємо, що ви дуже зайняті,
> тому заздалегідь дякуємо за будь-який фідбек, він для нас надзвичайно важливий.

> Стало. Надсилаю пропозицію по інтеграції ще раз. Подивіться розділ про строки до пʼятниці і напишіть, що не
> влаштовує. Якщо все гаразд, стартуємо з понеділка.

## Установка

**Claude Code.** Дві команди в чаті, не в терміналі:

```
/plugin marketplace add adhdvital/numo-agent-talk
/plugin install numo-agent-talk@numo-agent-talk
```

**Codex і Cursor.** Клонуй репо і скопіюй одну теку:

```bash
git clone https://github.com/adhdvital/numo-agent-talk.git
cp -R numo-agent-talk/skills/numo-agent-talk ~/.agents/skills/
```

Тека `~/.agents/skills/` вмикає скіл у всіх проєктах, `.agents/skills/` усередині проєкту тільки в ньому.

## Як користуватись

Проси звичайними словами: перепиши це, звучить як слоп. Скороти лист. Напиши пост про реліз. Перевір текст і скажи, що
не так. Скіл сам обирає режим і зупиняється перед надсиланням, бо надсилає людина.

## Що змінюється

На кожному тексті працюють десять правил. Перше речення несе суть, бо все, що стоїть до неї, читач губить. Коротка
відповідь живе в чотирьох рядках. Статус читається з відсутності виправдань, тому геть «вибачте, що турбую», геть
«просто», геть сумнів перед власною думкою. Числа лишаються точними, бо заокруглений факт читається як брехня. Кожне
твердження несе джерело або чесне «з памʼяті». Повний набір із поясненням до кожного правила лежить у
[SKILL.md](skills/numo-agent-talk/SKILL.md).

## Чому скіл, а не промпт

Промпт живе одну сесію і вмирає. Скіл вмикається сам на потрібних словах, тримає правила в одному місці, читає твій
особистий файл стилю і зупиняється перед надсиланням. Правило з поясненням «чому» агент виконує стабільніше за список
заборон, а пара «було і стало» працює краще за будь-яку інструкцію.

## Щоб звучало як ти

Попроси агента налаштувати. Він створить локальний файл `.writing-local.md` з твоїм тоном, мовами, каналами і твоїми
парами «було і стало». Без файла скіл працює на повних дефолтах, файл лише додає твій голос зверху. Він особистий,
тому лишається в `.gitignore`.

## Джерела

Метод стоїть на 25 книгах про письмо і статус. Ядро з шести: «Пиши, скорочуй» (Ільяхов, Саричева), The Elements of
Style (Strunk, White), Smart Brevity (VandeHei, Allen, Schwartz), Never Split the Difference (Voss), Pitch Anything
(Klaff), Impro (Johnstone). Повний канон з головними правилами кожної книги лежить у
[references/library.md](skills/numo-agent-talk/references/library.md).

## Ліцензія і безпека

MIT на скіл і його структуру. Текст правил додатково доступний за CC BY 4.0, якщо потрібна атрибуція. Про вразливості
пиши за [SECURITY.md](SECURITY.md), про внески за [CONTRIBUTING.md](CONTRIBUTING.md).
