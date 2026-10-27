# goit-aiqa-pipeline

QA пайплайн на скілах Claude Code з курсу AI-QA Pipeline Bootcamp, GoIT. Він веде задачу Jira від збору контексту до аудиту тестового покриття.

- `docs/hw01-architecture/`: ДЗ 1, архітектура пайплайну і схема `pipeline_architecture.png` (її малює `draw_pipeline.py`).
- `docs/hw02-jira-task-context/`: ДЗ 2, опис скіла jira-task-context і запуску на задачі KAN-7.
- `Task Runs/KAN-7/`: результати скілів для задачі KAN-7.
- `.claude/skills/`: скіли jira-task-context, requirements-grooming і qa-checklist.

## Як запустити

Відкрити папку в Claude Code, скіли підхопляться з `.claude/skills/`. Для jira-task-context потрібен підключений Atlassian MCP. Результати кожного прогону зберігаються в `Task Runs/<ISSUEKEY>/`.
