---
name: infographic
description: Generates LinkedIn infographics (1080×1350) for the Victor Shulga personal brand (victorshulga.com) from raw text. Use whenever Viktor pastes text and asks for an infographic — "інфографіка", "зроби інфографіку", "comparison table", "step grid", "пончик", "лійка", "крива росту", "таймлайн", "драбина", "тір-ліст", "інструкція в 4 кроки", "how-to", "make an infographic from this" — or describes structured content that is NOT a carousel. Picks one of 24 catalogued shapes: read references/infographic-templates.md FIRST for what each shape serves, how it gets ruined, build mechanics, and the anti-monotony log that forbids repeating the previous creative shape. Ten have builders here (Comparison Table, Step Grid, Donut, Funnel, Growth Curve, Timeline, Block Grid, Vertical Steps, Ladder, Timeline Rows); fourteen more are specified in the catalogue (Spine + Satellites, Hub & Flows, Tier List, Claim + Evidence, Diagnostic Cards, Roster Grid, Panel Grid, Centre + Orbit, Spec Rail, Rail + Artifact, Maturity Staircase, Step Spine, Onion + Sectors, Named Venn). Two backends: Figma, or a build.py that screenshots HTML with headless Chrome — trigger it on "скриптом", "HTML-креатив", "не через Figma".
---

# /infographic

Generate LinkedIn infographics for the Victor Shulga personal brand (victorshulga.com) using his existing Figma design system. **Brand-pure palette**: white BG + coral + charcoal + forest only. NO pastels.

## When to trigger

- Viktor pastes text + says "інфографіка", "зроби інфографіку"
- Viktor describes structured content (table, steps, categories) and wants visuals
- Viktor says "comparison table", "step grid", "9 кроків як інфографіку"
- Viktor says "donut", "пончик", "pie", "лійка", "funnel", "крива росту", "growth curve", "таймлайн", "timeline", "before/after по осі"
- Any single-image structured visualization (NOT a multi-slide carousel — for that use `/linkedin-carousel`)

## Decision tree — which template to use

**Read `references/infographic-templates.md` FIRST.** It holds all twenty-four shapes with
the content each one serves and the way each gets ruined, plus the anti-monotony log:
do not repeat the shape used on the last creative. The table below covers only the ten
shapes that already have builders here; shapes 11-24 are specified in that file and
build on the HTML/Chrome backend.

Read the content. **Prefer a CHART over a text grid whenever the data has a shape** — proportions, a sequence with drop-off, change over time, or two poles on an axis. Text-in-boxes is the fallback, not the default.

| Content shape | Template |
|---|---|
| Parts of a whole / split of time, budget, channels, % that sum to 100 (4-6 slices) | **Donut / Pie** chart |
| A sequence that narrows — stages with drop-off, awareness→conversion, TOFU→BOFU | **Funnel** chart |
| A metric changing over time — growth, milestones (€0→€1M, week 1→12), trajectory | **Growth Curve** |
| Two opposed states on a horizontal axis (Reactive vs Proactive, Before vs After, early→late) with zones/phases | **Timeline** (1 or 2 stacked axes) |
| A single concept that needs its own diagram — niche focus, positioning, ICP attributes, population share, a score | **Chart atom v2** (Concentric / Quadrant / HubSpokes / DotGrid / ScoreRing) — standalone or inside a Block Grid card |
| 2-3 columns comparing categories (Weak vs Strong, Before vs After, Bad vs Good) across 4-6 rows | **Comparison Table** (text) |
| 5-12 sequential/parallel steps/tips, each title + 1-3 lines | **Step Grid 3×3** (text; or 2×3, 4×3) |
| A whole framework / playbook / deck condensed — 6-9 blocks, EACH needing its own little diagram (funnel, ladder, checklist, flow, chips) | **Block Grid** — dense N-card grid, mini-visual per card |
| A HOW-TO / setup / "do this then that" — 3-5 ordered steps, each deserving ONE full-width concrete visual (tool row, pill row, box row, input→output) | **Vertical Steps** — linear numbered sections, one band per step |
| A ranked ORDER over tiers — priority queue, trust ladder, maturity levels, "start here not there" (4-7 rows, each row carries a name + state + an intensity meter) | **Ladder** — HTML/Chrome backend, see recipe below |
| A PROCESS OVER TIME where each period has a hidden inside and a visible outside — launch plan, ramp-up, "what is built while nothing shows yet" (5-7 periods, each row = period + what happens + what the stakeholder sees, optional voice-of-stakeholder quote) | **Timeline Rows** — HTML/Chrome backend, see recipe below |
| Branching tree (1 → N → M with arrows) | **Custom build** — not templated, ~30-45 min |
| Multiple categorized cards + diagram + matrix (mixed canvas) | **Custom build** — not templated, ~45-60 min |

A single infographic may **combine** a chart band + a text band (e.g. donut on top, 3-tier funnel below) — see the demo pattern. Stack bands vertically with ~40-60px gutters.

If content is genuinely 2-3 things and short → ask Viktor if he wants it as 2-3 SLIDE CAROUSEL instead (better for LinkedIn engagement).

## Render backend — Figma vs HTML/Chrome

Two ways to produce the same 1080×1350 brand-pure image. **Pick one deliberately before building** and say which one you picked.

| | **Figma** (default) | **HTML + headless Chrome** |
|---|---|---|
| How | `use_figma` builds nodes in a new file | a `build.py` writes an HTML string, Chrome screenshots it |
| Deliverable | Figma file URL + PNG export by hand | PNG on disk, ready to upload |
| Viktor can edit after | yes, directly on canvas | no — edits go through the script |
| Best for | anything already templated here (charts, grids, tables, steps) | shapes CSS does in one line and Figma nodes do in twenty: staircase indents, opacity ramps across rows, `border-radius` cards, flex meters, precise letter-spacing |
| Iteration cost | a nudge = one more tool call | a nudge = edit a constant, re-run, look at the PNG |
| Risk | node math, font style strings, collapsing auto-layout | needs network for Google Fonts; Cyrillic falls back to serif without the right Chrome flags |

**Choose HTML/Chrome when** the layout is a repeated row/card structure driven by a data list (a ladder, a ranked table, a dense matrix), when you need CSS-native effects (opacity ramps, staircase offsets, pill tags inline in a flex row), or when Viktor wants the image regenerated repeatedly with different numbers. **Otherwise stay on Figma** — he can edit it afterwards, which is worth a lot.

### HTML/Chrome mechanics

Working reference (runs as-is, produces the "Новий офер тестують не на холодних" ladder):
`~/.claude/skills/infographic/assets/html-render/ladder-reference.py`

Copy it into the post's output folder, swap the data list + title + rule band, run it. The skeleton:

```python
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([
    CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
    "--force-device-scale-factor=2",          # 2160×2700 output, retina-sharp
    "--window-size=1080,1350",
    "--virtual-time-budget=6000",             # MANDATORY — else Cyrillic renders as serif
    "--run-all-compositor-stages-before-draw",# MANDATORY — else webfonts miss the frame
    f"--screenshot={png}", str(html_path),
], check=True, capture_output=True)
```

Non-negotiables for this backend:

- **Both Chrome flags** (`--virtual-time-budget=6000`, `--run-all-compositor-stages-before-draw`). Without them Google Fonts don't land and Ukrainian text drops to a serif fallback. Always open the PNG and confirm the Cyrillic before shipping.
- **Photo goes in as base64**, never a file path — `file://` images are flaky in headless. Source: `~/.claude/skills/infographic/assets/avatar.png`.
- **Bowtie mark is inline SVG** (see `BOWTIE` in the reference), not an image asset.
- **Brand tokens are declared once at the top** of the script as Python constants, copied from `victorshulga-design-system/index.html`. Never hardcode hexes inline in the CSS string.
- `html,body{{width:1080px;height:1350px;overflow:hidden}}` — fix the canvas, don't let content grow it. If a row list overflows, shrink the row height, don't let Chrome scroll.
- Same brand rules as Figma: white BG, rubric chip on top, ALL-CAPS centered title, white text on coral highlight, footer with photo + FRACTIONAL CRO pill left / bowtie + victorshulga.com right.

## Recipe: LADDER (ranked tiers, HTML/Chrome)

A vertical staircase of 4-7 rows. Row 1 sits at the top, full coral; each next row indents right and fades. Reads as "start at the top, not at the bottom".

Data shape — one tuple per row:

```python
# (queue number, name, state line, filled meter dots, background opacity, white text?)
ROWS = [
    ("1", "Амбасадор", "рекомендує вас іншим",       6, 1.00, True),
    ("2", "Клієнт",    "платить прямо зараз",        5, 0.82, True),
    ("3", "SQL",       "бачив пропозал, не купив",   4, 0.62, True),
    ("4", "MQL",       "був дзвінок, далі тиша",     3, 0.42, False),
    ("5", "Лід",       "є діалог, ще нічого не було",2, 0.24, False),
    ("6", "Проспект",  "холодний, про вас не чув",   1, 0.11, False),
]
```

Mechanics:

- **Staircase** = `margin-left: i * 30px` on row `i`. Keep 30px; more and the last row loses its meter column.
- **Fade** = `background: rgba(232,90,79,{opacity})` — the coral token in rgba form. Flip text to white for the top ~3 rows (opacity ≥ .6), ink below, so contrast holds both ways.
- **Meter** = 6 dots, `filled` at full opacity and the rest at `.22`, colored with the row's own text color. It gives a second read of the same ranking without a second axis.
- **Column headers** above the ladder (`Черга тесту` / `Траст`) in JetBrains Mono, uppercase, muted — they name the two axes in 4 words.
- **One black tag** (`сюди всі ллють тести`) pinned on the row that carries the tension. Exactly one, or the joke dies.
- **Rule band** at the bottom: ink card, coral `ПРАВИЛО` pill, one white sentence + one muted sentence. This is where the payoff line lives.
- Vertical coral arrow on the left, arrowhead UP, shaft at `.28` opacity — it says which direction the ladder is read.

Pitfalls specific to Ladder:

- Rows are `height:112px` with `gap:15px` for 6 rows. For 7 rows drop to 96px; for 4-5 rows go up to 130px rather than leaving dead space.
- The state line is the payload, not decoration — write it as an observable fact ("бачив пропозал, не купив"), never a category label.
- Don't put the coral highlight pill in the title AND keep row 1 full coral without checking the render — two solid coral masses stacked read as a bug.

## Recipe: TIMELINE ROWS (a process over time, HTML/Chrome)

Built 2026-08-31 for «Таймлайн запуску аутбаунду». Reference script:
`~/.claude/skills/infographic/assets/html-render/timeline-rows-reference.py` — runs as-is, produces that creative.

