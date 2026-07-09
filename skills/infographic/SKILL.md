---
name: infographic
description: Generates LinkedIn infographics (1080×1350) for Victor Shulga's personal brand in Figma from raw text. Use whenever Viktor pastes text and asks for an infographic — "інфографіка", "зроби інфографіку", "comparison table з цього", "step grid", "9 кроків як інфографіка", "donut/пончик", "лійка/funnel", "крива росту", "таймлайн", "make an infographic from this", or describes structured content that's NOT a carousel sequence. Routes between text templates (Comparison Table N×3, Step Grid 3×3) AND data-viz chart templates (Donut/Pie, Funnel, Growth Curve, Timeline), or falls back to custom-build for other shapes (Branching Tree, ICP/Quadrant Analysis).
---

# /infographic

Generate LinkedIn infographics for Victor Shulga's personal brand using his existing Figma design system. **Brand-pure palette**: white BG + coral + charcoal + forest only. NO pastels.

## When to trigger

- Viktor pastes text + says "інфографіка", "зроби інфографіку"
- Viktor describes structured content (table, steps, categories) and wants visuals
- Viktor says "comparison table", "step grid", "9 кроків як інфографіку"
- Viktor says "donut", "пончик", "pie", "лійка", "funnel", "крива росту", "growth curve", "таймлайн", "timeline", "before/after по осі"
- Any single-image structured visualization (NOT a multi-slide carousel — for that use `/linkedin-carousel`)

## Decision tree — which template to use

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
| Branching tree (1 → N → M with arrows) | **Custom build** — not templated, ~30-45 min |
| Multiple categorized cards + diagram + matrix (mixed canvas) | **Custom build** — not templated, ~45-60 min |

A single infographic may **combine** a chart band + a text band (e.g. donut on top, 3-tier funnel below) — see the demo pattern. Stack bands vertically with ~40-60px gutters.

If content is genuinely 2-3 things and short → ask Viktor if he wants it as 2-3 SLIDE CAROUSEL instead (better for LinkedIn engagement).

## Brand reference (memorize)

**Foundations file**: `https://www.figma.com/design/ngweiN07cnXQo8zjRMfbZI`
**Plan key (Viktor)**: `team::YOUR_PLAN_KEY`
**Format**: 1080×1350 (4:5 portrait)

**Palette** (always 0-1 range):
- BG `{r:1, g:1, b:1}` white
- Text `{r:30/255, g:30/255, b:30/255}` charcoal
- Coral `{r:232/255, g:90/255, b:79/255}` for highlights / accent markers
- Forest `{r:46/255, g:125/255, b:91/255}` for positive callouts ONLY
- Border `{r:0.92, g:0.92, b:0.92}` light grey for card/row dividers

**Typography**: Inter — `Extra Bold`, `Semi Bold`, `Regular` (with space in style names).

**TITLE RULES (brand-wide, every post — infographic AND carousel):**
- Main title is **ALL CAPS** and **CENTERED** (not left-aligned).
- Any **coral-highlight pill** has **WHITE text** (never charcoal). `makeHL` already does this.
- Section sub-labels are centered too. (See [[feedback_infographic_caps_title]].)

**Image asset hash** (must be uploaded to new file first):
- Avatar (Viktor's photo on coral disc, 1080×1080): `ea444ff18bbcd12290653fdf4d261e16949fc0d9`

The brand mark in the footer is now a **bowtie on a coral square drawn as vectors** (`makeBowtieSquare`) — NO wordmark image needed. Footer = `makeAuthor` (photo + name + FRACTIONAL CRO pill) left, `makeWordmark` (bowtie mark + victorshulga.com) right. This replaced the old VICTOR SHULGA globe wordmark + "Fractional CRO" line.

**Source PNG**:
- `~/.claude/skills/infographic/assets/avatar.png`

## Workflow

### Step 1 — Classify + plan structure

Pick template based on content shape (decision tree above). For Comparison Table: identify the comparison axis (2 columns vs 3), category rows, and bullets per cell. For Step Grid: identify step count (best is 9 = 3×3, but also 6 = 2×3 or 12 = 3×4).

For Custom builds: outline the structure to Viktor as bullet points, get confirmation before starting, then build inline using same atom builders.

### Step 2 — Create new Figma file

```
whoami → planKey "team::YOUR_PLAN_KEY"
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
  text:   { r: 30/255,  g: 30/255,  b: 30/255  },
  coral:  { r: 232/255, g: 90/255,  b: 79/255  },
  forest: { r: 46/255,  g: 125/255, b: 91/255  },
  border: { r: 0.92,    g: 0.92,    b: 0.92    },
};
const PAINT = (c) => ({ type: "SOLID", color: c });
const IMG = {
  avatar:   "ea444ff18bbcd12290653fdf4d261e16949fc0d9",
};

// Bowtie brand mark — APPROVED victorshulga.com symbol: coral rounded square,
// two ROUNDED white wings (stroke-linejoin round) + charcoal center node.
// Geometry 1:1 with victor-logo/assets/favicon.svg (viewBox 100). Vector-drawn, no image.
// NODE = { r:28/255, g:28/255, b:30/255 } (#1C1C1E). Replaces the old wordmark globe.
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

## Chart atom builders — v2 (Pierre-style diagram elements)

Brand-recolored versions of Pierre Herubel's visual vocabulary (approved 2026-06-19) — use these to put a real graphic in EVERY block, not just text. All brand-pure (coral + tints + forest + charcoal); no pastels. `GREY` = the neutral dot/track shade.

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

## Icon library + icon-tiles (Pierre "icon-tile" element)

31 brand line icons live as SVG files in `assets/icons/` (24-grid, stroke 2, round caps, charcoal). The **icon-tile** — rounded coral-tint square + line icon + label — is the core Pierre element: use it in ROWS for "channels / ways / list" content (e.g. lead-gen channels, content formats, outbound tactics) instead of plain text pills. Preview all 31 at `assets/icons/preview.html`.

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

**Rules:** one row = 3-6 tiles (wrap to a second row beyond 6). Keep tiles charcoal by default; set `accent:true` on at most one tile per row (the "punch"), per the one-accent-per-card rule. Tile label ≤ 2 words. To reproduce a Pierre-style "canvas of channels" (e.g. Demand Gen icon grid), stack 2-3 `makeIconRow` bands under a section header.

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

This is the **flagship dense format** — the one that looks like the GTM/LinkedIn reference posts (Sollo, McTighe, Estner): a header + a 3-col grid of cards, where **every card carries its own little diagram**, not just text. Use it to condense a whole framework, playbook, or slide deck into one image. Built 2026-06-17 from the GTM-стратегія deck (file `qQDQowVVvNIOtGKp5XWcev`, 9 cards = 3×3).

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
- **Coral discipline**: 1 highlight per title MAX. Coral on row markers only. Avoid coloring rows / cards / backgrounds.

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
