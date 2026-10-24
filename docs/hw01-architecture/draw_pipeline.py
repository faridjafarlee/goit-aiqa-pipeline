#!/usr/bin/env python3
"""ДЗ1: схема AI-QA пайплайну. Скелет курсу (10 скілів у 4 фазах) плюс власні доповнення:
ворота між етапами, теги джерела, профілі прогону, run.json, run-retro, шар безпеки.
Генерує pipeline_architecture.png (Pillow)."""
from PIL import Image, ImageDraw, ImageFont
import math

W, H = 2400, 1940
img = Image.new('RGB', (W, H), 'white'); d = ImageDraw.Draw(img)
FONT = '/System/Library/Fonts/Supplemental/Arial Unicode.ttf'
F = lambda s: ImageFont.truetype(FONT, s)
F_T, F_H, F_B, F_S, F_XS = F(34), F(24), F(20), F(17), F(15)
INK, GREY = '#1f2937', '#6b7280'
ACC, ACC_BG = '#be185d', '#fdf2f8'  # мої доповнення
PH = {1: ('#eef2ff', '#4338ca'), 2: ('#ecfeff', '#0e7490'), 3: ('#f0fdf4', '#15803d'), 4: ('#fff7ed', '#c2410c')}


def text_c(box, txt, font, fill=INK):
    x0, y0, x1, y1 = box; lines = txt.split('\n')
    bb = [d.textbbox((0, 0), l, font=font) for l in lines]
    th = sum(b[3] - b[1] for b in bb) + 5 * (len(lines) - 1); y = (y0 + y1 - th) / 2
    for l, b in zip(lines, bb):
        d.text(((x0 + x1 - (b[2] - b[0])) / 2, y - b[1]), l, font=font, fill=fill); y += b[3] - b[1] + 5


def lines(x, y, items, font=F_S, fill=INK, step=34):
    for i, t in enumerate(items):
        d.text((x, y + i * step), t, font=font, fill=fill)


def arrow(p, q, color=INK, w=3):
    d.line([p, q], fill=color, width=w); a = math.atan2(q[1] - p[1], q[0] - p[0])
    for s in (1, -1):
        d.line([q, (q[0] - 16 * math.cos(a + s * .45), q[1] - 16 * math.sin(a + s * .45))], fill=color, width=w)


def path(points, color=INK, w=3):
    d.line(points[:-1], fill=color, width=w, joint='curve'); arrow(points[-2], points[-1], color, w)


def gate(cx, cy, letter, who):
    r = 30
    d.polygon([(cx, cy - r), (cx + r, cy), (cx, cy + r), (cx - r, cy)], fill=ACC, outline=ACC)
    text_c((cx - r, cy - r, cx + r, cy + r), letter, F_B, 'white')
    if who:
        d.multiline_text((cx, cy + r + 6), who, font=F_XS, fill=ACC, anchor='ma', align='center', spacing=3)


SW, SH = 380, 175


def skill(x, y, n, name, out, mine, phase):
    _, edge = PH[phase]
    d.rounded_rectangle((x, y, x + SW, y + SH), 14, fill='white', outline=edge, width=3)
    d.ellipse((x + 12, y + 12, x + 50, y + 50), fill=edge); text_c((x + 12, y + 12, x + 50, y + 50), str(n), F_B, 'white')
    d.text((x + 62, y + 18), name, font=F_B, fill=INK)
    d.multiline_text((x + 16, y + 60), out, font=F_S, fill=GREY, spacing=5)
    if mine:
        d.multiline_text((x + 16, y + 112), mine, font=F_XS, fill=ACC, spacing=4)


# Заголовок
d.text((40, 24), 'AI-QA пайплайн: ланцюг із трасуванням і воротами (ДЗ1)', font=F_T, fill=INK)
d.text((40, 74), 'Вхід: тікет Jira (Atlassian MCP)  ·  артефакти: Task Runs/<ISSUEKEY>/<ISSUEKEY>-*.md  ·  '
       'дані рухаються лише вперед, вхідні файли тільки для читання', font=F_S, fill=GREY)