**Pick this over Ladder when** the rows are PERIODS, not ranks: the coral ramp reads as time passing and
results arriving, not as trust. Pick it over Vertical Steps when every period needs the SAME three columns
rather than its own bespoke band. The format exists to hold one specific tension: **what is being built
vs what the stakeholder actually sees**. If there is no such gap, this template is the wrong shape.

### Anatomy (top to bottom)

1. **Rubric chip** — centred, per the locked 7-pillar mapping. A launch/channel creative is
   «Мультиканальний аутріч» charcoal `#161513`, not GTM-strategy coral. Check the mapping, don't default.
2. **H1 + subheading** — the usual literal artifact name, CAPS, centred, line 2 in the coral pill.
3. **Source-card band** (`STREAMS`) — 3-5 cards, each `name` + coral caption + wrapped chip pills + a
   muted volume line pinned to the card bottom (`margin-top:auto`). This is the "where does the input
   come from" layer. Above it a mono eyebrow (`Звідки беремо ліди`).
4. **Two-column header** — left names the left columns, right names the right column.
5. **Rows** (`ROWS`) — one per period: badge (period label) · title + detail · optional stakeholder
   quote pill · right-hand "what they see" column. Background = `rgba(coral, op)` with `op` rising
   0.10 → 1.00 down the list; flip text to white from ~0.6 down.
6. **Rule band** — ink card, coral pill label, one factual sentence, one number chip pushed right
   with `margin-left:auto`.
7. Standard footer.

### Data shape

```python
# (name, caption, [source chips], volume line)
STREAMS = [("Сигнал", "коли писати", ["вакансії", "рух штату"], "3–5% бази в моменті"), ...]

# (period, what is built, detail, stakeholder quote or "", what they see, bg opacity, white text?)
ROWS = [("3–4", "База під сигнал і дозбір даних", "збираємо тих, у кого сигнал зараз",
         "де ліди?", "список компаній", 0.24, False), ...]
```

### Rules that this template is actually about

- **The right column holds ANSWERS, not labels.** «слайди й таблиці», «список компаній»,
  «зустрічі в календарі» — things a person could point at. One-word abstractions
  («порожньо», «потік») fail the column's own question and Viktor rejects them on sight.
- **Quote pills are white with ink text on every row**, coral `CEO`-style tag inside; exactly ONE row
  gets the ink/white inverted pill and that row carries the creative's tension. Outlined or
  translucent quote pills over a coral ramp are unreadable — this was the first thing rejected.
- **Leave one row without a quote.** Six pills in a column reads as a form, not as a voice.
- **The rule band states a fact from the table above it**, not a summary of the idea. «Зустрічі
  зʼявляються на тижні 7» passes; «Перші шість тижнів оплачують шар даних» is an image and was
  rejected as AI-speak.

### Height budgeting (the loop you will run 3-4 times)

Rows are the shock absorber. Everything else is fixed, so: render → measure the white gap between the
last row and the rule band → add `gap / 6` to `.row height` → re-render. A 5-card source band with
wrapping pills is ~135px; a 4-card band is ~115px and rows grow to ~104px to compensate. Chip pills at
`font-size:11.5px` fit roughly 2 per 159px card column and 2-3 per 234px column — dropping a card
changes the wrap and therefore the whole budget.

Card width also decides the source format: at 4 cards (~234px) pills work; at 5 cards (~185px) they
wrap one-per-line and a plain `·`-separated text line reads better.

### Run the copy through the detector before shipping

