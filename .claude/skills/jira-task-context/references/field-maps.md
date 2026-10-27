# KAN Jira Field Maps

Карти полів для проєкту KAN "QA pipeline" у навчальній Jira `neoversity-ak.atlassian.net`
(cloudId `cd52b9dc-9af2-4871-b83e-93ea86ecb36c`). Використовуй їх як є, не перевідкривай метадані на кожному запуску.

Карти перевірено 2026-10-27 через Atlassian MCP `getJiraIssueTypeMetaWithFields` для проєкту KAN.
Типи задач у проєкті: Epic (10005), Subtask (10006), Task (10007). Story і Bug у KAN немає.
Кастомних полів для вимог (User story, Acceptance criteria, Notes for QA) у KAN немає:
опис, критерії приймання й таблиці лежать у системному полі `description`.

Якщо поле з карти перестало повертатися, онови карту після нової перевірки метаданих. ID не вгадуй.

## Що не читати

Для всіх типів не запитуй і не переноси у файл PM-дані й службові поля:
assignee, reporter, priority, status, labels, fixVersions, duedate, created, updated,
`customfield_10000` (development), `customfield_10001` (Team), `customfield_10015` (Start date),
`customfield_10019` (Rank), `customfield_10021` (Flagged), `customfield_10037` (Vulnerability).

Не запитуй `customfield_10923`, `customfield_10594`, `customfield_10424`, `customfield_11717`.
Їх запитував скіл з уроку 2 для KAN-4, але у метаданих KAN цих полів немає, тож вони завжди порожні.

## Task (10007)

| Значення | Ключ поля | Обовʼязкове |
|---|---|---|
| Назва | summary | так |
| Опис (вимоги, AC, таблиці) | description | так |
| Тип задачі | issuetype | так (для маршрутизації) |
| Коментарі | comment | ні |
| Вкладення | attachment | ні |
| Повʼязані задачі | issuelinks | ні (лише фон) |
| Батьківська задача (епік) | parent | ні (лише фон) |

Запит: `fields: ["summary", "description", "issuetype", "comment", "attachment", "issuelinks", "parent"]`.

## Subtask (10006)

Ті самі поля, що й у Task. `parent` у Subtask обовʼязковий у Jira, але для контексту це лише фон:
вимоги батьківської задачі в контекст підзадачі не переносяться.

## Epic (10005) та інші типи

Карти немає. Епік обʼєднує кілька задач, а один контекст-файл відповідає одній задачі.
Зупинись і попроси ключ конкретної задачі (Task або Subtask).
