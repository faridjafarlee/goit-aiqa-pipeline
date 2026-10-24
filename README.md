# goit-aiqa-pipeline

QA пайплайн на скілах Claude Code з курсу AI-QA Pipeline Bootcamp, GoIT. Він веде задачу Jira від збору контексту до аудиту тестового покриття.

- `docs/hw01-architecture/`: ДЗ 1, архітектура пайплайну і схема `pipeline_architecture.png` (її малює `draw_pipeline.py`).
- `.claude/skills/`: скіли jira-task-context, requirements-grooming і qa-checklist.

## Як запустити

Відкрити папку в Claude Code, скіли підхопляться з `.claude/skills/`. Для jira-task-context потрібен підключений Atlassian MCP. Результати кожного прогону зберігаються в `Task Runs/<ISSUEKEY>/`.
