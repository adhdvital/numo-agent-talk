# numo-agent-talk

Скіл, який вчить вашого агента писати коротко, ясно і з позиції рівного: чат, пости, листи, повідомлення.

## Було і стало

**Було.** Доброго дня! Вибачте, що турбую. Просто хотів поцікавитись, чи не могли б ви, якщо буде можливість,
подивитись нашу пропозицію по інтеграції, яку ми надсилали минулого тижня. Ми розуміємо, що ви дуже зайняті, тому
заздалегідь дякуємо за будь-який фідбек, він для нас надзвичайно важливий.

**Стало.** Надсилаю пропозицію по інтеграції ще раз. Подивіться розділ про строки до пʼятниці і напишіть, що не
влаштовує. Якщо все гаразд, стартуємо з понеділка.

Обидва абзаци синтетичні, написані з нуля для цієї вітрини.

### Відповідь агента в чаті

**Без скіла.** Отже, підсумовуючи: варто зазначити, що я проаналізував ситуацію і, здається, можу сказати, що
проблема, ймовірно, полягає в конфігурації. Це досить поширена ситуація, яка часто виникає в подібних випадках.
Загалом, я б рекомендував, якщо це можливо, перевірити налаштування, хоча остаточне рішення, звісно, за вами.

**Зі скілом.** Впав деплой: у конфігу стоїть старий домен. Правлю і перезапускаю, це три хвилини.
Якщо домен змінили навмисно, скажи, і я підлаштую решту посилань.

### Повідомлення другу

**Без скіла.** Привіт! Вибач, що турбую, і вибач, що так пізно пишу. Просто хотів дізнатись, чи не міг би ти,
якщо в тебе раптом буде вільна хвилинка і якщо тобі це взагалі зручно, глянути мій текст. Заздалегідь дуже дякую!

**Зі скілом.** Привіт. Глянеш мій текст до четверга? Цікавить одне: чи зрозуміла перша половина.
Не встигаєш, скажи, віддам іншому.


## Установка

- Claude Code: `/plugin marketplace add adhdvital/numo-agent-talk`, далі `/plugin install numo-agent-talk@numo-agent-talk`
- Codex: клонуйте репо і скопіюйте теку `skills/numo-agent-talk` у `.agents/skills/` вашого проєкту
- Cursor: та сама тека, Cursor читає її через спільний каталог скілів проєкту
- Вбудовування в репо: `git subtree add` з цього репозиторію

## Як викликати

1. Слеш-команда за назвою скіла.
2. Звичайне прохання: «перепиши це, звучить як слоп», «скороти лист», «напиши пост».
3. Шлях до файла: «прожени цей текст через skills/numo-agent-talk».

## Чому скіл, а не промпт

Промпт живе одну сесію і вмирає. Скіл вмикається сам на потрібних словах, тримає правила в одному місці, читає ваш
локальний файл стилю і зупиняється перед надсиланням. Правила з поясненням «чому» агент виконує стабільніше, ніж список
заборон у системному промпті, а приклади «було і стало» працюють краще за будь-яку інструкцію.

## 10 правил зі скіла

1. Суть у першому рядку, бо все до неї читач губить (K1).
2. Коротка відповідь у 4 рядки, стеля 6, бо стислість читається як впевненість (K2).
3. Високий статус без вибачень і «просто», бо статус це відсутність виправдань (K3).
4. Без води, бо слово без роботи краде увагу в слів із роботою (K4).
5. Дієслово і виконавець, бо пасив ховає відповідальність (K5).
6. Доказ, джерело або чесна позначка «з памʼяті», бо впевненість без джерела це вигадка (K6).
7. Точні числа без округлень, бо заокруглення факту читається як брехня (K7).
8. Пояснення для людини поза контекстом, бо читач не бачив вашої розмови (K8).
9. Чисті знаки без довгого тире і тильд, бо машинні мітки видають машину (K10).
10. Надсилає людина після явного «так», бо надіслане не забирається назад (E7).

## Свій стиль

Запустіть режим `setup`, і скіл створить локальний файл `.writing-local.md` з вашим тоном, мовами, каналами і парами
«було і стало». Без файла скіл працює на повних дефолтах; локальний файл лише додає ваш голос зверху. Додайте його в
`.gitignore`, бо це особистий файл.

## Джерела

Метод стоїть на 25 книгах про письмо і статус. Ядро складають «Пиши, скорочуй» (Ільяхов, Саричева), The Elements of
Style (Strunk, White), Smart Brevity (VandeHei, Allen, Schwartz), Never Split the Difference (Voss), Pitch Anything
(Klaff) і Impro (Johnstone). Повний канон з головними правилами кожної книги лежить у
`skills/numo-agent-talk/references/library.md`.

## Версії

<details>
<summary>Історія версій</summary>

- 0.1.0, перший публічний реліз. 25 правил, 7 довідкових файлів, тести на спрацювання.

</details>

## Ліцензії і безпека

Код і структура скіла під ліцензією MIT. Текст правил додатково доступний за CC BY 4.0 для тих, кому потрібна
атрибуція. Як повідомити про вразливість, каже SECURITY.md; правила внесків лежать у CONTRIBUTING.md.

---

# numo-agent-talk (English)

A skill that teaches your agent to write short, clear, high-status text: chat replies, posts, emails, messages.

## Before and after

**Before.** Hi! Sorry to bother you. I just wanted to quickly check whether you might have had a chance to look at the
integration proposal we sent last week. We totally understand you are super busy, so thanks in advance for any
feedback, it would be extremely valuable to us.

**After.** Resending the integration proposal. Please review the timeline section by Friday and reply with what needs
to change. If it looks good, we start Monday.

Both paragraphs are synthetic, written from scratch for this page.

## Install

- Claude Code: `/plugin marketplace add adhdvital/numo-agent-talk`, then `/plugin install numo-agent-talk@numo-agent-talk`
- Codex: clone the repo and copy `skills/numo-agent-talk` into your project's `.agents/skills/`
- Cursor: same folder, read through the project's shared skills directory
- Embed: `git subtree add` from this repository

## Invoke

Use the slash command, or just ask: "rewrite this, it sounds like AI slop", "shorten this email", "draft a post".
You can also point the agent at `skills/numo-agent-talk`.

## Why a skill, not a prompt

A prompt lives for one session. A skill triggers itself on the right words, keeps the rules in one place, reads your
local style file, and always stops before anything is sent. A human sends, after an explicit yes.

## Personal style

Run the setup mode to create a local `.writing-local.md` with your own tone, languages, channels, and before-and-after
pairs. Without it the skill runs on full defaults; the local file only adds your voice on top. Add it to `.gitignore`,
it is a personal file.

## Sources

The method stands on 25 books about writing and status. The full canon with each book's key rules lives in
`skills/numo-agent-talk/references/library.md`. The Ukrainian half of this page also lists the six core books.

## Licenses

MIT for the skill code and structure. The rule texts are additionally available under CC BY 4.0. Security policy in
SECURITY.md, contribution rules in CONTRIBUTING.md.