Creative copy is post copy. Dump every string into a `.md` and run
`anticopywriting-ai/scripts/detect.py --lang uk --mode post`. Real hits found this way: em dashes in
the rule band (`сигнал — коли писати` → `сигнал: коли писати`), and the word «тиша» for absent replies
(ban #12). Two hits are ARTIFACTS of flattening a table into prose — `rule_of_three` fires when list
rows land as consecutive short fragments (prefix them with `→` in the dump), and `throat_clear` always
fires on the H1 because the brand rule requires a literal artifact name there. Neither is a real defect.

## Brand reference (memorize)

**Foundations file**: `https://www.figma.com/design/ngweiN07cnXQo8zjRMfbZI`
**Plan key (Viktor)**: `<your Figma plan key>`
**Format**: 1080×1350 (4:5 portrait)

**Palette** (always 0-1 range):
- BG `{r:1, g:1, b:1}` white
- Text `{r:22/255, g:21/255, b:19/255}` ink `#161513`
- Coral `{r:232/255, g:90/255, b:79/255}` `#E85A4F` for highlights / accent markers
- Forest `{r:45/255, g:90/255, b:74/255}` `#2D5A4A` for positive callouts ONLY
- Border `{r:0.92, g:0.92, b:0.92}` light grey for card/row dividers

**Typography**: Inter — `Extra Bold`, `Semi Bold`, `Regular` (with space in style names).

**TITLE RULES (brand-wide, every post — infographic AND carousel):**
- Main title is **ALL CAPS** and **CENTERED** (not left-aligned).
- **TITLE TEST — run this BEFORE building anything.** The H1 answers **«ЩО ЦЕ ЗА ДОКУМЕНТ?»** (what IS this artifact), never «what is the main point». Formula: **`<artifact type> + <subject>`** — «Калькулятор потужності аутріча», «Карта GTM-системи», «9 місяців студії Gavan Fitness», «24 скіли для Claude Code». Three auto-reject checks — if ANY fires, the title is a hook, rewrite it:
  1. the H1 would work as the post's opening line (a scroll-stopper) → hook
  2. the H1 carries a result or a promise-number («10 зустрічей на місяць», «$3 093», «83% бюджету») → hook
  3. the H1 asks a question or promises an answer («що для цього треба», «як це працює») → hook
  The example figure and the thesis go in the SUBHEADING under the H1 («Приклад: 10 зустрічей на місяць»). A number stays in the H1 only when the number IS the subject («9 місяців», «24 скіли»).
  Rejected 2026-08-12 in one session: «БЮДЖЕТ АУТБАУНДУ НА МІСЯЦЬ $3 093», «10 ЗУСТРІЧЕЙ НА МІСЯЦЬ / ЩО ДЛЯ ЦЬОГО ТРЕБА». Approved: «КАЛЬКУЛЯТОР ПОТУЖНОСТІ / АУТРІЧА».
- **The H1 names the creative's subject LITERALLY — it is not the punch, the insight, or the post's thesis.** Viktor rejects metaphorical and clever headlines on sight ("знову назва відстій"). Write what the image IS: «Аутріч на сигналах», «9 місяців студії Gavan Fitness», «10 джерел для аутріча». The insight lives in the rubric chip, the subheading, or the post body — never in the H1. Corollary: a number in the H1 must appear somewhere in the image; don't headline a figure the reader can't find. Default shape for recurring/report creatives: `<what it is> + <period/number>`. (Rule 8a in `feedback_writing_bans`.)
- **Headline SHAPE is fixed (canon: design system §16 cover + the «Новий офер тестують / НЕ НА ХОЛОДНИХ» creative):** two lines — line 1 plain ink, line 2 SHORTER and wrapped in the coral pill with white text. Never the whole headline in one coral slab; never a coral-colored word instead of the pill; never a pill on the longer line. If the title is one line, it stays plain ink and the pill is skipped.
- Any **coral-highlight pill** has **WHITE text** (never charcoal). `makeHL` already does this.
- Section sub-labels are centered too. (See [[feedback_infographic_caps_title]].)

**Image asset hash** (must be uploaded to new file first):
- Avatar (Viktor's photo on coral disc, 1080×1080): `ea444ff18bbcd12290653fdf4d261e16949fc0d9`

The brand mark in the footer is now a **bowtie on a coral square drawn as vectors** (`makeBowtieSquare`) — NO wordmark image needed. Footer = `makeAuthor` (photo + name + FRACTIONAL CRO pill) left, `makeWordmark` (bowtie mark + victorshulga.com) right. This replaced the old dead-brand globe wordmark + founder line.

**Source PNG**:
- `~/.claude/skills/infographic/assets/avatar.png`

## Workflow

### Step 1 — Classify + plan structure

Pick template based on content shape (decision tree above), then pick the **render backend** (Figma vs HTML/Chrome — see the table above) and state which one you're using. Steps 2-4 below are the Figma path; for the HTML path copy `assets/html-render/ladder-reference.py` into the post folder, edit the data list, run it, and inspect the PNG. For Comparison Table: identify the comparison axis (2 columns vs 3), category rows, and bullets per cell. For Step Grid: identify step count (best is 9 = 3×3, but also 6 = 2×3 or 12 = 3×4).

For Custom builds: outline the structure to Viktor as bullet points, get confirmation before starting, then build inline using same atom builders.

### Step 2 — Create new Figma file

```
whoami → planKey "<your Figma plan key>"
create_new_file → editorType="design", fileName="[topic] — Infographic"
```

### Step 3 — Upload brand image (MANDATORY)

Skip → avatar fails silently. Only the avatar photo is uploaded now (bowtie mark is vector-drawn).

```
upload_assets fileKey=<new_file_key> count=1
```

Then POST the avatar PNG via Bash:
```bash
curl -s -X POST -F "file=@~/.claude/skills/infographic/assets/avatar.png" "<submitUrl_1>"
```

Auto-creates 1 placeholder frame — delete it in Step 4.

### Step 4 — Build infographic (single use_figma call)

Clear placeholder frames, load fonts, build the chosen template. Use the recipes below.

## Atom builders (shared across templates)

```js
const C = {
  bg:     { r: 1,       g: 1,       b: 1       },
  text:   { r: 22/255,  g: 21/255,  b: 19/255  },   // ink #161513
  coral:  { r: 232/255, g: 90/255,  b: 79/255  },   // #E85A4F
  forest: { r: 45/255,  g: 90/255,  b: 74/255  },   // #2D5A4A

  border: { r: 0.92,    g: 0.92,    b: 0.92    },
};
const PAINT = (c) => ({ type: "SOLID", color: c });
const IMG = {
  avatar:   "ea444ff18bbcd12290653fdf4d261e16949fc0d9",
};

// Bowtie brand mark — APPROVED victorshulga.com symbol: coral rounded square,
// two ROUNDED white wings (stroke-linejoin round) + charcoal center node.
// Geometry 1:1 with victor-logo/assets/favicon.svg (viewBox 100). Vector-drawn, no image.
// NODE = { r:28/255, g:28/255, b:30/255 } (#1C1C1E, matches favicon geometry).
function makeBowtieSquare(size = 52) {
  const k = size / 100;
  const NODE = { r: 28/255, g: 28/255, b: 30/255 };
  const sq = figma.createFrame();
  sq.name = "Bowtie mark"; sq.resize(size, size);
  sq.cornerRadius = size * 0.22; sq.fills = [PAINT(C.coral)]; sq.clipsContent = true;
  const wing = (pts) => {                       // pts in 0–100 viewBox coords
    const sp = pts.map(p => [p[0]*k, p[1]*k]);
    const mnX = Math.min(...sp.map(p=>p[0])), mnY = Math.min(...sp.map(p=>p[1]));
    const v = figma.createVector();
    v.vectorPaths = [{ windingRule: "NONZERO", data: "M " + sp.map(p => (p[0]-mnX) + " " + (p[1]-mnY)).join(" L ") + " Z" }];
    v.fills = [PAINT(C.bg)]; v.strokes = [PAINT(C.bg)]; v.strokeWeight = 11*k; v.strokeJoin = "ROUND";
    sq.appendChild(v); v.x = mnX; v.y = mnY;
  };
  wing([[14,24],[46,50],[14,76]]);              // left wing
  wing([[86,24],[54,50],[86,76]]);              // right wing
  const dot = figma.createEllipse(); const r = 7.5*k;
  dot.resize(r*2, r*2); dot.x = 50*k - r; dot.y = 50*k - r;
  dot.fills = [PAINT(NODE)]; sq.appendChild(dot);
  return sq;
}

// Right footer cluster — bowtie mark + victorshulga.com. Self-positions bottom-right
// (ignores passed x; right margin 60). Keep the makeWordmark name for call-site compatibility.
function makeWordmark(parent, x, y, scale = 1) {
  const ab = figma.createAutoLayout("HORIZONTAL", { itemSpacing: 12 });
  ab.fills = []; ab.counterAxisAlignItems = "CENTER";
  ab.appendChild(makeBowtieSquare(52));
  const d = figma.createText();
  d.fontName = { family: "Inter", style: "Semi Bold" };
  d.characters = "victorshulga.com"; d.fontSize = 19;
  d.fills = [PAINT(C.coral)]; ab.appendChild(d);
  parent.appendChild(ab);
  ab.x = 1080 - ab.width - 60; ab.y = y; return ab;
}

// Author block — real photo (coral ring) + name + "FRACTIONAL CRO" coral pill.
function makeAuthor(parent, x, y) {
  const ab = figma.createAutoLayout("HORIZONTAL", { itemSpacing: 16 });
  ab.fills = []; ab.counterAxisAlignItems = "CENTER";
  const av = figma.createEllipse(); av.resize(72, 72);
  av.fills = [{ type: "IMAGE", imageHash: IMG.avatar, scaleMode: "FILL" }];
  av.strokes = [PAINT(C.coral)]; av.strokeWeight = 3;
  ab.appendChild(av);
  const s = figma.createAutoLayout("VERTICAL", { itemSpacing: 8 });
  s.fills = []; ab.appendChild(s);
  const n = figma.createText();
  n.fontName = { family: "Inter", style: "Extra Bold" };
  n.characters = "Victor Shulga"; n.fontSize = 24;
  n.fills = [PAINT(C.text)]; s.appendChild(n);
  const pill = figma.createAutoLayout("HORIZONTAL", { paddingTop: 6, paddingBottom: 6, paddingLeft: 12, paddingRight: 12 });
  pill.fills = [PAINT(C.coral)]; pill.cornerRadius = 8; s.appendChild(pill);
  const r = figma.createText();
  r.fontName = { family: "Inter", style: "Semi Bold" };
  r.characters = "FRACTIONAL CRO"; r.fontSize = 14;
  r.letterSpacing = { unit: "PERCENT", value: 8 };
  r.fills = [PAINT(C.bg)]; pill.appendChild(r);   // WHITE on coral (brand rule)
  ab.x = x; ab.y = y; parent.appendChild(ab); return ab;
}

function makeHL(text, fontSize, pad = {t:6,b:6,l:16,r:16}) {
  const w = figma.createAutoLayout("HORIZONTAL", {
    itemSpacing: 0, paddingTop: pad.t, paddingBottom: pad.b, paddingLeft: pad.l, paddingRight: pad.r
  });
  w.fills = [PAINT(C.coral)];
  const t = figma.createText();
  t.fontName = { family: "Inter", style: "Extra Bold" };
  t.characters = text; t.fontSize = fontSize;
  t.fills = [PAINT(C.bg)]; w.appendChild(t);   // WHITE text on coral highlight (brand rule)
  return w;
}

function makeFrame(name) {
  const f = figma.createFrame();
  f.name = name; f.resize(1080, 1350);
  f.fills = [PAINT(C.bg)]; f.clipsContent = true;
  f.x = 100; f.y = 100; return f;
}

// Absolutely-positioned text helper (charts position by x/y, NOT auto-layout).
// align: "LEFT" | "CENTER" | "RIGHT". width needed only for CENTER/RIGHT.
function makeText(parent, str, x, y, size, style, color, align = "LEFT", width = null) {
  const t = figma.createText();
  t.fontName = { family: "Inter", style };
  t.characters = str; t.fontSize = size;
  t.fills = [PAINT(color)];
  parent.appendChild(t);
  if (align !== "LEFT" && width) {
    t.textAlignHorizontal = align;
    t.resize(width, t.height);
    t.x = x; t.y = y;
  } else {
    t.x = x; t.y = y;
  }
  return t;
}
```

## Chart palette — slice colors

Charts need 4-6 distinguishable fills but the brand only has coral + charcoal + forest. Use this fixed ramp (brand-pure, no pastels) so every donut/funnel reads the same:

```js
const RAMP = [
  C.coral,                                  // 1 — primary
  C.text,                                   // 2 — charcoal
  C.forest,                                 // 3 — forest
  { r: 200/255, g: 70/255,  b: 60/255 },    // 4 — coral deep
  { r: 194/255, g: 188/255, b: 180/255 },   // 5 — warm grey
  { r: 122/255, g: 100/255, b: 96/255 },    // 6 — taupe
];
```

Rule: the **most important slice is always coral (RAMP[0])**. Warm grey/taupe carry the "rest" or low-priority slices. Never invent new hues.

## Chart atom builders

```js
// ---- DONUT / PIE ----
// segs = [{value, color}]. innerRatio 0.55 = donut, 0 = pie. Start at 12 o'clock, clockwise.
// gap = small radians between slices (0.018 looks clean; 0 = touching).
function makeDonut(parent, cx, cy, diameter, segs, innerRatio = 0.55, gap = 0.018) {
  const total = segs.reduce((s, x) => s + x.value, 0);
  const r = diameter / 2;
  let a = -Math.PI / 2;
  for (const seg of segs) {
    const sweep = (seg.value / total) * Math.PI * 2;
    const e = figma.createEllipse();
    e.resize(diameter, diameter);
    e.x = cx - r; e.y = cy - r;
    e.fills = [PAINT(seg.color)];
    e.arcData = { startingAngle: a + gap / 2, endingAngle: a + sweep - gap / 2, innerRadius: innerRatio };
    parent.appendChild(e);
    a += sweep;
  }
}

// Center label for a donut (big number + small caption). cx/cy = donut center.
function makeDonutCenter(parent, cx, cy, big, small) {
  makeText(parent, big, cx - 100, cy - 38, 46, "Extra Bold", C.text, "CENTER", 200);
  if (small) makeText(parent, small, cx - 100, cy + 14, 20, "Regular", C.text, "CENTER", 200);
}

// Legend: stacked rows of [swatch] label .......... value. Returns nothing.
// items = [{label, value, color}]. x/y = top-left, w = total width.
function makeLegend(parent, x, y, w, items, rowH = 44) {
  items.forEach((it, i) => {
    const yy = y + i * rowH;
    const sw = figma.createRectangle();
    sw.resize(22, 22); sw.cornerRadius = 4; sw.x = x; sw.y = yy;
    sw.fills = [PAINT(it.color)]; parent.appendChild(sw);
    makeText(parent, it.label, x + 34, yy + 1, 22, "Semi Bold", C.text);
    if (it.value != null) makeText(parent, String(it.value), x, yy + 1, 22, "Extra Bold", C.text, "RIGHT", w);
  });
}

// ---- FUNNEL ----
// tiers = [{label, sub, color, dark}]. Narrows top→bottom. cx = horizontal center.
function makeFunnel(parent, cx, topY, maxW, minW, tierH, tierGap, tiers) {
  const n = tiers.length;
  let y = topY;
  tiers.forEach((tier, i) => {
    const topW = maxW - (maxW - minW) * (i / n);
    const botW = maxW - (maxW - minW) * ((i + 1) / n);
    const inset = (topW - botW) / 2;
    const v = figma.createVector();
    v.vectorPaths = [{ windingRule: "NONZERO",
      data: `M 0 0 L ${topW} 0 L ${topW - inset} ${tierH} L ${inset} ${tierH} Z` }];
    v.fills = [PAINT(tier.color)]; v.strokes = [];
    parent.appendChild(v);
    v.x = cx - topW / 2; v.y = y;
    // white label centered on the narrow (bottom) width so it never overflows
    makeText(parent, tier.label, cx - botW / 2, y + tierH / 2 - 18, 26, "Extra Bold", C.bg, "CENTER", botW);
    if (tier.sub) makeText(parent, tier.sub, cx + topW / 2 + 24, y + tierH / 2 - 13, 21, "Regular", C.text);
    y += tierH + tierGap;
  });
}

// ---- GROWTH CURVE ----
// Draw an upward bezier with milestone dots. pathD = bezier string in FRAME coords.
// dots = [{x, y, label, big}]. baselineY = x-axis y, x0/x1 = axis extent.
function makeCurve(parent, pathD, baselineY, x0, x1, dots, areaD = null) {
  if (areaD) {
    const area = figma.createVector();
    area.vectorPaths = [{ windingRule: "NONZERO", data: areaD }];
    area.fills = [{ type: "SOLID", color: C.coral, opacity: 0.12 }]; area.strokes = [];
    parent.appendChild(area); area.x = 0; area.y = 0;
  }
  const line = figma.createVector();
  line.vectorPaths = [{ windingRule: "NONE", data: pathD }];
  line.strokes = [PAINT(C.coral)]; line.strokeWeight = 5; line.strokeCap = "ROUND";
  line.fills = []; parent.appendChild(line); line.x = 0; line.y = 0;
  // baseline (thin rect, not createLine — easier to position)
  const ax = figma.createRectangle();
  ax.x = x0; ax.y = baselineY - 1.5; ax.resize(x1 - x0, 3); ax.fills = [PAINT(C.text)];
  parent.appendChild(ax);
  for (const d of dots) {
    const e = figma.createEllipse();
    const rad = d.big ? 11 : 9;
    e.resize(rad * 2, rad * 2); e.x = d.x - rad; e.y = d.y - rad;
    e.fills = [PAINT(d.big ? C.coral : C.text)]; parent.appendChild(e);
    if (d.label) makeText(parent, d.label, d.x - 80, d.y + 22, 19, "Semi Bold", d.big ? C.coral : C.text, "CENTER", 160);
  }
}

// ---- TIMELINE (1 axis) ----
// zones = [{from,to,color,label,dark}] (fractions 0..1, drawn below axis).
// ticks = [{at,label}] (fraction, label above axis). axisY, x0/x1 in frame coords.
function makeTimeline(parent, x0, x1, axisY, zones, ticks) {
  const W = x1 - x0;
  for (const z of zones) {
    const r = figma.createRectangle();
    r.x = x0 + z.from * W; r.y = axisY + 16; r.resize((z.to - z.from) * W, 60);
    r.cornerRadius = 6; r.fills = [PAINT(z.color)]; parent.appendChild(r);
    makeText(parent, z.label, x0 + z.from * W, axisY + 16 + 30 - 13, 21, "Semi Bold",
      z.dark ? C.bg : C.text, "CENTER", (z.to - z.from) * W);
  }
  const ax = figma.createRectangle();
  ax.x = x0; ax.y = axisY - 1.5; ax.resize(W, 3); ax.fills = [PAINT(C.text)]; parent.appendChild(ax);
  // arrowhead at the right end
  const arr = figma.createVector();
  arr.vectorPaths = [{ windingRule: "NONZERO", data: "M 0 0 L 18 9 L 0 18 Z" }];
  arr.fills = [PAINT(C.text)]; arr.strokes = []; parent.appendChild(arr);
  arr.x = x1; arr.y = axisY - 9;
  for (const tk of ticks) {
    const tx = x0 + tk.at * W;
    const t = figma.createRectangle();
    t.x = tx - 1; t.y = axisY - 16; t.resize(2, 16); t.fills = [PAINT(C.text)]; parent.appendChild(t);
    makeText(parent, tk.label, tx - 130, axisY - 54, 20, "Semi Bold", C.text, "CENTER", 260);
  }
}
```

## Chart atom builders — v2 (diagram elements)

Brand-recolored diagram atoms — use these to put a real graphic in EVERY block, not just text. All brand-pure (coral + tints + forest + charcoal); no pastels. `GREY` = the neutral dot/track shade.

```js
const GREY = { r: 0.85, g: 0.82, b: 0.79 };
const TRACK = { r: 0.93, g: 0.92, b: 0.90 };
const AXIS = { r: 0.79, g: 0.76, b: 0.73 };

// ---- CONCENTRIC CIRCLES (complexity layers / "narrow to your niche") ----
// Nested filled coral circles, opacity rising toward the solid centre.
function makeConcentric(parent, cx, cy, maxR, layers = 4) {
  for (let i = 0; i < layers; i++) {
    const r = maxR * (1 - i / layers);
    const e = figma.createEllipse(); e.resize(r * 2, r * 2); e.x = cx - r; e.y = cy - r;
    const op = i === layers - 1 ? 1 : 0.13 + i * (0.87 / (layers - 1));
    e.fills = [{ type: "SOLID", color: C.coral, opacity: op }];
    parent.appendChild(e);
  }
}

// ---- 2×2 QUADRANT / MATRIX (positioning map) ----
// dots = [{fx, fy, color}] with fx/fy in 0..1 (position inside the box).
function makeQuadrant(parent, x, y, w, h, dots) {
  const bg = figma.createRectangle(); bg.x = x; bg.y = y; bg.resize(w, h); bg.cornerRadius = 6;
  bg.fills = [{ type: "SOLID", color: C.coral, opacity: 0.06 }]; parent.appendChild(bg);
  const vx = figma.createRectangle(); vx.resize(2, h); vx.x = x + w / 2 - 1; vx.y = y; vx.fills = [PAINT(AXIS)]; parent.appendChild(vx);
  const hx = figma.createRectangle(); hx.resize(w, 2); hx.x = x; hx.y = y + h / 2 - 1; hx.fills = [PAINT(AXIS)]; parent.appendChild(hx);
  for (const d of dots) {
    const e = figma.createEllipse(); e.resize(14, 14); e.x = x + d.fx * w - 7; e.y = y + d.fy * h - 7;
    e.fills = [PAINT(d.color || C.coral)]; parent.appendChild(e);
  }
}

// ---- HUB & SPOKES (1 centre → N attributes, e.g. ICP / committee) ----
function makeHubSpokes(parent, cx, cy, radius, n) {
  let d = ""; const pts = [];
  for (let i = 0; i < n; i++) {
    const a = -Math.PI / 2 + i * 2 * Math.PI / n;
    const px = cx + radius * Math.cos(a), py = cy + radius * Math.sin(a);
    pts.push([px, py]); d += `M ${cx} ${cy} L ${px} ${py} `;
  }
  const spokes = figma.createVector(); spokes.vectorPaths = [{ windingRule: "NONE", data: d }];
  spokes.strokes = [PAINT(AXIS)]; spokes.strokeWeight = 2; spokes.fills = []; parent.appendChild(spokes); spokes.x = 0; spokes.y = 0;
  for (const [px, py] of pts) {
    const e = figma.createEllipse(); e.resize(16, 16); e.x = px - 8; e.y = py - 8;
    e.fills = [PAINT(C.bg)]; e.strokes = [PAINT(C.coral)]; e.strokeWeight = 2; parent.appendChild(e);
  }
  const ctr = figma.createEllipse(); ctr.resize(26, 26); ctr.x = cx - 13; ctr.y = cy - 13; ctr.fills = [PAINT(C.coral)]; parent.appendChild(ctr);
}

// ---- DOT GRID (population / segment share) ----
function makeDotGrid(parent, x, y, cols, rows, gap, dotR, filled) {
  let n = 0;
  for (let r = 0; r < rows; r++) for (let c = 0; c < cols; c++) {
    const e = figma.createEllipse(); e.resize(dotR * 2, dotR * 2); e.x = x + c * gap; e.y = y + r * gap;
    e.fills = [PAINT(n < filled ? C.coral : GREY)]; parent.appendChild(e); n++;
  }
}

// ---- SCORE / PROGRESS RING ----
// pct 0..1. Grey track ring + coral progress arc + centre number.
function makeScoreRing(parent, cx, cy, r, pct, big) {
  const inner = (r - 11) / r;                       // ~11px ring band
  const disk = figma.createEllipse(); disk.resize(r * 2, r * 2); disk.x = cx - r; disk.y = cy - r;
  disk.fills = [PAINT(TRACK)]; parent.appendChild(disk);
  const hole = figma.createEllipse(); const hr = r * inner;
  hole.resize(hr * 2, hr * 2); hole.x = cx - hr; hole.y = cy - hr; hole.fills = [PAINT(C.bg)]; parent.appendChild(hole);
  const arc = figma.createEllipse(); arc.resize(r * 2, r * 2); arc.x = cx - r; arc.y = cy - r;
  arc.fills = [PAINT(C.coral)];
  arc.arcData = { startingAngle: -Math.PI / 2, endingAngle: -Math.PI / 2 + pct * Math.PI * 2, innerRadius: inner };
  parent.appendChild(arc);
  if (big) makeText(parent, big, cx - 50, cy - 14, 22, "Extra Bold", C.text, "CENTER", 100);
}

// ---- BAR CHART (axis + rising coral opacity ramp) ----
// bars = [{label, h}] h in px. Grounds bars on an L-axis like the offer ladder.
function makeBarChart(parent, x0, baseY, bars, barW = 44, gap = 14) {
  const top = baseY - Math.max(...bars.map(b => b.h)) - 6;
  const ay = figma.createRectangle(); ay.resize(2, baseY - top); ay.x = x0 - 2; ay.y = top; ay.fills = [PAINT(AXIS)]; parent.appendChild(ay);
  const ax = figma.createRectangle(); ax.resize(bars.length * (barW + gap) + 6, 2); ax.x = x0 - 2; ax.y = baseY; ax.fills = [PAINT(AXIS)]; parent.appendChild(ax);
  bars.forEach((b, i) => {
    const x = x0 + i * (barW + gap);
    const rect = figma.createRectangle(); rect.resize(barW, b.h); rect.x = x; rect.y = baseY - b.h; rect.cornerRadius = 6;
    rect.fills = [{ type: "SOLID", color: C.coral, opacity: 0.45 + i * (0.55 / Math.max(1, bars.length - 1)) }];
    parent.appendChild(rect);
    if (b.label) makeText(parent, b.label, x - 5, baseY + 6, 12, "Semi Bold", C.grey, "CENTER", barW + 10);
  });
}
```

**Improved FUNNEL ramp:** in `makeFunnel`, use opacity ramp `1 → 0.7 → 0.5` on coral tiers and make the LAST tier `C.forest` (the convert / positive stage). Keeps it brand and reads as "narrowing to the win".

**Which element per intent:** proportion → Donut; share of a population → DotGrid; narrowing stages → Funnel; change over time → Curve; magnitude/ranking → BarChart; "focus to the niche" / complexity layers → Concentric; positioning / two axes → Quadrant; one hub → many attributes (ICP, committee) → HubSpokes; a single metric/score → ScoreRing; two opposed states on an axis → Timeline.

## Icon library + icon-tiles

31 brand line icons live as SVG files in `assets/icons/` (24-grid, stroke 2, round caps, charcoal). The **icon-tile** — rounded coral-tint square + line icon + label — is the core list element: use it in ROWS for "channels / ways / list" content (e.g. lead-gen channels, content formats, outbound tactics) instead of plain text pills. Preview all 31 at `assets/icons/preview.html`.

**Icon-map (card theme → icon name):**

| Theme | icon | Theme | icon |
|---|---|---|---|
| ICP / ideal customer | `icp` | podcast | `podcast` |
| target / niche / bullseye | `target` | short video / video | `video` |
| funnel / stages | `funnel` | webinar / group call | `webinar` |
| offer / pricing / deal-tag | `offer` | newsletter | `newsletter` |
| growth / trajectory | `growth` | community | `community` |
| outbound / send | `outbound` | thought leadership / idea | `insight` |
| inbound / attract | `inbound` | industry report | `report` |
| positioning / 2×2 | `positioning` | cold email | `email` |
| warning / risk / mistake | `warning` | DM / chat | `dm` |
| buying signal / intent | `signal` | phone / cold call | `phone` |
| lead / new contact | `lead` | LinkedIn | `linkedin` |
| case study / proof | `case-study` | website form | `website-form` |
| revenue / money | `revenue` | lead magnet / ebook | `lead-magnet` |
| pipeline / stages board | `pipeline` | booked meeting / calendar | `meeting` |
| score / rating | `score` | won deal / trophy | `win` |
| timing / speed | `clock` | | |

**Getting an icon into Figma:** the Figma plugin can't read the filesystem, so **inline the SVG string**. Copy the entries you need from `assets/icons/icons.js` (a `const ICONS = { name: "<svg…>" }` map) into the top of your `use_figma` script, then `figma.createNodeFromSvg(ICONS.podcast)`. `currentColor` does NOT resolve on import — the tile builder recolors every stroke after import.

```js
// ICON-TILE — tint square + recolored line icon + centered label.
// svgStr = ICONS[name]; accent=true → coral icon, else charcoal.
function makeIconTile(parent, x, y, svgStr, label, opts = {}) {
  const s = opts.size || 72, accent = !!opts.accent;
  const sq = figma.createRectangle(); sq.resize(s, s); sq.x = x; sq.y = y; sq.cornerRadius = 18;
  sq.fills = [{ type: "SOLID", color: C.coral, opacity: 0.10 }]; parent.appendChild(sq);
  const ic = figma.createNodeFromSvg(svgStr);
  const g = s * 0.5; ic.resize(g, g); ic.x = x + (s - g) / 2; ic.y = y + (s - g) / 2;
  ic.findAll(n => "strokes" in n && n.strokes.length).forEach(n => n.strokes = [PAINT(accent ? C.coral : C.text)]);
  ic.findAll(n => "fills" in n && Array.isArray(n.fills) && n.fills.length && n.type !== "FRAME")
    .forEach(n => n.fills = [PAINT(accent ? C.coral : C.text)]);   // recolor filled dots too
  parent.appendChild(ic);
  if (label) makeText(parent, label, x - 12, y + s + 8, 14, "Semi Bold", C.text, "CENTER", s + 24);
}

// ROW of icon-tiles, auto-spaced. items = [{icon:"podcast", label:"Podcast"}, ...]
function makeIconRow(parent, x, y, items, opts = {}) {
  const s = opts.size || 72, gap = opts.gap || 28;
  items.forEach((it, i) => makeIconTile(parent, x + i * (s + gap), y, ICONS[it.icon], it.label, { size: s, accent: it.accent }));
}
```

**Rules:** one row = 3-6 tiles (wrap to a second row beyond 6). Keep tiles charcoal by default; set `accent:true` on at most one tile per row (the "punch"), per the one-accent-per-card rule. Tile label ≤ 2 words. To build a "canvas of channels" (e.g. Demand Gen icon grid), stack 2-3 `makeIconRow` bands under a section header.

## Recipe: DONUT / PIE

Inputs: `titleParts`, `subheading`, `slices` = `[{label, value, color}]` (4-6, sorted desc, most important = coral). Layout: donut left, legend right.

```js
const frame = makeFrame("Infographic / Donut");
figma.currentPage.appendChild(frame);
buildTitle(frame, titleParts, subheading);          // see "Shared title block" below

const cx = 320, cy = 560, dia = 300;
makeDonut(frame, cx, cy, dia, slices.map(s => ({ value: s.value, color: s.color })));
const totalLabel = String(slices.reduce((a, s) => a + s.value, 0));
makeDonutCenter(frame, cx, cy, totalLabel, "разом");
makeLegend(frame, 560, 470, 460,
  slices.map(s => ({ label: s.label, value: s.value, color: s.color })));

makeAuthor(frame, 60, 1350 - 72 - 60);
makeWordmark(frame, 1080 - 180 - 60, 1350 - 60 - 60);
```

## Recipe: FUNNEL

Inputs: `titleParts`, `subheading`, `tiers` = `[{label, sub, color, dark}]` (3-5, top→bottom). Use coral → coral-deep → charcoal for a 3-tier; keep `dark:true` only if text legibility needs it.

```js
const frame = makeFrame("Infographic / Funnel");
figma.currentPage.appendChild(frame);
buildTitle(frame, titleParts, subheading);

makeFunnel(frame, 460, 440, 600, 220, 130, 14, tiers);

makeAuthor(frame, 60, 1350 - 72 - 60);
makeWordmark(frame, 1080 - 180 - 60, 1350 - 60 - 60);
```

## Recipe: GROWTH CURVE

Inputs: `titleParts`, `subheading`, plus you hand-author the bezier `pathD` and `dots` in frame coords. Keep the curve in the lower band (y ≈ 600-1180). Template values:

```js
const frame = makeFrame("Infographic / Growth Curve");
figma.currentPage.appendChild(frame);
buildTitle(frame, titleParts, subheading);

const x0 = 120, x1 = 960, baseY = 1180;
const pathD = `M 140 1170 C 380 1162 440 1060 580 1000 S 840 880 940 840`;
const areaD = `M 140 1170 C 380 1162 440 1060 580 1000 S 840 880 940 840 L 940 1180 L 140 1180 Z`;
const dots = [
  { x: 360, y: 1095, label: "Тиж 1" },
  { x: 620, y: 970,  label: "Тиж 6" },
  { x: 938, y: 842,  label: "10K", big: true },
];
makeCurve(frame, pathD, baseY, x0, x1, dots, areaD);

makeAuthor(frame, 60, 1350 - 72 - 60);
makeWordmark(frame, 1080 - 180 - 60, 1350 - 60 - 60);
```

Curve geometry is hand-tuned — **screenshot after building and nudge `pathD`/`dots` once** so dots sit on the line and the rise feels like growth (start shallow, end steep).

## Recipe: TIMELINE

Inputs: `titleParts`, `subheading`, `zones`, `ticks`. For a Reactive-vs-Proactive style (two contrasted rows), call `makeTimeline` twice with its own sub-heading + axisY (~520 and ~960). Single axis: one call (~640).

```js
const frame = makeFrame("Infographic / Timeline");
figma.currentPage.appendChild(frame);
buildTitle(frame, titleParts, subheading);

// Row 1 — e.g. "Reactive"
makeText(frame, "РЕАКТИВНО", 60, 420, 28, "Extra Bold", C.coral);
makeTimeline(frame, 120, 940, 520,
  [{ from: 0.08, to: 0.42, color: { r: 244/255, g: 180/255, b: 173/255 }, label: "немає інвестицій" },
   { from: 0.52, to: 0.92, color: C.coral, dark: true, label: "реклама + масові розсилки" }],
  [{ at: 0.1, label: "«не до маркетингу»" }, { at: 0.5, label: "«потрібні ліди вже!»" }, { at: 0.9, label: "«не працює!»" }]);

// Row 2 — e.g. "Proactive"
makeText(frame, "ПРОАКТИВНО", 60, 860, 28, "Extra Bold", C.forest);
makeTimeline(frame, 120, 940, 960,
  [{ from: 0.08, to: 0.42, color: { r: 180/255, g: 220/255, b: 200/255 }, label: "бренд + впізнаваність" },
   { from: 0.52, to: 0.92, color: C.forest, dark: true, label: "реклама + теплі листи" }],
  [{ at: 0.1, label: "«почнімо рано»" }, { at: 0.5, label: "«захопимо попит»" }, { at: 0.9, label: "«реінвестуймо»" }]);

makeAuthor(frame, 60, 1350 - 72 - 60);
makeWordmark(frame, 1080 - 180 - 60, 1350 - 60 - 60);
```

## Recipe: BLOCK GRID (dense N-card with a mini-visual per card)

This is the **flagship dense format** — a header + a 3-col grid of cards, where **every card carries its own little diagram**, not just text. Use it to condense a whole framework, playbook, or slide deck into one image. Built from a 9-card 3×3 GTM deck condensation.

**Density is the point.** A sparse 3-block layout reads as low-effort — Viktor rejected it. Aim for 6 (2×3) or 9 (3×3) cards, each = number badge + 1-2-line title + a compact mini-visual + optional micro-labels.

### Layout constants (1080×1350, 3 cols)

```js
const M=50, gap=16, cardW=316, cardH=337;           // 9-card 3×3
// card origins: x = M + col*(cardW+gap); y = 224 + row*(cardH+gap)
// header band: y 44–200 (title 2 lines + coral-hl pill + grey subtitle)
// footer: author at (50,1262), wordmark (150×75) at (880,1256)
// per card → badge disc 42 at (x+22,y+22) with centered white number;
//            title BESIDE the badge (not under it): x=x+78, top-aligned with the number,
//            width=218 (=cardW-78-20), 21px Extra Bold, wraps to ≤2 lines;
//            DESCRIPTOR: one ≤1-line grey explainer (16px, {88,88,94}, width 272, lineHeight 126%)
//              at (x+22, y+72) — full card width, BELOW the badge. Adds a teaching layer + fills
//              the space the raised title leaves (Viktor's call 2026-06-17). Keep it 1 line, punchy.
//            VISUAL REGION: vx=x+22, vy=y+150, vw=272, vh=165 (full card width)
```

For a 6-card 2×3, raise `cardH` to ~430 and start grid lower; the visual region grows to ~vh 250.

### Card shell + header

Build the skeleton in call 1 (frame, coral top bar, header, footer, 9× [bg rect radius18 + coral badge disc + white number + wrapped title]). Return `frame.id`. Then fill mini-visuals in 2 more calls (cards 1-5, then 6-9) — re-acquire the frame via `await figma.getNodeByIdAsync(frameId)`. Keep each call ≤ ~10 cards' worth of nodes. See the GTM build in session for the exact skeleton script.

### Mini-visual library (each draws inside `vx,vy,vw=272,vh=165`)

Pick the shape that fits each card's content. All use the `mt()` absolute-text helper and `P()`.

```js
// pill: rounded rect + centered label (vertical-centered)
function pill(f,x,y,w,h,fill,txt,tc,fs,style){
  const r=figma.createRectangle(); r.resize(w,h); r.x=x; r.y=y; r.cornerRadius=Math.min(h/2,22);
  r.fills=[P(fill)]; f.appendChild(r);
  mt(f,txt,x,y+(h-fs*1.25)/2,fs,style||"Semi Bold",tc,"CENTER",w);
}
```

- **narrowingPills** (focus / "pick a niche", block 1): 3 stacked pills decreasing width (272→206→140), top=grey "all", mid=charcoal, bottom=coral "your niche".
- **chipGrid 2×3** (a 6-part model like ICP, block 2): 6 chips, `chipW=85,gap8,chipH=68,rowgap10`; fill `{0.975,0.965,0.96}` + 1px border, 12px centered wrapped labels.
- **checkList + result** (qualification, block 3): N rows of [forest disc 24 + "✓" + 15px label], then a full-width coral result pill "= …".
- **ladderBars** (offer/value ladder, block 4): 4 ascending bars `w44,gap14`, heights `[44,74,102,130]`, coral with rising `opacity [.45,.65,.82,1]`, 12px grey labels under (Free/Low/Front/High). **Ground them on an L-axis** (vertical + horizontal grey 2px rects + small triangle arrowheads) with a rotated "Value" y-axis label (`text.rotation=90`, then set x/y) — bare floating bars look unfinished. Don't add an "Ціна →" x-title: the Free→High ticks + the axis arrow already convey price, and a right-side title collides with the tallest bar.
- **numberedRows** (value-prop / any ordered list, block 5): N rows of [coral disc 24 + white number + 15px label], rowH 30.
- **questionRows** (positioning, block 6): like numberedRows but disc shows "?" and labels are questions.
- **flowChips** (case study Проблема→Рішення→Результат, block 7): 3 stacked pills (charcoal→coral→forest) with "↓" arrows (18px grey) between.
- **vFunnel** (buyer journey, block 8): 5 stacked trapezoid vectors narrowing `maxW272→minW116`, `tierH26,gap4`, coral with falling opacity, **last tier forest** (the convert/decision stage), 12px white centered labels. Trapezoid: `M 0 0 L topW 0 L ${topW-inset} H L ${inset} H Z`, `inset=(topW-botW)/2`, place `v.x=cx-topW/2`.
- **quad2x2** (channels, block 9): 4 chips `130×66, gap12`, coral 15px bold title + 11px grey sub ("Email · LinkedIn").

### Block Grid pitfalls

- **Title ≤ 2 lines** at 21px/width 272 — shorten copy (drop filler words) so it never collides with the visual region at vy=y+150.
- **Mini-visuals are abstract, not literal** — chips/bars/dots/arrows, NOT detailed replicas of deck slides. The card is ~272×165; keep ≤6 elements and fonts ≥11px.
- **One accent per card max** — coral OR forest as the "punch" element, the rest charcoal/grey. Across 9 cards this keeps it brand-pure, not a coral mess.
- **Whitespace is fine** — a ladder/funnel that fills the lower half with empty top is OK; don't cram to fill.
- **Build in 3 calls** (skeleton → cards 1-5 → cards 6-9) and screenshot once at the end; nudge only what's off.
- **Redrawing a card = remove old nodes by GENEROUS geometric bounds, then redraw.** Mini-visual nodes (vectors, tall bars) can sit a few px ABOVE the card's visual region `vy` — a funnel's top tier or a 130px bar starts above `y+150`. Filter `frame.children` by `x∈[cardX-2, cardX+cardW]` and `y∈[titleBottom, cardBottom]` (start the y-window a bit ABOVE vy, e.g. `y+135`), not `y≥vy` — a tight window leaves a "ghost" tier behind (hit this on the GTM funnel: stray tier was at y≈1040 while the region check started at 1060). Return the removed nodes' y-values to confirm the sweep caught everything.

## Shared title block (charts)

Charts position by x/y, so they share one title helper instead of the auto-layout title used by text templates:

```js
function buildTitle(frame, titleParts, subheading) {
  // titleParts: [{text, highlight}]. CAPS, 56px, CENTERED (brand rule). Each part on its own line.
  let y = 80;
  for (const part of titleParts) {
    if (part.highlight) {
      const hl = makeHL(part.text, 56);                 // white text on coral
      frame.appendChild(hl); hl.y = y; hl.x = Math.round((1080 - hl.width) / 2);
    } else {
      makeText(frame, part.text, 0, y, 56, "Extra Bold", C.text, "CENTER", 1080);
    }
    y += 66;
  }
  if (subheading) makeText(frame, subheading, 0, y + 8, 22, "Regular", { r: 107/255, g: 107/255, b: 112/255 }, "CENTER", 1080);
}
// Title with an INLINE coral pill on the same line (e.g. "GTM-СТРАТЕГІЯ АГЕНЦІЇ [У 2026]"),
// centered as a row: create the plain text + pill text, measure widths, center the row.
// rowW = mainW + gap + (pillTextW + 2*padX); startX = (1080 - rowW)/2. Pill rect behind, white text on top.
```

Per the CAPS-title rule, chart headlines are UPPERCASE; section sub-labels (РЕАКТИВНО / ПРОАКТИВНО, etc.) are centered or left per layout.

## Recipe: COMPARISON TABLE (N rows × 2-3 cols)

Inputs you need from text:
- `titleParts`: array of `{text, highlight}` for headline parts (typically: plain + coral-highlighted phrase + plain)
- `subheading`: short string with → arrow
- `headers`: ["Category", "Weak/Bad header", "Strong/Good header"]
- `rows`: array of `{label, bullets1: [...], bullets2: [...]}` (3 bullets per cell ideal, 1-4 acceptable)

```js
const frame = makeFrame("Infographic / Comparison Table");
figma.currentPage.appendChild(frame);

// Title block
const tb = figma.createAutoLayout("VERTICAL", { itemSpacing: 12 });
tb.fills = []; tb.x = 60; tb.y = 80;
frame.appendChild(tb);
for (const part of titleParts) {
  if (part.highlight) {
    tb.appendChild(makeHL(part.text, 56));
  } else {
    const t = figma.createText();
    t.fontName = { family: "Inter", style: "Extra Bold" };
    t.characters = part.text; t.fontSize = 56;
    t.fills = [PAINT(C.text)]; tb.appendChild(t);
  }
}
// Subheading (after title block — separate node positioned below)
const sub = figma.createText();
sub.fontName = { family: "Inter", style: "Regular" };
sub.characters = subheading; sub.fontSize = 22;
sub.fills = [PAINT(C.text)]; sub.x = 60; sub.y = 340;
frame.appendChild(sub);

// Header row
const tableW = 960;
const labelW = 200;
const dataW = (tableW - labelW) / 2;
const header = figma.createAutoLayout("HORIZONTAL", { itemSpacing: 0 });
header.fills = [PAINT(C.text)]; header.cornerRadius = 12;
header.x = 60; header.y = 400; header.resize(tableW, 70);
header.counterAxisAlignItems = "CENTER";
frame.appendChild(header);
function headerCell(text, w) {
  const c = figma.createAutoLayout("HORIZONTAL", {
    itemSpacing: 0, paddingTop: 16, paddingBottom: 16, paddingLeft: 24, paddingRight: 24
  });
  c.fills = []; c.resize(w, 70);
  c.layoutSizingHorizontal = "FIXED"; c.layoutSizingVertical = "FIXED";
  c.counterAxisAlignItems = "CENTER";
  const t = figma.createText();
  t.fontName = { family: "Inter", style: "Semi Bold" };
  t.characters = text; t.fontSize = 22;
  t.fills = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 } }];
  c.appendChild(t); return c;
}
header.appendChild(headerCell(headers[0], labelW));
header.appendChild(headerCell(headers[1], dataW));
header.appendChild(headerCell(headers[2], dataW));

// Rows container
const rc = figma.createAutoLayout("VERTICAL", { itemSpacing: 0 });
rc.fills = []; rc.x = 60; rc.y = 470;
rc.resize(tableW, 1);
rc.layoutSizingHorizontal = "FIXED"; rc.layoutSizingVertical = "HUG";
frame.appendChild(rc);

function bulletText(s) {
  const t = figma.createText();
  t.fontName = { family: "Inter", style: "Regular" };
  t.characters = s; t.fontSize = 19;
  t.lineHeight = { unit: "PERCENT", value: 130 };
  t.fills = [PAINT(C.text)]; return t;
}
function dataCell(items, w) {
  const c = figma.createAutoLayout("VERTICAL", {
    itemSpacing: 8, paddingTop: 20, paddingBottom: 20, paddingLeft: 24, paddingRight: 24
  });
  c.fills = []; c.resize(w, 1);
  c.layoutSizingHorizontal = "FIXED"; c.layoutSizingVertical = "HUG";
  c.primaryAxisAlignItems = "CENTER";
  for (const i of items) c.appendChild(bulletText(i));
  return c;
}
function labelCell(label, w) {
  const c = figma.createAutoLayout("HORIZONTAL", {
    itemSpacing: 12, paddingTop: 20, paddingBottom: 20, paddingLeft: 24, paddingRight: 16
  });
  c.fills = []; c.resize(w, 1);
  c.layoutSizingHorizontal = "FIXED"; c.layoutSizingVertical = "HUG";
  c.counterAxisAlignItems = "CENTER";
  const dot = figma.createEllipse();
  dot.resize(14, 14); dot.fills = [PAINT(C.coral)];
  c.appendChild(dot);
  const t = figma.createText();
  t.fontName = { family: "Inter", style: "Semi Bold" };
  t.characters = label; t.fontSize = 22;
  t.fills = [PAINT(C.text)]; c.appendChild(t);
  return c;
}

for (const row of rows) {
  const rf = figma.createAutoLayout("HORIZONTAL", { itemSpacing: 0 });
  rf.fills = []; rf.resize(tableW, 1);
  rf.layoutSizingHorizontal = "FIXED"; rf.layoutSizingVertical = "HUG";
  rf.counterAxisAlignItems = "MIN";
  rf.strokes = [PAINT(C.border)];
  rf.strokeTopWeight = 1; rf.strokeBottomWeight = 0;
  rf.strokeLeftWeight = 0; rf.strokeRightWeight = 0;
  rf.appendChild(labelCell(row.label, labelW));
  rf.appendChild(dataCell(row.bullets1, dataW));
  rf.appendChild(dataCell(row.bullets2, dataW));
  rc.appendChild(rf);
}

makeAuthor(frame, 60, 1350 - 72 - 60);
makeWordmark(frame, 1080 - 180 - 60, 1350 - 60 - 60);
```

## Recipe: STEP GRID (typically 3×3 = 9 steps)

Inputs:
- `titleParts`: array of `{text, highlight}` for headline parts
- `subheading`: short descriptor
- `steps`: array of `{num: "01", title: "Short title", body: "1-2 sentence description."}` — 6, 9, or 12 items

```js
const frame = makeFrame("Infographic / Step Grid");
figma.currentPage.appendChild(frame);

// Title row (horizontal — keep on one line)
const titleStack = figma.createAutoLayout("VERTICAL", { itemSpacing: 8 });
titleStack.fills = []; titleStack.x = 60; titleStack.y = 80;
frame.appendChild(titleStack);

const titleRow = figma.createAutoLayout("HORIZONTAL", { itemSpacing: 16 });
titleRow.fills = []; titleRow.counterAxisAlignItems = "CENTER";
titleStack.appendChild(titleRow);
for (const part of titleParts) {
  if (part.highlight) {
    titleRow.appendChild(makeHL(part.text, 56));
  } else {
    const t = figma.createText();
    t.fontName = { family: "Inter", style: "Extra Bold" };
    t.characters = part.text; t.fontSize = 56;
    t.fills = [PAINT(C.text)]; titleRow.appendChild(t);
  }
}

const sub = figma.createText();
sub.fontName = { family: "Inter", style: "Regular" };
sub.characters = subheading; sub.fontSize = 22;
sub.fills = [PAINT(C.text)];
titleStack.appendChild(sub);

// Grid
const cols = 3;
const rows = Math.ceil(steps.length / cols);
const gap = 18;
const gridW = 960;
const cardW = (gridW - gap * (cols - 1)) / cols;

function makeCard(step) {
  const card = figma.createAutoLayout("VERTICAL", {
    itemSpacing: 14,
    paddingTop: 22, paddingBottom: 22, paddingLeft: 22, paddingRight: 22
  });
  card.cornerRadius = 12;
  card.fills = [PAINT(C.bg)];
  card.strokes = [PAINT(C.border)]; card.strokeWeight = 1;
  card.resize(cardW, 200);
  card.layoutSizingHorizontal = "FIXED";
  card.layoutSizingVertical = "HUG";
  
  // Badge
  const bw = figma.createAutoLayout("HORIZONTAL", {
    itemSpacing: 0, paddingTop: 6, paddingBottom: 6, paddingLeft: 12, paddingRight: 12
  });
  bw.fills = [PAINT(C.text)]; bw.cornerRadius = 4;
  const bt = figma.createText();
  bt.fontName = { family: "Inter", style: "Extra Bold" };
  bt.characters = step.num; bt.fontSize = 16;
  bt.fills = [{ type: "SOLID", color: { r: 1, g: 1, b: 1 } }];
  bt.letterSpacing = { unit: "PERCENT", value: 8 };
  bw.appendChild(bt);
  card.appendChild(bw);
  
  // Title (MUST set FILL after appendChild)
  const tt = figma.createText();
  tt.fontName = { family: "Inter", style: "Extra Bold" };
  tt.characters = step.title; tt.fontSize = 24;
  tt.lineHeight = { unit: "PERCENT", value: 120 };
  tt.fills = [PAINT(C.text)];
  tt.textAutoResize = "HEIGHT";
  card.appendChild(tt);
  tt.layoutSizingHorizontal = "FILL";
  
  // Body
  const bb = figma.createText();
  bb.fontName = { family: "Inter", style: "Regular" };
  bb.characters = step.body; bb.fontSize = 16;
  bb.lineHeight = { unit: "PERCENT", value: 140 };
  bb.fills = [PAINT(C.text)];
  bb.textAutoResize = "HEIGHT";
  card.appendChild(bb);
  bb.layoutSizingHorizontal = "FILL";
  
  return card;
}

const grid = figma.createAutoLayout("VERTICAL", { itemSpacing: gap });
grid.fills = []; grid.x = 60; grid.y = 360;
frame.appendChild(grid);
for (let r = 0; r < rows; r++) {
  const row = figma.createAutoLayout("HORIZONTAL", { itemSpacing: gap });
  row.fills = [];
  for (let c = 0; c < cols; c++) {
    const i = r * cols + c;
    if (i < steps.length) row.appendChild(makeCard(steps[i]));
  }
  grid.appendChild(row);
}

makeAuthor(frame, 60, 1350 - 72 - 60);
makeWordmark(frame, 1080 - 180 - 60, 1350 - 60 - 60);
```

## Recipe: VERTICAL STEPS (linear how-to, 3-5 ordered sections)

The **how-to counterpart to Block Grid**. Block Grid = a catalogue you scan; Vertical Steps = an instruction you read top-down. Added 2026-08-03 after a reference teardown: when the content is "do this, then this", a 3×3 grid reads as a reference card and loses the sequence.

**Pick this over Block Grid when** the content is ordered, the reader is meant to DO it, and each step deserves one *concrete* visual (a row of real things) rather than an abstract diagram. Rule of thumb: if the steps can be reordered without breaking meaning → Block Grid. If they can't → Vertical Steps.

**Concrete beats abstract here.** Block Grid mini-visuals are diagrams (donut, funnel, ring). Vertical Steps bands are interface-like objects: tiles, pills, boxes, chips, an input→output pair. Do NOT reuse the chart atoms in this template.

### Layout constants (1080×1350)

```js
const M = 60;                       // left/right margin (wider than Block Grid — this format breathes)
const CW = 1080 - M * 2;            // 960 content width
// header:  chip y=40 · title y=96 (2 lines, 46px CAPS centered) · subhead y≈214
// steps:   start y=280, section gap 38
// per step: number+title row (h 38) → caption (h 24) → gap 14 → band
// footer:  hairline rule + tagline row, then makeAuthor / makeWordmark
```

Budget the bands BEFORE building: `Σ(stepHeights) + gaps` must leave ≥ 175px for the footer block. Typical band heights: tileRow 104 · pillRow 58 · noteBar 52 · coralBoxRow 112 · twoColArrow 150. Four steps fit 1080×1350 comfortably; five is the ceiling. **Never exceed 1080×1350** — LinkedIn crops past 4:5.

### Step header

```js
// number in coral + title in ink, on one row; caption underneath in grey
function stepHead(f, n, title, caption, y) {
  mt(f, n, M, y + 6, 18, "Extra Bold", C.coral);
  mt(f, title, M + 46, y, 30, "Extra Bold", C.text);
  if (caption) mt(f, caption, M + 46, y + 40, 18, "Regular", C.grey);
  return y + (caption ? 74 : 46);            // returns the band's top y
}
```

### Band library

```js
// 1. TILE ROW — N cards, each optional badge + bold label + grey sub. The "your stack" band.
//    items = [{label, sub, badge}]  (badge = 1-2 chars or an emoji-free glyph)
function tileRow(f, x, y, w, items, opts = {}) {
  const h = opts.h || 104, gap = 14;
  const tw = (w - gap * (items.length - 1)) / items.length;
  const wrap = figma.createRectangle();
  wrap.resize(w + 28, h + 28); wrap.x = x - 14; wrap.y = y - 14; wrap.cornerRadius = 16;
  wrap.fills = [PAINT(C.card)]; f.appendChild(wrap);
  items.forEach((it, i) => {
    const tx = x + i * (tw + gap);
    const c = figma.createRectangle();
    c.resize(tw, h); c.x = tx; c.y = y; c.cornerRadius = 12;
    c.fills = [PAINT(C.bg)]; c.strokes = [PAINT(C.line)]; c.strokeWeight = 1; f.appendChild(c);
    if (it.badge) {
      const b = figma.createRectangle();
      b.resize(34, 34); b.x = tx + tw / 2 - 17; b.y = y + 16; b.cornerRadius = 9;
      b.fills = [PAINT(C.text)]; f.appendChild(b);
      mt(f, it.badge, tx + tw / 2 - 17, y + 25, 14, "Extra Bold", C.bg, "CENTER", 34);
    }
    mt(f, it.label, tx, y + (it.badge ? 60 : 26), 17, "Extra Bold", C.text, "CENTER", tw);
    if (it.sub) mt(f, it.sub, tx, y + (it.badge ? 82 : 52), 15, "Regular", C.grey, "CENTER", tw);
  });
  return y + h;
}

// 2. PILL ROW — N outlined CAPS pills. The "what each one exposes" band.
function pillRow(f, x, y, w, labels, opts = {}) {
  const h = opts.h || 58, gap = 14;
  const pw = (w - gap * (labels.length - 1)) / labels.length;
  labels.forEach((l, i) => {
    const px = x + i * (pw + gap);
    const r = figma.createRectangle();
    r.resize(pw, h); r.x = px; r.y = y; r.cornerRadius = 10;
    r.fills = [PAINT(C.bg)]; r.strokes = [PAINT(C.text)]; r.strokeWeight = 2; f.appendChild(r);
    const t = mt(f, l, px, y + h / 2 - 12, 21, "Extra Bold", C.text, "CENTER", pw);
    t.letterSpacing = { unit: "PERCENT", value: 6 };
  });
  return y + h;
}

// 3. NOTE BAR — full-width tinted bar: bold lead + grey tail. The one-line proof under a band.
function noteBar(f, x, y, w, lead, tail, opts = {}) {
  const h = opts.h || 52;
  const r = figma.createRectangle();
  r.resize(w, h); r.x = x; r.y = y; r.cornerRadius = 10;
  r.fills = [PAINT(opts.coral ? C.coralSoft : C.card)]; f.appendChild(r);
  const a = mt(f, lead, x + 20, y + h / 2 - 11, 17, "Extra Bold", C.text);
  if (tail) mt(f, tail, x + 20 + a.width + 8, y + h / 2 - 11, 17, "Regular", C.grey);
  return y + h;
}

// 4. CORAL BOX ROW — coral-outlined container, eyebrow label, right-hand tag, N solid coral boxes
//    with WHITE text. The "make it interview you" band. boxes = ["…", "…"]
function coralBoxRow(f, x, y, w, eyebrow, tag, boxes, opts = {}) {
  const bh = opts.bh || 76, pad = 18, gap = 12, h = bh + 40 + pad * 2;
  const shell = figma.createRectangle();
  shell.resize(w, h); shell.x = x; shell.y = y; shell.cornerRadius = 14;
  shell.fills = [PAINT(C.bg)]; shell.strokes = [PAINT(C.coral)]; shell.strokeWeight = 2; f.appendChild(shell);
  const e = mt(f, eyebrow, x + pad, y + pad, 14, "Semi Bold", C.coral);
  e.letterSpacing = { unit: "PERCENT", value: 10 };
  if (tag) {
    const t = mt(f, tag, x, y + pad, 14, "Semi Bold", C.grey, "RIGHT", w - pad);
    t.letterSpacing = { unit: "PERCENT", value: 10 };
  }
  const bw = (w - pad * 2 - gap * (boxes.length - 1)) / boxes.length;
  boxes.forEach((b, i) => {
    const bx = x + pad + i * (bw + gap);
    const r = figma.createRectangle();
    r.resize(bw, bh); r.x = bx; r.y = y + pad + 40; r.cornerRadius = 10;
    r.fills = [PAINT(C.coral)]; f.appendChild(r);
    const t = figma.createText();
    t.fontName = { family: "Inter", style: "Extra Bold" };
    t.characters = b; t.fontSize = 17; t.fills = [PAINT(C.bg)];      // WHITE on coral (brand rule)
    t.lineHeight = { unit: "PERCENT", value: 122 }; t.textAutoResize = "HEIGHT";
    f.appendChild(t); t.resize(bw - 28, t.height);
    t.x = bx + 14; t.y = y + pad + 40 + (bh - t.height) / 2;
  });
  return y + h;
}

// 5. TWO-COL ARROW — left panel (coral-arrow list) → arrow → right panel (wrapped chips).
//    The "you describe / it builds" band. Widest band; budget 150px.
function twoColArrow(f, x, y, w, leftTitle, leftItems, rightTitle, chips, opts = {}) {
  const h = opts.h || 150, arrowW = 56;
  const lw = Math.round((w - arrowW) * 0.46), rw = w - arrowW - lw;
  const lp = figma.createRectangle();
  lp.resize(lw, h); lp.x = x; lp.y = y; lp.cornerRadius = 12; lp.fills = [PAINT(C.card)]; f.appendChild(lp);
  const lt = mt(f, leftTitle, x + 18, y + 16, 13, "Semi Bold", C.grey);
  lt.letterSpacing = { unit: "PERCENT", value: 10 };
  leftItems.forEach((it, i) => {
    mt(f, "→", x + 18, y + 44 + i * 24, 15, "Semi Bold", C.coral);
    mt(f, it, x + 44, y + 44 + i * 24, 16, "Semi Bold", C.text);
  });
  mt(f, "→", x + lw + 14, y + h / 2 - 16, 30, "Semi Bold", C.grey);
  const rp = figma.createRectangle();
  rp.resize(rw, h); rp.x = x + lw + arrowW; rp.y = y; rp.cornerRadius = 12;
  rp.fills = [PAINT(C.bg)]; rp.strokes = [PAINT(C.text)]; rp.strokeWeight = 2; f.appendChild(rp);
  const rt = mt(f, rightTitle, x + lw + arrowW + 18, y + 16, 13, "Semi Bold", C.text);
  rt.letterSpacing = { unit: "PERCENT", value: 10 };
  chipWrap(f, x + lw + arrowW + 18, y + 44, rw - 36, chips);
  return y + h;
}

// 6. CHIP WRAP — mono-ish chips that wrap onto rows. Use for file names, tags, fields.
function chipWrap(f, x, y, w, chips, opts = {}) {
  const ch = opts.ch || 32, gap = 8, fs = opts.fs || 14;
  let cx = x, cy = y;
  for (const label of chips) {
    const tw = label.length * fs * 0.60 + 24;
    if (cx + tw > x + w) { cx = x; cy += ch + gap; }
    const r = figma.createRectangle();
    r.resize(tw, ch); r.x = cx; r.y = cy; r.cornerRadius = 8;
    r.fills = [PAINT(C.bg)]; r.strokes = [PAINT(C.line)]; r.strokeWeight = 1; f.appendChild(r);
    mt(f, label, cx, cy + ch / 2 - 9, fs, "Semi Bold", C.text, "CENTER", tw);
    cx += tw + gap;
  }
  return cy + ch;
}

// 7. FOOTER TAGLINE — hairline rule + bold lead + grey tail, sits ABOVE makeAuthor/makeWordmark.
function taglineRule(f, x, y, w, lead, tail) {
  const r = figma.createRectangle();
  r.resize(w, 1); r.x = x; r.y = y; r.fills = [PAINT(C.line)]; f.appendChild(r);
  const a = mt(f, lead, x, y + 20, 18, "Extra Bold", C.text);
  if (tail) mt(f, tail, x + a.width + 8, y + 20, 18, "Regular", C.grey);
  return y + 46;
}
```

`C.card` = `{r:247/255,g:245/255,b:241/255}`, `C.coralSoft` = `{r:251/255,g:234/255,b:232/255}`, `C.line` = `{r:232/255,g:230/255,b:225/255}`, `C.grey` = `{r:108/255,g:106/255,b:100/255}` — add these to the `C` object for this template.

### Assembly

```js
const frame = makeFrame("Infographic / Vertical Steps");
figma.currentPage.appendChild(frame);
buildChip(frame, "ПРОЦЕСИ");                       // rubric chip, centered, y=40
buildTitle(frame, titleParts, subheading);         // CAPS centered — brand rule still wins here

let y = 280;
y = stepHead(frame, "01", "…", "…", y);
y = tileRow(frame, M, y, CW, tiles) + 38;
y = stepHead(frame, "02", "…", "…", y);
y = pillRow(frame, M, y, CW, ["API","CLI","MCP","ВЕБХУК"]) + 12;
y = noteBar(frame, M, y, CW, "…", "…") + 38;
y = stepHead(frame, "03", "…", "…", y);
y = coralBoxRow(frame, M, y, CW, "PLAN MODE / ГОДИНА ВГОЛОС", "ЦЕ НЕ ПРОМПТ", boxes) + 38;
y = stepHead(frame, "04", "…", "…", y);
y = twoColArrow(frame, M, y, CW, "ТИ ОПИСУЄШ", left, "ВОНО БУДУЄ", chips);

taglineRule(frame, M, 1350 - 190, CW, "…", "…");
makeAuthor(frame, M, 1350 - 72 - 52);
makeWordmark(frame, 0, 1350 - 72 - 42);
```

### Real product logos in a tile row

A logo row is what makes step 1 land — the reader recognises their own stack. Fetch the marks, don't draw them.

```bash
# 1. grab icons (python, not a bash for-loop — PATH gets clobbered in multi-line loops)
#    apple-touch-icon first, Google's favicon service as fallback (128px, always PNG)
https://<domain>/apple-touch-icon.png
https://www.google.com/s2/favicons?domain=<domain>&sz=128
# known exceptions: notion → https://www.notion.so/images/logo-ios.png · ahrefs → no public icon, skip it
```

Then `upload_assets` with `count = N`, POST each file to its own `submitUrl`, and use the returned `imageHash` in a `FIT`-scaled rectangle:

```js
function img(hash, x, y, size) {
  const r = figma.createRectangle();
  r.resize(size, size); r.x = x; r.y = y; r.cornerRadius = size * 0.22;
  r.fills = [{ type: "IMAGE", imageHash: hash, scaleMode: "FIT" }];   // FIT, never FILL — FILL crops the mark
  return r;
}
```

⚠️ `upload_assets` drops a 400×300 placeholder frame per asset on the canvas. Delete them before screenshotting or they show up beside the artboard.

Inline a single logo in a `noteBar` when the note is about that specific tool — it reads as evidence, not decoration.

### Vertical Steps pitfalls

- **Every band builder returns its bottom y.** Chain through `y` and add the gap explicitly — never hardcode section positions, or one copy edit shifts everything into the footer.
- **Measure before you build.** Sum the band heights on paper first. Running past y≈1175 collides with the footer, and the fix is a rebuild, not a nudge.
- **`chipWrap` width is estimated** from `label.length * fs * 0.60` — fine for Latin file names (`positioning.md`), too narrow for CAPS Cyrillic. Bump the factor to 0.72 for Cyrillic labels or the text overflows its chip.
- **Real vendor names and logos ARE allowed in Viktor's OWN creatives** (confirmed 2026-08-03). CLAUDE.md §4's ban on third-party vendor names covers client-facing material and client repos, not his personal brand. Swapping real tools for generic categories (джерело · збагачення · перевірка) kills the creative — the reader recognising their own stack is half the hook. Client names stay banned everywhere.
- **A backdrop rect behind a band will eat the step caption.** The band starts at the y returned by `stepHead`, and a wrapper drawn at `y - 12` reaches back into the caption's last line. Inset the wrapper ≤4 at the top, or push the whole band down.
- **Right-aligned text nodes report the ALIGNMENT width, not the glyph width.** `mt(..., "RIGHT", 1020).width` is 1020, so positioning an icon at `x - label.width` throws it off-canvas. Measure with a throwaway LEFT-aligned probe node, read `.width`, then `.remove()` it.
- **One coral band per creative.** The `coralBoxRow` is the punch. If two bands go coral, neither reads as the emphasis — keep the rest charcoal/card.
- **Captions are real sentences here**, not the 2-4 word telegraph of Block Grid. Short sentences with a period. That tonal difference is most of what makes the format read as an instruction.

## Custom builds (Branching Tree, ICP/Quadrant Analysis, mixed canvas)

For shapes NOT covered by the 2 templates:

1. **Acknowledge to Viktor**: "Це custom build — не template. Витратимо ~30-45 хв на унікальну структуру."
2. Get bullet-point structure confirmation from Viktor.
3. Build in new Figma file inline using the atom builders (Wordmark, Author, HL).
4. For arrows / connectors → use `figma.createVector()` with simple paths (line + arrowhead triangle).
5. Iterate visually with screenshots until acceptable.

## Pitfalls

- **Font style strings**: `Extra Bold` / `Semi Bold` / `Regular` — WITH spaces. Never `ExtraBold`.
- **Text wrapping in auto-layout cards**: ALWAYS `appendChild` first, then `layoutSizingHorizontal = "FILL"`. Don't use manual `.resize(w, 1)` on text inside auto-layout — it collapses.
- **Cross-file image hashes**: must `upload_assets` to each new file before using hashes — they look global but each file has its own registry.
- **Comparison Table: 3+ bullets per cell** — keep them PUNCHY (3-6 words). Long bullets break the visual rhythm.
- **Step Grid: 6/9/12 items**. Avoid 7, 8, 10, 11 (don't fit cleanly into 3-col).
- **Coral discipline**: 1 highlight per title MAX. Coral on row markers only. Avoid coloring rows / cards / backgrounds. (Ladder is the one sanctioned exception — there the coral ramp IS the data.)
- **HTML/Chrome backend**: never ship a PNG you haven't opened. The two Chrome flags are the difference between Inter and a serif fallback on every Cyrillic glyph, and the failure is silent.

### Chart-specific pitfalls

- **Donut arcs**: use `ellipse.arcData = { startingAngle, endingAngle, innerRadius }` — angles in RADIANS, 0 = 3 o'clock, clockwise. Start at `-Math.PI/2` for 12 o'clock. `innerRadius` is 0-1 (fraction of radius), NOT pixels. Each slice is a full-diameter ellipse stacked at the same x/y — bounding boxes overlap, wedges don't.
- **Vectors don't auto-move**: a freshly created vector sits at x=0,y=0 and its `vectorPaths` coords are read in that local space → for the curve, author the path in FRAME coordinates and leave `v.x=v.y=0`. For funnel/arrow, author the path starting at 0,0 and set `v.x`/`v.y` to position it. Don't mix the two.
- **Vector fill vs stroke**: line charts = `fills=[]` + `strokes=[...]` + `strokeWeight`. Filled shapes (funnel, arrow, area) = `fills=[...]` + `strokes=[]`. Setting both on a curve double-renders.
- **Chart text is absolutely positioned** — use `makeText(...)`, never the auto-layout text path (it collapses outside a layout parent). For centered labels you MUST pass a `width`.
- **Slice colors come from `RAMP` only** — 4-6 brand-pure fills, most important slice = coral. No pastels, no invented hues. If you need a 7th slice, merge the tail into "інше".
- **Verify geometry with a screenshot** for curve and funnel before declaring done — these are hand-tuned and a 20px nudge is normal. Donut/timeline are deterministic and rarely need it.
- **opacity on a SOLID paint**: the area fill under a curve uses `{ type:"SOLID", color: C.coral, opacity: 0.12 }` — opacity lives on the paint, not the node.

## Output template

```
✅ Інфографіка готова — [Block Grid / Donut / Funnel / Growth Curve / Timeline / Comparison Table / Step Grid / Custom]

🔗 Figma: [file_url]

[inline screenshot of the infographic]

📥 Export: відкрий файл → виділи frame → Export → PNG.

Що покращити?
- Перефразувати заголовок / coral hl на інше слово
- Для charts: змінити значення/пропорції, переставити slice на coral, підрівняти криву
- Додати/прибрати рядки / cards / slices
- Змінити кольори в окремих елементах (forest для positive)
```
