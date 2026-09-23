#!/usr/bin/env python3
"""REFERENCE BUILD — Timeline Rows template, HTML+Chrome backend. 1080x1350, white BG.
Copy into the post folder, swap STREAMS / ROWS / title / rule band, run it.
See SKILL.md "Recipe: TIMELINE ROWS". Produces the "Таймлайн запуску аутбаунду" creative (31.08.2026).
"""
import subprocess, base64, pathlib

OUT = pathlib.Path(__file__).parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# --- brand tokens (source: victorshulga-design-system/index.html) ---
CORAL, CORAL_DEEP, CORAL_SOFT = "#E85A4F", "#C24235", "#FBEAE8"
INK, BODY, MUTED, LINE, CARD = "#161513", "#3D3D3A", "#6C6A64", "#E8E6E1", "#F7F5F1"

CHIP_LABEL, CHIP_BG, CHIP_FG = "Мультиканальний аутріч", INK, "#FFFFFF"

AVATAR = pathlib.Path.home() / ".claude/skills/infographic/assets/avatar.png"
photo_b64 = base64.b64encode(AVATAR.read_bytes()).decode()

BOWTIE = ('<svg width="44" height="44" viewBox="0 0 100 100">'
          '<rect width="100" height="100" rx="24" fill="#E85A4F"/>'
          '<path d="M14 24 L46 50 L14 76 Z" fill="#fff" stroke="#fff" stroke-width="11" stroke-linejoin="round"/>'
          '<path d="M86 24 L54 50 L86 76 Z" fill="#fff" stroke="#fff" stroke-width="11" stroke-linejoin="round"/>'
          '<circle cx="50" cy="50" r="7.5" fill="#1C1C1E"/></svg>')

# блоки: (назва, підпис, джерела, обсяг)
STREAMS = [
    ("Сигнал", "коли писати",
     ["вакансії", "рух штату", "тендери", "конференції"], "3–5% бази в моменті"),
    ("Дата-поінт", "що сказати",
     ["стек на сайті", "гео", "розмір команди", "портфоліо"], "майже вся база"),
    ("Інтент", "хто вже шукає",
     ["візити на сайт", "вхідні форми", "коментарі під постами"], "найменший обсяг"),
    ("Інбаунд", "заповнена форма",
     ["сайт", "лід-магніт", "калькулятор"], "найтепліші"),
]

# (тиждень, що будується, деталь, репліка CEO, що бачить CEO, opacity, білий текст?)
ROWS = [
    ("1–2",  "ICP, гіпотези, вибір сигналів",
             "каталог під нішу · прогрів доменів",
             "можемо це пропустити?", "слайди й таблиці", 0.10, False),
    ("3–4",  "База під сигнал і дозбір даних",
             "збираємо тих, у кого сигнал зараз",
             "де ліди?", "список компаній", 0.24, False),
    ("5",    "Перші відправки",
             "прогрів закінчився, сіквенс пішов",
             "тиждень без відповідей", "листи пішли", 0.42, False),
    ("6",    "Перші відповіді",
             "видно, який сигнал і оффер працює",
             "", "перші відповіді", 0.62, True),
    ("7–8",  "Перші зустрічі",
             "з тих, хто відповів на 2–3 дотику",
             "чому не всі дійшли?", "зустрічі в календарі", 0.81, True),
    ("9–12", "Правки і вихід на план",
             "той самий список дає інший результат",
             "а можна вдвічі більше?", "угоди в пайплайні", 1.00, True),
]

streams_html = ""
for name, caption, sources, vol in STREAMS:
    chips = "".join(f'<span class="src">{x}</span>' for x in sources)
    streams_html += (
        f'<div class="lcard">'
        f'<div class="lname">{name}</div>'
        f'<div class="lans">{caption}</div>'
        f'<div class="srcs">{chips}</div>'
        f'<div class="lvol">{vol}</div>'
        f'</div>'
    )

