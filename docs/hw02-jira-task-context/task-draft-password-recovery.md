# Чернетка задачі для Jira (проєкт KAN)

Тип: Task. Звʼязок: relates to KAN-1 (User Registration Form).
Summary: `[Jafarli] Password Recovery: Forgot Password and Reset Link`

## Description (піде в Jira як є)

**Description:**

Implement password recovery for registered users. On the `/forgot-password` page the user enters an email and requests a reset link. The link opens the `/reset-password` page, where the user sets a new password and confirms it. The reset link is valid for 30 minutes and can be used only once. For security reasons, the same confirmation message is shown whether or not the email is registered.

**Entry point**

The "Forgot password?" link is displayed below the Password field on the `/login` page and opens `/forgot-password`.

**Page: Forgot password**

| Parameter | Value |
|---|---|
| Type | email |
| Label | Email |
| Placeholder | anna@example.com |
| Required | yes |
| Button | Send reset link |

**Validation rules — Email:**

| Rule | Error message |
|---|---|
| Field empty | "Email is required" |
| Invalid format (missing @, domain without a dot) | "Please enter a valid email address" |

After a successful request the form is replaced with the message: "If an account exists for this email, we've sent a password reset link."

The user can request a new link after a short delay.

**Page: Reset password**

| Parameter | New password | Confirm new password |
|---|---|---|
| Type | password | password |
| Label | New password | Confirm new password |
| Placeholder | Min. 8 characters | Re-enter new password |
| Maximum length | 64 characters | 64 characters |
| Required | yes | yes |
| Button | Reset password | |

**Validation rules — New password:**

| Rule | Error message |
|---|---|
| Field empty | "Password is required" |
| Fewer than 8 characters | "Password must be at least 8 characters" |
| More than 64 characters | "Password must not exceed 64 characters" |
| No uppercase letter | "Password must contain at least one uppercase letter" |
| No number | "Password must contain at least one number" |

**Validation rules — Confirm new password:**

| Rule | Error message |
|---|---|
| Field empty | "Please confirm your password" |
| Does not match New password | "Passwords do not match" |

### Additional:

* The reset request is sent as `email` in the `POST /api/password/forgot` request.
* The new password is sent as `token` and `password` in the `POST /api/password/reset` request; the token is taken from the reset link.
* Email lookup is case-insensitive (`Anna@example.com` and `anna@example.com` are the same user).
* Both password fields mask the input (type `password`).

### Acceptance criteria:

* The "Forgot password?" link on `/login` opens `/forgot-password`.
* Each field renders with its label and a required asterisk; placeholders are as specified above.
* Validation triggers on form submit.
* An empty Email shows "Email is required"; an invalid format shows "Please enter a valid email address".
* For a registered email, `POST /api/password/forgot` returns `200` and the confirmation message is shown.
* If the email is not registered, the server returns `404` and the page shows "No account found with this email".
* The reset link opens `/reset-password` with the New password and Confirm new password fields.
* An expired link (older than 60 minutes) shows "This reset link has expired. Please request a new one."
* A link that was already used shows "This reset link has already been used."
* The new password must differ from the current password.
* An empty confirmation shows "Please confirm your password"; a confirmation that does not match shows "Passwords do not match".
* Errors are displayed below the corresponding field in red text.
* After a successful reset the user is redirected to `/login` with the message "Your password has been reset. Please log in."
* The server rejects an invalid or expired token with `400` and a `message` field.
* The server enforces the password rules and returns `400` naming the failing rule.

## Коментарі (3 окремі коментарі після створення задачі)

1. `After the password is reset, all active sessions of the user must be logged out.`
2. `Clarification for the delay before a new link: the "Resend link" button becomes active 60 seconds after the previous request and shows a countdown "Resend in 60s".`
3. `Design mockups for both pages will be ready on Friday. QA can start with the API checks.`

## Що тут закладено для перевірки скілів (у Jira не йде)

- Суперечності: строк дії посилання 30 хв в описі проти 60 хв в AC; однакове повідомлення для будь-якого email в описі проти `404` і "No account found with this email" в AC.
- Неповні місця: "after a short delay" без числа; правило "must differ from the current password" без тексту помилки; немає правила про спецсимвол і немає таблиці для помилок посилання.
- Коментарі: №1 нова вимога (має піти в "Додаткові вимоги"), №2 уточнює наявну вимогу про затримку (має піти в "Вимоги"), №3 процес (має бути проігнорований).
- Вкладень немає: Atlassian MCP не вміє їх завантажувати.