# Профіль прогону (доповнення)
d.rounded_rectangle((40, 118, 2360, 196), 14, fill=ACC_BG, outline=ACC, width=2)
d.text((60, 128), '★ Профіль прогону (обирає QA на старті)', font=F_B, fill=ACC)
d.text((60, 160), 'Lite: скіли 1-4, ручне тестування і final-report (дрібні задачі й баги)   ·   '
       'Standard: усі 10 скілів і ворота A-F   ·   '
       'Critical (гроші, безпека, PII): Standard + незалежний суддя на іншій моделі для скілів 6 і 10',
       font=F_S, fill=INK)

# Вхід
d.rounded_rectangle((40, 300, 300, 400), 14, fill='#f3f4f6', outline=GREY, width=2)
text_c((40, 300, 300, 400), 'Тікет Jira\n(ключ / URL)', F_B)
d.rounded_rectangle((40, 425, 300, 520), 14, fill='#f3f4f6', outline=GREY, width=2)
text_c((40, 425, 300, 520), 'Людина-QA\n(вкладення, відповіді,\nапрув на воротах)', F_S)

# Фази
P1, P2, P3, P4 = (330, 225, 2360, 565), (330, 600, 1290, 945), (1320, 600, 2360, 945), (330, 1020, 2360, 1290)
for n, title, box in [(1, 'Фаза 1 · Вимоги → тест-кейси', P1), (2, 'Фаза 2 · Аналіз змін і перевірка за кодом', P2),
                      (3, 'Фаза 3 · Перевірка запущеного застосунку', P3), (4, 'Фаза 4 · Аналіз і аудит', P4)]:
    fill, edge = PH[n]
    d.rounded_rectangle(box, 18, fill=fill, outline=edge, width=2)
    d.text((box[0] + 20, box[1] + 12), title, font=F_H, fill=edge)

S = {1: (360, 280), 2: (890, 280), 3: (1420, 280), 4: (1950, 280),
     5: (355, 655), 6: (865, 655), 7: (1440, 655), 8: (1950, 655),
     9: (360, 1080), 10: (890, 1080)}
SK = {
    1: ('jira-task-context', 'Збирач · Jira через MCP\n→ <KEY>-context.md', '★ jira-snapshot.md, теги джерела\n★ позначки «конфлікт», «не вказано»', 1),
    2: ('requirements-grooming', 'Аналітик · Q&A з людиною\n→ <KEY>-requirements.md (REQ-ID)', '★ кожна REQ зберігає тег джерела', 1),
    3: ('qa-checklist', 'Аналітик · атомарні перевірки\n→ <KEY>-checklist.md (REQ-x.y)', '', 1),
    4: ('qa-test-cases', 'Аналітик · кроки, дані, surface-теги\n→ <KEY>-test-cases.md', '★ очікуваний результат\n    посилається на REQ', 1),
    5: ('pr-summary', 'Збирач · PR через gh CLI\n→ <KEY>-pr-summary.md', '★ gh лише на читання', 2),
    6: ('code-review', 'Верифікатор · PASS/FAIL/QA/N/A\n→ <KEY>-code-review.md', '★ кожен вердикт із цитатою file:line', 2),
    7: ('backend-testing', 'Верифікатор · [API] [DB] [Payment]\n→ <KEY>-backend-testing.md', '★ статус BLOCKED, доказ\n    до кожного вердикту', 3),
    8: ('web-testing', 'Верифікатор · [UI], Playwright/MCP\n→ <KEY>-web-testing.md', '★ окремий профіль браузера,\n    скріншот як доказ', 3),
    9: ('defect-analysis', 'Аналітик · шар, серйозність, причина\n→ <KEY>-defect-analysis.md', '', 4),
    10: ('coverage-critic', 'Аудитор · прогалини покриття\n→ <KEY>-coverage-critic.md', '★ RTM рахує скрипт, критик\n    оцінює якість покриття', 4),
}
for n, (x, y) in S.items():
    nm, out, mine, ph = SK[n]; skill(x, y, n, nm, out, mine, ph)