rows_html = ""
for i, (wk, build, detail, quote, sees, op, white) in enumerate(ROWS):
    fg = "#FFFFFF" if white else INK
    sub = "rgba(255,255,255,.82)" if white else MUTED
    if not quote:
        tag = ""
    else:
        cls = "q punch" if i == 1 else "q"
        tag = f'<span class="{cls}"><i>CEO</i>{quote}</span>'
    rows_html += (
        f'<div class="row" style="background:rgba(232,90,79,{op})">'
        f'<span class="badge">{wk}</span>'
        f'<div class="txt"><div class="build" style="color:{fg}">{build}</div>'
        f'<div class="detail" style="color:{sub}">{detail}</div></div>'
        f'{tag}'
        f'<div class="sees" style="color:{fg}">{sees}</div>'
        f'</div>'
    )

HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden;font-family:'Inter',sans-serif;background:#fff}}
.stage-w{{width:1080px;height:1350px;background:#fff;position:relative;padding:38px 56px 0}}

.chiprow{{text-align:center}}
.chip{{display:inline-flex;align-items:center;gap:8px;background:{CHIP_BG};color:{CHIP_FG};font-family:'Inter Tight';
  font-weight:700;font-size:14px;letter-spacing:.12em;text-transform:uppercase;padding:9px 18px;border-radius:999px}}
.chip i{{width:7px;height:7px;border-radius:50%;background:{CHIP_FG};opacity:.9}}

h1{{font-family:'Inter Tight';font-weight:800;font-size:42px;line-height:1.12;letter-spacing:-.015em;color:{INK};
  text-align:center;text-transform:uppercase;margin-top:16px}}
h1 mark{{background:{CORAL};color:#fff;padding:2px 14px 5px;border-radius:9px;display:inline-block;line-height:1.02}}
.sub{{font-family:'JetBrains Mono';font-weight:500;font-size:13px;letter-spacing:.06em;color:{MUTED};
  text-align:center;margin-top:12px;margin-bottom:18px;text-transform:uppercase}}

.srchdr{{font-family:'JetBrains Mono';font-weight:600;font-size:11.5px;letter-spacing:.16em;
  text-transform:uppercase;color:{MUTED};padding:0 4px 9px}}
.layers{{display:flex;gap:10px;align-items:stretch}}
.lcard{{flex:1;min-width:0;background:{CARD};border-radius:13px;padding:13px 13px 12px;display:flex;flex-direction:column}}
.lname{{font-family:'Inter Tight';font-weight:800;font-size:18px;letter-spacing:-.01em;color:{INK};line-height:1.1}}
.lans{{font-family:'Inter';font-weight:600;font-size:12.5px;color:{CORAL_DEEP};margin-top:6px;line-height:1.25}}
.srcs{{display:flex;flex-wrap:wrap;gap:5px;margin-top:9px}}
.src{{background:#fff;border:1px solid {LINE};border-radius:7px;padding:4px 8px;
  font-family:'Inter';font-weight:500;font-size:11.5px;color:{BODY};white-space:nowrap}}
.lvol{{font-family:'JetBrains Mono';font-weight:500;font-size:10px;letter-spacing:.05em;color:{MUTED};
  margin-top:auto;padding-top:10px;text-transform:uppercase}}

.hdr{{display:flex;justify-content:space-between;align-items:baseline;padding:15px 20px 8px;
  font-family:'JetBrains Mono';font-weight:600;font-size:11.5px;letter-spacing:.16em;
  text-transform:uppercase;color:{MUTED}}}
.rows{{display:flex;flex-direction:column;gap:8px}}
.row{{height:104px;border-radius:14px;padding:0 20px;display:flex;align-items:center;gap:14px}}
.badge{{min-width:70px;height:42px;flex:none;border-radius:11px;display:flex;align-items:center;justify-content:center;
  font-family:'Inter Tight';font-weight:800;font-size:20px;padding:0 10px;background:#FFFFFF;color:{CORAL_DEEP}}}
.txt{{flex:1;min-width:0}}
.build{{font-family:'Inter Tight';font-weight:700;font-size:20px;letter-spacing:-.01em;line-height:1.16}}
.detail{{font-family:'Inter';font-weight:500;font-size:13.5px;margin-top:5px;line-height:1.25}}
.q{{flex:none;white-space:nowrap;display:inline-flex;align-items:center;gap:9px;
  font-family:'Inter';font-weight:600;font-size:15px;color:{INK};
  background:#FFFFFF;border-radius:10px;padding:8px 13px 8px 9px}}
.q i{{font-style:normal;font-family:'JetBrains Mono';font-weight:600;font-size:10px;letter-spacing:.12em;
  color:#fff;background:{CORAL};border-radius:6px;padding:4px 6px}}
.q.punch{{background:{INK};color:#fff}}
.q.punch i{{background:#fff;color:{INK}}}
.sees{{font-family:'Inter Tight';font-weight:700;font-size:15.5px;flex:none;width:186px;text-align:right;line-height:1.2}}

.rule{{position:absolute;left:56px;right:56px;bottom:164px;background:{INK};border-radius:13px;
  padding:18px 20px;display:flex;align-items:center;gap:15px}}
.rn{{font-family:'Inter Tight';font-weight:800;font-size:13px;color:#fff;background:{CORAL};border-radius:8px;
  padding:7px 11px;letter-spacing:.08em;text-transform:uppercase;flex:none}}
.rt{{font-family:'Inter';font-weight:500;font-size:15.5px;color:#fff;line-height:1.4}}
.rnum{{margin-left:auto;flex:none;font-family:'Inter';font-weight:600;font-size:13.5px;color:#fff;
  border:1px solid rgba(255,255,255,.32);border-radius:8px;padding:6px 11px;white-space:nowrap}}

.footer{{position:absolute;left:0;right:0;bottom:0;height:146px;background:#fff;border-bottom:4px solid {CORAL};
  display:flex;align-items:center;justify-content:space-between;padding:0 56px}}
.fl{{display:flex;align-items:center;gap:15px}}
.ava{{width:56px;height:56px;border-radius:50%;border:3px solid {CORAL};object-fit:cover;object-position:50% 50%}}
.fname{{font-family:'Inter Tight',sans-serif;font-weight:700;color:{INK};font-size:20px;line-height:1;letter-spacing:-.01em}}
.pill{{display:inline-block;margin-top:9px;background:{CORAL};color:#fff;font-family:'Inter',sans-serif;
  font-weight:600;font-size:11.5px;letter-spacing:.06em;padding:6px 12px;border-radius:8px;text-transform:uppercase}}
.fr{{display:flex;align-items:center;gap:12px}}
.site{{font-family:'Inter',sans-serif;font-weight:500;color:{CORAL};font-size:16px}}
</style></head><body>
<div class="stage-w">
  <div class="chiprow"><span class="chip"><i></i>{CHIP_LABEL}</span></div>

  <h1>Таймлайн запуску<br><mark>аутбаунду</mark></h1>
  <div class="sub">Що будується, поки лідів ще нема</div>

  <div class="srchdr">Звідки беремо ліди</div>
  <div class="layers">{streams_html}</div>

  <div class="hdr"><span>Тиждень · що будується</span><span>Що бачить CEO</span></div>
  <div class="rows">{rows_html}</div>

  <div class="rule">
    <div class="rn">Строк</div>
    <div class="rt">Зустрічі зʼявляються на тижні 7. До того будується база під них.</div>
    <span class="rnum">145 сигналів у каталозі</span>
  </div>

  <div class="footer">
    <div class="fl">
      <img class="ava" src="data:image/png;base64,{photo_b64}">
      <div>
        <div class="fname">Victor Shulga</div>
        <span class="pill">Fractional CRO</span>
      </div>
    </div>
    <div class="fr">
      {BOWTIE}
      <span class="site">victorshulga.com</span>
    </div>
  </div>
</div></body></html>"""

(OUT / "creative.html").write_text(HTML, encoding="utf-8")
png = OUT / "timeline-rows.png"
subprocess.run([
    CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
    "--force-device-scale-factor=2", "--window-size=1080,1350",
    "--virtual-time-budget=6000", "--run-all-compositor-stages-before-draw",
    f"--screenshot={png}", str(OUT / "creative.html"),
], check=True, capture_output=True)
print("ok ->", png)
