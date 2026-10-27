# Приклад еталонного контекст-файлу

Приклад зроблено на реальній задачі KAN-7 і звірено з Jira 2026-10-27: кожен текст, число й умова є в задачі,
нічого не додано. Використовуй його для калібрування структури й деталізації, а не як джерело вимог для інших задач.

---

# KAN-7 - [Jafarli] Password Recovery: Forgot Password and Reset Link

Джерело: https://neoversity-ak.atlassian.net/browse/KAN-7
Тип: Task
Згенеровано: 2026-10-27

## Мета

"Implement password recovery for registered users. On the `/forgot-password` page the user enters an email and requests a reset link. The link opens the `/reset-password` page, where the user sets a new password and confirms it." (опис)

## Межі

- У межах задачі: посилання "Forgot password?" на `/login`, сторінки `/forgot-password` і `/reset-password`, їхні поля, валідація й повідомлення, запити `POST /api/password/forgot` і `POST /api/password/reset` (опис; Additional; AC).
- Поза межами задачі: Не вказано в Jira.

## Вимоги

### Форма загалом

- "Each field renders with its label and a required asterisk; placeholders are as specified above." (AC)
- "Validation triggers on form submit." (AC)
- "Errors are displayed below the corresponding field in red text." (AC)

### Entry point

- "The "Forgot password?" link is displayed below the Password field on the `/login` page and opens `/forgot-password`." (опис; AC: "The "Forgot password?" link on `/login` opens `/forgot-password`.")

### Page: Forgot password

Параметри поля (таблиця Page: Forgot password):
- Type: email
- Label: "Email"
- Placeholder: "anna@example.com"
- Required: yes
- Button: "Send reset link"

Правила валідації і тексти помилок (таблиця Validation rules — Email; AC):
- Field empty: "Email is required"
- Invalid format (missing @, domain without a dot): "Please enter a valid email address"

Результат запиту:
- "After a successful request the form is replaced with the message: "If an account exists for this email, we've sent a password reset link."" (опис)
- "For security reasons, the same confirmation message is shown whether or not the email is registered." (опис)
- "For a registered email, `POST /api/password/forgot` returns `200` and the confirmation message is shown." (AC)
- "If the email is not registered, the server returns `404` and the page shows "No account found with this email"." (AC)
- Розбіжність між джерелами: опис "the same confirmation message is shown whether or not the email is registered"; AC: для незареєстрованого email "the server returns `404` and the page shows "No account found with this email"". Не узгоджено в Jira.
- "Email lookup is case-insensitive (`Anna@example.com` and `anna@example.com` are the same user)." (Additional)

Повторний запит посилання:
- "The user can request a new link after a short delay." (опис)
- Уточнення: "the "Resend link" button becomes active 60 seconds after the previous request and shows a countdown "Resend in 60s"." (коментар ai.qa.students+1, 2026-10-27)

### Reset link

- "The reset link is valid for 30 minutes and can be used only once." (опис)
- "The reset link opens `/reset-password` with the New password and Confirm new password fields." (AC)
- "An expired link (older than 60 minutes) shows "This reset link has expired. Please request a new one."" (AC)
- "A link that was already used shows "This reset link has already been used."" (AC)
- Розбіжність між джерелами: опис "valid for 30 minutes"; AC "An expired link (older than 60 minutes)". Не узгоджено в Jira.

### Page: Reset password

Параметри полів (таблиця Page: Reset password):

| Parameter | New password | Confirm new password |
|---|---|---|
| Type | password | password |
| Label | New password | Confirm new password |
| Placeholder | Min. 8 characters | Re-enter new password |
| Maximum length | 64 characters | 64 characters |
| Required | yes | yes |
| Button | Reset password | |

- "Both password fields mask the input (type `password`)." (Additional)

Правила валідації New password і тексти помилок (таблиця Validation rules — New password):
- Field empty: "Password is required"
- Fewer than 8 characters: "Password must be at least 8 characters"
- More than 64 characters: "Password must not exceed 64 characters"
- No uppercase letter: "Password must contain at least one uppercase letter"
- No number: "Password must contain at least one number"
- "The new password must differ from the current password." (AC)

Правила валідації Confirm new password і тексти помилок (таблиця Validation rules — Confirm new password; AC):
- Field empty: "Please confirm your password"
- Does not match New password: "Passwords do not match"

Після скидання:
- "After a successful reset the user is redirected to `/login` with the message "Your password has been reset. Please log in."" (AC)

### Серверний контракт

- "The reset request is sent as `email` in the `POST /api/password/forgot` request." (Additional)
- "The new password is sent as `token` and `password` in the `POST /api/password/reset` request; the token is taken from the reset link." (Additional)
- "The server rejects an invalid or expired token with `400` and a `message` field." (AC)
- "The server enforces the password rules and returns `400` naming the failing rule." (AC)

## Додаткові вимоги (з коментарів)

- "After the password is reset, all active sessions of the user must be logged out." (коментар ai.qa.students+1, 2026-10-27)

## Повʼязаний Jira-контекст

> Ця секція лише для ознайомлення з контекстом.
> Її пункти не є вимогами поточної задачі, і наступні скіли їх не обробляють.

- `KAN-1` (Epic "User Registration Form"), звʼязок relates to. Задачу не відкривали, її вимоги в цей контекст не переносяться.

---

Що показує приклад:
- Тексти помилок, числа й умови збережено дослівно мовою оригіналу, без узагальнень.
- Біля кожної вимоги вказано джерело. Якщо факт є в кількох джерелах (таблиця і AC), булет один, а джерела перелічено.
- Коментар, що уточнює вимогу (затримка перед новим посиланням), стоїть поруч із нею у "Вимогах".
- Коментар з новою вимогою (вихід з усіх сесій) винесено в "Додаткові вимоги" з автором і датою.
- Коментар про процес (макети в пʼятницю) у файл не потрапив.
- Розбіжності (30 / 60 хвилин; однакове повідомлення / `404`) записано з обома значеннями і не вирішено.
- Повʼязана задача подана лише ключем, типом, назвою і типом звʼязку з Jira.
- Межі, яких немає в Jira, позначено "Не вказано в Jira".

У KAN-7 вкладень немає, тому немає й секції "Вкладення". Якщо вони є, секція виглядає так:

## Вкладення

- `<назва файлу>.png` (PNG, завантажено користувачем у чат) - <що містить>; дані перенесено в "Вимоги".
- `<назва файлу>.mp4` (відео) - наявне, але не оброблене (відео не підтримується).
