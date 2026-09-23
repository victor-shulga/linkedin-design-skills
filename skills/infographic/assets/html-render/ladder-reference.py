#!/usr/bin/env python3
"""REFERENCE BUILD — Ladder template, HTML+Chrome backend. 1080x1350, white BG.
Copy this file into the post folder, swap ROWS / title / rule, run it. See SKILL.md "Render backend".
"""
import subprocess, base64, pathlib

OUT = pathlib.Path(__file__).parent
ROOT = OUT.parent.parent
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# --- brand tokens (source of truth: victorshulga-design-system/index.html) ---
CORAL, CORAL_DEEP, CORAL_SOFT = "#E85A4F", "#C24235", "#FBEAE8"
INK, BODY, MUTED, LINE, CARD = "#161513", "#3D3D3A", "#6C6A64", "#E8E6E1", "#F7F5F1"

# --- rubric chip: pillar "GTM стратегія" ---
CHIP_LABEL, CHIP_BG, CHIP_FG = "GTM стратегія", CORAL, "#FFFFFF"

AVATAR = pathlib.Path.home() / ".claude/skills/infographic/assets/avatar.png"
photo_b64 = base64.b64encode(AVATAR.read_bytes()).decode()

BOWTIE = ('<svg width="44" height="44" viewBox="0 0 100 100">'
          '<rect width="100" height="100" rx="24" fill="#E85A4F"/>'
          '<path d="M14 24 L46 50 L14 76 Z" fill="#fff" stroke="#fff" stroke-width="11" stroke-linejoin="round"/>'
          '<path d="M86 24 L54 50 L86 76 Z" fill="#fff" stroke="#fff" stroke-width="11" stroke-linejoin="round"/>'
          '<circle cx="50" cy="50" r="7.5" fill="#1C1C1E"/></svg>')

# n(черга тесту), стадія, стан, заповнених крапок трасту, opacity фону, білий текст?
ROWS = [
    ("1", "Амбасадор", "рекомендує вас іншим", 6, 1.00, True),
    ("2", "Клієнт", "платить прямо зараз", 5, 0.82, True),
    ("3", "SQL", "бачив пропозал, не купив", 4, 0.62, True),
    ("4", "MQL", "був дзвінок, далі тиша", 3, 0.42, False),
    ("5", "Лід", "є діалог, ще нічого не було", 2, 0.24, False),
    ("6", "Проспект", "холодний, про вас не чув", 1, 0.11, False),
]

rows_html = ""
for i, (n, stage, state, dots, op, white) in enumerate(ROWS):
    indent = i * 30
    fg = "#FFFFFF" if white else INK
    sub = "rgba(255,255,255,.78)" if white else MUTED
    badge_bg = "rgba(255,255,255,.22)" if white else "#FFFFFF"
    dots_html = "".join(
        f'<span class="d" style="background:{fg};opacity:{"1" if k < dots else ".22"}"></span>'
        for k in range(6)
    )
    tag = '<span class="tag">сюди всі ллють тести</span>' if i == 5 else ""
    rows_html += (
        f'<div class="row" style="margin-left:{indent}px;background:rgba(232,90,79,{op})">'
        f'<span class="badge" style="background:{badge_bg};color:{CORAL_DEEP}">{n}</span>'
        f'<div class="txt"><div class="stage" style="color:{fg}">{stage}</div>'
        f'<div class="state" style="color:{sub}">{state}</div></div>'
        f'{tag}<div class="meter">{dots_html}</div></div>'
    )

HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=Inter+Tight:wght@600;700;800&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@500;600&display=swap" rel="stylesheet">
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{width:1080px;height:1350px;overflow:hidden;font-family:'Inter',sans-serif;background:#fff}}
.stage-w{{width:1080px;height:1350px;background:#fff;position:relative;padding:46px 56px 0}}

.chiprow{{text-align:center}}
.chip{{display:inline-flex;align-items:center;gap:8px;background:{CHIP_BG};color:{CHIP_FG};font-family:'Inter Tight';
  font-weight:700;font-size:14px;letter-spacing:.12em;text-transform:uppercase;padding:9px 18px;border-radius:999px}}
.chip i{{width:7px;height:7px;border-radius:50%;background:{CHIP_FG};opacity:.9}}

h1{{font-family:'Inter Tight';font-weight:800;font-size:44px;line-height:1.14;letter-spacing:-.015em;color:{INK};
  text-align:center;text-transform:uppercase;margin-top:20px}}
h1 mark{{background:{CORAL};color:#fff;padding:2px 14px 5px;border-radius:9px;display:inline-block;line-height:1.02}}
.sub{{font-family:'JetBrains Mono';font-weight:500;font-size:14px;letter-spacing:.06em;color:{MUTED};
  text-align:center;margin-top:16px;text-transform:uppercase}}

.main{{display:flex;gap:18px;margin-top:28px}}
.arrow{{width:58px;display:flex;flex-direction:column;align-items:center;padding-top:6px}}
.arrow .lab{{font-family:'JetBrains Mono';font-weight:600;font-size:12px;letter-spacing:.16em;color:{CORAL_DEEP};
  text-transform:uppercase;writing-mode:vertical-rl;transform:rotate(180deg);margin-top:14px}}

.ladder{{flex:1;display:flex;flex-direction:column;gap:15px}}
.hdr{{display:flex;justify-content:space-between;align-items:baseline;padding:0 22px 10px;
  font-family:'JetBrains Mono';font-weight:600;font-size:11.5px;letter-spacing:.16em;
  text-transform:uppercase;color:{MUTED}}}
.row{{height:112px;border-radius:14px;padding:0 22px;display:flex;align-items:center;gap:18px;position:relative}}
.badge{{width:46px;height:46px;flex:none;border-radius:12px;display:flex;align-items:center;justify-content:center;
  font-family:'Inter Tight';font-weight:800;font-size:23px}}
.txt{{flex:1}}
.stage{{font-family:'Inter Tight';font-weight:800;font-size:28px;letter-spacing:-.015em;line-height:1}}
.state{{font-family:'Inter';font-weight:500;font-size:15.5px;margin-top:7px}}
.meter{{display:flex;gap:6px;flex:none}}
.meter .d{{width:11px;height:11px;border-radius:50%}}
.tag{{background:{INK};color:#fff;flex:none;
  font-family:'JetBrains Mono';font-weight:600;font-size:11.5px;letter-spacing:.08em;text-transform:uppercase;
  padding:8px 12px;border-radius:8px;white-space:nowrap}}

.rule{{position:absolute;left:56px;right:56px;bottom:180px;background:{INK};border-radius:13px;
  padding:18px 24px;display:flex;align-items:center;gap:18px}}
.rn{{font-family:'Inter Tight';font-weight:800;font-size:15px;color:#fff;background:{CORAL};border-radius:8px;
  padding:7px 12px;letter-spacing:.08em;text-transform:uppercase;flex:none}}
.rt{{font-family:'Inter';font-weight:500;font-size:16px;color:#fff;line-height:1.4}}
.rt span{{color:{MUTED}}}

.footer{{position:absolute;left:0;right:0;bottom:0;height:150px;background:#fff;border-bottom:4px solid {CORAL};
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

  <h1>Новий офер тестують<br><mark>не на холодних</mark></h1>
  <div class="sub">Порядок тесту = зворотний до воронки</div>

  <div class="main">
    <div class="arrow">
      <svg width="26" height="800" viewBox="0 0 26 800">
        <path d="M13 40 L24 62 L2 62 Z" fill="{CORAL}"/>
        <rect x="10" y="60" width="6" height="736" rx="3" fill="{CORAL}" opacity=".28"/>
      </svg>
    </div>
    <div class="ladder">
      <div class="hdr"><span>Черга тесту</span><span>Траст</span></div>
      {rows_html}
    </div>
  </div>

  <div class="rule">
    <div class="rn">Правило</div>
    <div class="rt">У лідген іде тільки той офер, який уже продає.<br><span>Новий спершу показують тим, хто вже платить. Відповідь буде за тиждень.</span></div>
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
png = OUT / "offer-test-order.png"
subprocess.run([
    CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
    "--force-device-scale-factor=2", "--window-size=1080,1350",
    "--virtual-time-budget=6000", "--run-all-compositor-stages-before-draw",
    f"--screenshot={png}", str(OUT / "creative.html"),
], check=True, capture_output=True)
print("ok ->", png)