R = lambda n: (S[n][0] + SW, S[n][1] + SH // 2)
L = lambda n: (S[n][0], S[n][1] + SH // 2)
B = lambda n: (S[n][0] + SW // 2, S[n][1] + SH)
T = lambda n: (S[n][0] + SW // 2, S[n][1])

# Фаза 1: 1 →A→ 2 →B→ 3 → 4 →C
arrow((300, 350), (360, 350))
gy = S[1][1] + SH // 2
arrow(R(1), (815, gy)); gate(845, gy, 'A', 'lint +\nлюдина'); arrow((875, gy), L(2))
arrow(R(2), (1345, gy)); gate(1375, gy, 'B', 'людина'); arrow((1405, gy), L(3))
arrow(R(3), L(4))
gate(B(4)[0], 500, 'C', '')
d.text((B(4)[0] + 40, 490), 'lint', font=F_XS, fill=ACC)
d.line([B(4), (B(4)[0], 470)], fill=INK, width=3)
d.line([(B(4)[0], 530), (B(4)[0], 582), (T(6)[0], 582)], fill=INK, width=3); arrow((T(6)[0], 582), T(6))
d.text((1745, 492), 'тест-кейси + surface-теги (для скілів 6, 7, 8)', font=F_XS, fill=GREY)
d.multiline_text((355, 860), 'Кейси, які code-review підтвердив цитатами коду (PASS), далі не тестуються\n(навчальне спрощення курсу; у Critical перевіряється все)', font=F_XS, fill=GREY, spacing=4)
d.text((372, 470), 'контекст-файл (source of truth) читають скіли 2, 3, 4 і 10', font=F_XS, fill='#7c3aed')

# Фаза 2 → D → Фаза 3 (послідовно: backend, потім web)
arrow(R(5), L(6))
dy = S[6][1] + SH // 2
arrow(R(6), (1350, dy)); gate(1380, dy, 'D', 'lint'); arrow((1410, dy), L(7))
arrow(R(7), L(8))
d.text((1832, dy + 14), 'незакрите', font=F_XS, fill=GREY)
d.text((1832, dy + 32), 'з 7 → 8', font=F_XS, fill=GREY)
d.text((1340, 905), 'маршрути за тегами: [API] [DB] [Payment] → 7;  [UI] і те, що не закрив скіл 7 → 8', font=F_XS, fill=GREY)

# Фаза 3 → E → Фаза 4
ey = 880
d.line([B(7), (B(7)[0], ey)], fill=INK, width=3); d.line([B(8), (B(8)[0], ey)], fill=INK, width=3)
d.line([(B(7)[0], ey), (B(8)[0], ey)], fill=INK, width=3)
ex = 2260; d.line([(B(8)[0], ey), (ex - 30, ey)], fill=INK, width=3); gate(ex, ey, 'E', '')
d.text((ex + 36, ey - 10), 'lint', font=F_XS, fill=ACC)
ax9 = d.textbbox((P4[0] + 20, P4[1] + 12), 'Фаза 4 · Аналіз і аудит', font=F_H)[2] + 40
assert ax9 < S[9][0] + SW - 20, ax9
d.line([(ex, ey + 30), (ex, 985), (ax9, 985)], fill=INK, width=3)
arrow((ax9, 985), (ax9, S[9][1])); arrow((T(10)[0], 985), T(10))
d.text((1000, 958), 'об’єднання результатів 6, 7, 8', font=F_XS, fill=GREY)

# Фаза 4: 9 → 10 →F→ людина → run-retro
arrow(R(9), L(10)); d.text((752, 1140), 'дефекти', font=F_XS, fill=GREY)
fy = S[10][1] + SH // 2
arrow(R(10), (1325, fy)); gate(1355, fy, 'F', 'людина'); arrow((1385, fy), (1420, fy))
d.rounded_rectangle((1420, 1100, 1820, 1235), 14, fill='white', outline=INK, width=3)
text_c((1420, 1100, 1820, 1235), 'Рішення людини:\nDone або повернути\nна потрібний етап', F_B)
arrow((1820, fy), (1950, fy))
d.rounded_rectangle((1950, 1080, 2330, 1255), 14, fill=ACC_BG, outline=ACC, width=3)
d.text((1966, 1096), '★ run-retro', font=F_B, fill=ACC)
d.multiline_text((1966, 1136), 'правки людини на воротах\n→ нові правила й заборони\n→ knowledge/lessons.md\n(лише після апруву)',
                 font=F_S, fill=INK, spacing=5)

# Нижні панелі
PY0, PY1 = 1325, 1785
d.rounded_rectangle((40, PY0, 830, PY1), 18, fill=ACC_BG, outline=ACC, width=2)
d.text((60, PY0 + 12), '★ Ворота між етапами', font=F_H, fill=ACC)
lines(60, PY0 + 60, [
    'A  після 1: у кожного факту тег джерела; цитати',
    '    й числа знайдено в jira-snapshot.md; людина',
    '    перевіряє контекст (конфлікти, межі, вкладення)',
    'B  після 2: людина затверджує реєстр вимог',
    'C  після 4: RTM без «сиріт»: REQ → перевірка → TC,',
    '    у кожного TC є surface-тег',
    'D  після 6: кожна цитата коду є в diff PR',
    'E  після 7, 8: кожен вердикт має файл-доказ,',
    '    у звітах немає токенів і паролів',
    'F  після 10: людина вирішує Done або повернення',
    'Не пройшли ворота → наступний скіл не запускається',
], font=F_S, step=33)

d.rounded_rectangle((850, PY0, 1600, PY1), 18, fill=ACC_BG, outline=ACC, width=2)
d.text((870, PY0 + 12), '★ Наскрізні складові', font=F_H, fill=ACC)
lines(870, PY0 + 60, [
    'pipeline-lint (Python): детерміновані перевірки',
    '    на воротах A, C, D, E',
    'run.json: журнал прогону (версія скіла, модель,',
    '    effort, hash входів і виходів, статус, хто затвердив)',
    'history/: попередні версії артефактів замість',
    '    мовчазного перезапису',
    'Новий прогін: діф jira-snapshot показує, що',
    '    змінилось у Jira; людина вирішує, що переганяти',
    'Суддя (Critical) завжди на іншій моделі, ніж автор',
], font=F_S, step=33)
d.text((870, PY0 + 372), 'Курс:', font=F_B, fill=INK)
lines(870, PY0 + 404, [
    'final-report: звіт у будь-який момент після скіла 6',
    'surface-routing.md, language-rule.md, конфіги доступу',
], font=F_S, step=30)

d.rounded_rectangle((1620, PY0, 2360, PY1), 18, fill=ACC_BG, outline=ACC, width=2)
d.text((1640, PY0 + 12), '★ Безпека', font=F_H, fill=ACC)
lines(1640, PY0 + 60, [
    'Atlassian MCP і gh: токени лише на читання',
    'Текст тікета, PR, логів і скрінів є даними,',
    '    а не інструкціями для агента',
    'Посилання з тікета агент не відкриває',
    'Секрети тільки через env; у звіти й чат',
    '    вони не потрапляють (перевіряють ворота E)',
    'web-testing: окремий профіль браузера',
    'Платежі тільки в test mode',
    'Кожна задача в новому чаті (/clear)',
    'Нічого не пишеться в Jira чи knowledge base',
    '    без апруву людини',
], font=F_S, step=33)

# Легенда й моделі
ly = 1815
d.rectangle((40, ly + 4, 64, ly + 24), fill='#eef2ff', outline='#4338ca', width=2)
d.text((74, ly), 'скелет курсу (10 скілів, final-report, довідники)', font=F_S, fill=INK)
d.rectangle((560, ly + 4, 584, ly + 24), fill=ACC_BG, outline=ACC, width=2)
d.text((594, ly), '★ мої доповнення', font=F_S, fill=ACC)
d.text((800, ly), 'Категорії: збирачі (1, 5) · аналітики (2, 3, 4, 9) · верифікатори (6, 7, 8) · аудитор (10). '
       '«Повне покриття» не означає відсутність багів.', font=F_S, fill=INK)
d.text((40, ly + 44), 'Моделі (людина перемикає вручну): збирачі 1 і 5 на Haiku або Sonnet з low; аналітики 2, 3, 4, 9 '
       'на Sonnet з medium; верифікатори 6, 7, 8 на Sonnet з high; суддя завжди на іншій моделі, ніж автор артефакту.',
       font=F_S, fill=GREY)
img.save('pipeline_architecture.png'); print('saved', img.size)
