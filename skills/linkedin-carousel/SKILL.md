---
name: linkedin-carousel
description: Generates a LinkedIn carousel design (1080×1350, 4:5) for Victor Shulga's personal brand in Figma from raw text. Use whenever Viktor pastes text and asks for a carousel — "карусель", "зроби карусель", "побудуй карусель", "карусель на цю тему", "10 слайдів про X", "make a carousel from this", or shares a topic/draft and wants visuals. Always produces a complete carousel in a new Figma file with each slide screenshot inline, matching Viktor's exact brand language: white BG + coral accents + Inter typography + author block + Victor Shulga wordmark.
---

# /linkedin-carousel

You generate LinkedIn carousel designs for Victor Shulga's personal brand by writing slides directly into a new Figma file using the Figma MCP `use_figma` tool.

## When to trigger

- Viktor pastes text and says "карусель", "зроби карусель", "побудуй карусель"
- Viktor provides a topic/draft and asks for slide visuals
- Viktor says "make a carousel from this", "give me 10 slides about X"
- Any time the deliverable is a LinkedIn carousel for the personal brand

## What you need from Viktor

1. **Text content** (Ukrainian, occasionally English). Either:
   - Already-written carousel copy split into slides, OR
   - A topic / hook / raw draft to expand into slides
2. *Optional*: target slide count (default: decide based on idea density, aim 7-10)
3. *Optional*: tone hint (insight / story / listicle / rant / case study)

If the text is too thin (under 100 words and no clear thesis) → ask ONE clarifying question before starting. Otherwise just go.

## Brand reference (memorize)

**File**: `https://www.figma.com/design/ngweiN07cnXQo8zjRMfbZI` (Foundations + slide templates)
**Slide size**: 1080×1350 (4:5 portrait)
**Plan key (Viktor)**: `team::YOUR_PLAN_KEY`

**Palette** (always bind to variables if working in Foundations file):
- Background `#FFFFFF`
- Text `#1E1E1E` (charcoal)
- Accent / Primary `#E85A4F` (coral) — highlights, badges, swipe arrow, separators
- Accent / Positive `#2E7D5B` (forest green) — ONLY for positive metrics/wins

**Typography** (Inter family, exact style strings):
- Cover headline: Inter `Extra Bold` 96px, line-height 105%
- Section title: Inter `Extra Bold` 72px, line-height 115%
- Body large: Inter `Regular` 32px, line-height 140%
- Body default: Inter `Regular` 24px, line-height 140%
- Author name: Inter `Extra Bold` 22px
- Author role: Inter `Regular` 18px
- Caption: Inter `Regular` 14px

Style strings MUST be `Extra Bold` / `Semi Bold` / `Regular` with the space — NOT `ExtraBold` / `SemiBold`.

**Image asset hashes** (content-addressed, globally unique — same bytes → same hash everywhere):
- Avatar (Viktor portrait on coral disc, full-quality): `ea444ff18bbcd12290653fdf4d261e16949fc0d9` (1080×1080)
- Wordmark (FULL "VICTOR SHULGA" logo with globe + text — single image, not composed): `4f06f797dbd0f826e9b5b219605dcf3af93b2a6a` (200×100, 2:1 ratio)
- Cover photo (Viktor portrait, cropped): `387843364547d8b44de1fa68304c2b3f826899bf` (590×1010)

**Source PNG files** (use these to upload into new files):
- `~/.claude/skills/linkedin-carousel/assets/avatar.png`
- `~/.claude/skills/linkedin-carousel/assets/wordmark.png`
- `~/.claude/skills/linkedin-carousel/assets/cover-photo.png`

⚠️ **CRITICAL**: image hashes are globally unique BUT each file must REGISTER the image bytes before nodes can reference them via hash. Cross-file hash references silently fail (image fill drops to empty). The workflow MUST upload the 3 PNGs to each new file before building slides.

## The 4 slide variants

Every slide is 1080×1350 with white BG. Universal atoms ALWAYS in fixed positions:

```
┌────────────────────────────────────────┐
│ [wordmark*]              [swipe arrow*]│  ← *position varies by variant
│                                         │
│  HEADLINE area (variant-specific)       │
│                                         │
│  BODY area (variant-specific)           │
│                                         │
│ [author block]          [wordmark]      │
└────────────────────────────────────────┘
```

### Variant: COVER
- Top-left: Wordmark (small)
- Top-right: Swipe Arrow Box
- Center-left: Big multi-line headline with coral highlight on 1-2 key words
- Bottom-right: Cropped photo of Viktor (use asset hash)
- Bottom-left: Stacked first/last name caption with coral hl on last name
- NO author block (replaced by name caption)

### Variant: CONTENT
- Top-left: Section title (1-3 words, ~72px Extra Bold)
- Top-right: Swipe Arrow Box
- Below title: Optional small subtitle/eyebrow
- Center: Body content (large text, or list, or quote)
- Bottom-left: Author Block (avatar + Victor Shulga + Fractional CRO)
- Bottom-right: Wordmark

### Variant: STAT
- Same as Content for top + bottom
- Center: HUGE stat number (~240px Extra Bold)
  - Use `accent/positive` (#2E7D5B forest green) if it's a positive metric/win
  - Use `text` (#1E1E1E charcoal) for neutral numbers
  - Use `accent/primary` (#E85A4F coral) for warning/loss numbers
- Below stat: caption (large body) explaining what the number is

### Variant: CTA (last slide)
- Top: NO swipe arrow (it's the final slide)
- Center: Big headline like "Found this useful?" / "Корисно?" with coral hl on action word
- Mid-bottom: Body prompt ("Save and repost to support…")
- Coral block with action text ("+Like & Comment" or "+Лайк і коменти")
- Bottom-left: Author Block
- Bottom-right: Wordmark BIGGER (×1.3 scale)

## Workflow

### Step 1 — Parse text into slide plan

Apply Viktor's rule: **«Одна думка = один слайд»** (one thought = one slide).

Output a structured plan:

```
Plan:
1. COVER — hook headline: "[text]" — hl words: ["X", "Y"]
2. CONTENT — section: "Контекст" — body: "..."
3. CONTENT — section: "Проблема" — body: "..."
4. STAT — section: "Результат" — number: "+247%" (positive) — caption: "..."
5. CONTENT — ...
...
N. CTA — headline: "Корисно?" — action: "+Лайк і коменти"
```

**Section title heuristics** (use Viktor's idiom):
- Setup: "Контекст", "Передісторія", "Чому це важливо"
- Problem: "Проблема", "Дорога проблема"
- Solution: "Рішення", "Метод", "Підхід"
- Steps: "Крок 1.", "Крок 2." …
- Examples: "Приклад", "Кейс", "З життя"
- Insights: "Інсайт", "Висновок", "М'ясо контенту"
- Bonus: "Бонус"

**Coral highlight pick rule** (cover):
- 1-2 words MAX per cover, never more
- The MAIN NOUN (what the post is about) — e.g. "каруселі", "пропоузал", "GTM аудит"
- Optionally a leading short word — e.g. "Як", "Чому"

**Stat extraction**:
- Scan body for "+X%", "X%", "Xx", "$X", growth metrics
- Only convert to Stat slide if the number IS the point (not an aside)

**Slide count target**: 7-10. Less than 5 = thin; more than 12 = over-stuffed.

### Step 2 — Create the new Figma file

```
whoami → use planKey "team::YOUR_PLAN_KEY"
create_new_file → editorType="design", fileName="[short topic] — Carousel"
```

Capture the new file_key.

### Step 2.5 — MANDATORY: Register the 3 brand images in the new file

Skip this step → image fills silently drop. Always do it.

```
upload_assets fileKey=<new_file_key> count=3
# Returns 3 single-use submit URLs
```

Then POST each PNG via Bash (multipart/form-data):

```bash
curl -s -X POST -F "file=@~/.claude/skills/linkedin-carousel/assets/avatar.png" "<submitUrl_1>"
curl -s -X POST -F "file=@~/.claude/skills/linkedin-carousel/assets/wordmark.png" "<submitUrl_2>"
curl -s -X POST -F "file=@~/.claude/skills/linkedin-carousel/assets/cover-photo.png" "<submitUrl_3>"
```

Each response confirms `success: true` and returns the hash (which will match the constants above). Bytes are now registered in the file's image store — fills can reference them by hash.

The uploads also auto-create 3 frames on the canvas (one per image) — **DELETE these placeholder frames in Step 3** before building slides.

### Step 3 — Clean canvas + set up fonts (single use_figma call)

```js
// Delete the 3 auto-placed upload frames
const page = figma.currentPage;
page.name = "Carousel";
for (const c of [...page.children]) c.remove();

// Load all Inter fonts we'll need
await figma.loadFontAsync({ family: "Inter", style: "Extra Bold" });
await figma.loadFontAsync({ family: "Inter", style: "Regular" });
await figma.loadFontAsync({ family: "Inter", style: "Semi Bold" });
```

Skip loading variables — for new generated files we inline hex colors directly to keep the skill self-contained and not dependent on library publishing.

**Color constants** for inlined use:
```js
const C = {
  bg:      { r: 1,        g: 1,        b: 1        },  // #FFFFFF
  text:    { r: 30/255,   g: 30/255,   b: 30/255   },  // #1E1E1E
  coral:   { r: 232/255,  g: 90/255,   b: 79/255   },  // #E85A4F
  forest:  { r: 46/255,   g: 125/255,  b: 91/255   },  // #2E7D5B
};
const PAINT = (c) => ({ type: "SOLID", color: c });
```

### Step 4 — Build slides one by one

For each slide in the plan, run a `use_figma` call. Each slide is a separate Frame, 1080×1350. Position with x = slideIndex × (1080 + 100), y = 100.

**Atom builders** (reuse across slides — keep these as inline helper functions in your scripts):

```js
// Wordmark — single image, full "VICTOR SHULGA" logo
// Source 200×100 (2:1 ratio). Scale param controls width; height auto-derives.
function makeWordmark(parent, x, y, scale = 1) {
  const w = 180 * scale;
  const h = w / 2;  // preserve 2:1 aspect
  const wm = figma.createRectangle();
  wm.name = "Wordmark";
  wm.resize(w, h);
  wm.fills = [{
    type: "IMAGE",
    imageHash: "4f06f797dbd0f826e9b5b219605dcf3af93b2a6a",
    scaleMode: "FIT"
  }];
  wm.x = x; wm.y = y;
  parent.appendChild(wm);
  return wm;
}

// Author Block
function makeAuthorBlock(parent, x, y) {
  const ab = figma.createAutoLayout("HORIZONTAL", { itemSpacing: 16 });
  ab.fills = [];
  ab.counterAxisAlignItems = "CENTER";

  const avatar = figma.createEllipse();
  avatar.resize(72, 72);
  avatar.fills = [{
    type: "IMAGE",
    imageHash: "ea444ff18bbcd12290653fdf4d261e16949fc0d9",
    scaleMode: "FILL"
  }];
  ab.appendChild(avatar);

  const stack = figma.createAutoLayout("VERTICAL", { itemSpacing: 4 });
  stack.fills = [];
  ab.appendChild(stack);

  const name = figma.createText();
  name.fontName = { family: "Inter", style: "Extra Bold" };
  name.characters = "Victor Shulga";
  name.fontSize = 22;
  name.fills = [PAINT(C.text)];
  stack.appendChild(name);

  const role = figma.createText();
  role.fontName = { family: "Inter", style: "Regular" };
  role.characters = "Fractional CRO";
  role.fontSize = 18;
  role.fills = [PAINT(C.text)];
  stack.appendChild(role);

  ab.x = x; ab.y = y;
  parent.appendChild(ab);
  return ab;
}

// Swipe Arrow Box
function makeSwipeArrow(parent, x, y) {
  const sa = figma.createAutoLayout("HORIZONTAL", {
    itemSpacing: 0,
    paddingTop: 18, paddingBottom: 18, paddingLeft: 22, paddingRight: 22
  });
  sa.primaryAxisAlignItems = "CENTER";
  sa.counterAxisAlignItems = "CENTER";
  sa.cornerRadius = 4;
  sa.fills = [PAINT(C.coral)];

  const arrow = figma.createText();
  arrow.fontName = { family: "Inter", style: "Extra Bold" };
  arrow.characters = "→";
  arrow.fontSize = 56;
  arrow.fills = [PAINT(C.text)];
  sa.appendChild(arrow);

  sa.x = x; sa.y = y;
  parent.appendChild(sa);
  return sa;
}

// Coral highlighted text — wraps a piece of text in a coral background block
function makeHighlightedText(text, fontStyle, fontSize, padding = {top: 4, bottom: 4, left: 18, right: 18}) {
  const wrap = figma.createAutoLayout("HORIZONTAL", {
    itemSpacing: 0,
    paddingTop: padding.top, paddingBottom: padding.bottom,
    paddingLeft: padding.left, paddingRight: padding.right
  });
  wrap.fills = [PAINT(C.coral)];
  const t = figma.createText();
  t.fontName = { family: "Inter", style: fontStyle };
  t.characters = text;
  t.fontSize = fontSize;
  t.fills = [PAINT(C.text)];
  wrap.appendChild(t);
  return wrap;
}

// Helper to make a new slide frame
function makeSlideFrame(index, name) {
  const frame = figma.createFrame();
  frame.name = name;
  frame.resize(1080, 1350);
  frame.fills = [PAINT(C.bg)];
  frame.clipsContent = true;
  frame.x = index * 1180; // 1080 width + 100 gap
  frame.y = 100;
  return frame;
}
```

For each slide, assemble using the atom builders + variant-specific content. Return created node IDs after each `use_figma` call.

**Batch size rule**: Build at most 3 slides per `use_figma` call to keep scripts under the 50,000 char limit and atomic.

### Step 5 — Screenshot each slide for the user

After all slides are built, take screenshots:

```js
// In one final use_figma call:
const slides = figma.currentPage.children.filter(c => c.name.startsWith("Slide /"));
for (const s of slides) {
  await s.screenshot({ scale: 0.5 });  // 540px wide, readable inline
}
```

### Step 6 — Return to Viktor

Send Viktor:
1. **Figma URL** to the new file — for live editing
2. **Inline screenshots** of all slides (already returned via screenshot calls)
3. **Quick note** on what to tweak in Figma directly if anything (manual PNG export is one click in Figma UI: select all slides → Export PNG)

## Slide-specific build recipes

### COVER recipe

```js
const slide = makeSlideFrame(0, "Slide / Cover");
figma.currentPage.appendChild(slide);

makeWordmark(slide, 60, 60);
makeSwipeArrow(slide, 1080 - 60 - 100, 60);

// Cover photo bottom-right
const photo = figma.createRectangle();
photo.resize(480, 820);
photo.x = 1080 - 480 - 20;
photo.y = 1350 - 820 - 120;
photo.fills = [{
  type: "IMAGE",
  imageHash: "387843364547d8b44de1fa68304c2b3f826899bf",
  scaleMode: "FIT"
}];
slide.appendChild(photo);

// Headline stack (left side, vertical)
const stack = figma.createAutoLayout("VERTICAL", { itemSpacing: 12, name: "Headline" });
stack.fills = [];
stack.x = 60; stack.y = 280;
stack.resize(620, 200);
stack.layoutSizingHorizontal = "FIXED";
stack.layoutSizingVertical = "HUG";
slide.appendChild(stack);

// Row 1 — split into highlighted + plain parts
const row1 = figma.createAutoLayout("HORIZONTAL", { itemSpacing: 16 });
row1.fills = [];
row1.counterAxisAlignItems = "CENTER";
row1.appendChild(makeHighlightedText(HL_WORD_1, "Extra Bold", 96));
const plain1 = figma.createText();
plain1.fontName = { family: "Inter", style: "Extra Bold" };
plain1.characters = PLAIN_REST_OF_LINE_1;
plain1.fontSize = 96;
plain1.fills = [PAINT(C.text)];
row1.appendChild(plain1);
stack.appendChild(row1);

// Row 2 — second highlighted word on own line
stack.appendChild(makeHighlightedText(HL_WORD_2, "Extra Bold", 96));

// Subheading
const sub = figma.createText();
sub.fontName = { family: "Inter", style: "Regular" };
sub.characters = SUBHEADING_TEXT;
sub.fontSize = 36;
sub.fills = [PAINT(C.text)];
stack.appendChild(sub);

// Name caption bottom-left
const nameStack = figma.createAutoLayout("VERTICAL", { itemSpacing: 0 });
nameStack.fills = [];
nameStack.x = 60; nameStack.y = 1350 - 200;
slide.appendChild(nameStack);

const fname = figma.createText();
fname.fontName = { family: "Inter", style: "Extra Bold" };
fname.characters = "Victor";
fname.fontSize = 56;
fname.fills = [PAINT(C.text)];
nameStack.appendChild(fname);

nameStack.appendChild(makeHighlightedText("Shulga", "Extra Bold", 56, {top: 4, bottom: 4, left: 12, right: 12}));
```

### CONTENT recipe

```js
const slide = makeSlideFrame(index, "Slide / Content");
figma.currentPage.appendChild(slide);

makeSwipeArrow(slide, 1080 - 60 - 100, 60);

// Section title
const title = figma.createText();
title.fontName = { family: "Inter", style: "Extra Bold" };
title.characters = SECTION_TITLE;  // e.g. "Контекст"
title.fontSize = 72;
title.fills = [PAINT(C.text)];
title.x = 60; title.y = 140;
slide.appendChild(title);

// Body
const body = figma.createText();
body.fontName = { family: "Inter", style: "Regular" };
body.characters = BODY_TEXT;
body.fontSize = 32;
body.lineHeight = { unit: "PERCENT", value: 140 };
body.fills = [PAINT(C.text)];
body.x = 60; body.y = 380;
body.resize(960, 720);
body.textAutoResize = "HEIGHT";
slide.appendChild(body);

makeAuthorBlock(slide, 60, 1350 - 72 - 60);
makeWordmark(slide, 1080 - 180 - 60, 1350 - 60 - 60);
```

### STAT recipe

```js
const slide = makeSlideFrame(index, "Slide / Stat");
figma.currentPage.appendChild(slide);

makeSwipeArrow(slide, 1080 - 60 - 100, 60);

// Section title
const title = figma.createText();
title.fontName = { family: "Inter", style: "Extra Bold" };
title.characters = SECTION_TITLE;  // e.g. "Результат"
title.fontSize = 72;
title.fills = [PAINT(C.text)];
title.x = 60; title.y = 140;
slide.appendChild(title);

// Big stat — pick color based on sentiment
const statColor = SENTIMENT === "positive" ? C.forest : SENTIMENT === "warning" ? C.coral : C.text;
const num = figma.createText();
num.fontName = { family: "Inter", style: "Extra Bold" };
num.characters = STAT_NUMBER;  // e.g. "+247%"
num.fontSize = 240;
num.textAlignHorizontal = "CENTER";
num.fills = [PAINT(statColor)];
num.x = 0; num.y = 540;
num.resize(1080, 280);
slide.appendChild(num);

// Caption
const cap = figma.createText();
cap.fontName = { family: "Inter", style: "Regular" };
cap.characters = STAT_CAPTION;
cap.fontSize = 32;
cap.textAlignHorizontal = "CENTER";
cap.fills = [PAINT(C.text)];
cap.x = 60; cap.y = 850;
cap.resize(960, 60);
slide.appendChild(cap);

makeAuthorBlock(slide, 60, 1350 - 72 - 60);
makeWordmark(slide, 1080 - 180 - 60, 1350 - 60 - 60);
```

### CTA recipe

```js
const slide = makeSlideFrame(lastIndex, "Slide / CTA");
figma.currentPage.appendChild(slide);

// NO swipe arrow on CTA

// Big headline stack
const stack = figma.createAutoLayout("VERTICAL", { itemSpacing: 24, name: "CTA Headline" });
stack.fills = [];
stack.x = 60; stack.y = 280;
stack.resize(960, 400);
stack.layoutSizingHorizontal = "FIXED";
stack.layoutSizingVertical = "HUG";
slide.appendChild(stack);

const row = figma.createAutoLayout("HORIZONTAL", { itemSpacing: 20 });
row.fills = [];
row.counterAxisAlignItems = "CENTER";
stack.appendChild(row);

const plain = figma.createText();
plain.fontName = { family: "Inter", style: "Extra Bold" };
plain.characters = HEADLINE_PLAIN;  // e.g. "Found this"
plain.fontSize = 96;
plain.fills = [PAINT(C.text)];
row.appendChild(plain);

row.appendChild(makeHighlightedText(HEADLINE_HL, "Extra Bold", 96));  // e.g. "useful?"

// Body prompt
const body = figma.createText();
body.fontName = { family: "Inter", style: "Regular" };
body.characters = BODY_PROMPT;
body.fontSize = 32;
body.fills = [PAINT(C.text)];
body.x = 60; body.y = 760;
body.resize(960, 80);
slide.appendChild(body);

// Action coral block
const action = makeHighlightedText(ACTION_TEXT, "Extra Bold", 56, {top: 14, bottom: 14, left: 24, right: 24});
action.x = 60; action.y = 880;
slide.appendChild(action);

makeAuthorBlock(slide, 60, 1350 - 72 - 60);
makeWordmark(slide, 1080 - 180*1.3 - 60, 1350 - 60*1.3 - 60, 1.3);
```

## Pitfalls to avoid

- **Font style strings**: Use `Extra Bold` (with space), NOT `ExtraBold`. Same for `Semi Bold`. Failing this throws "Cannot write to node with unloaded font".
- **Colors are 0-1 range**, never 0-255. Divide by 255 if needed.
- **Position new frames away from (0,0)** — use `index * 1180` x-offset for slide layout.
- **One use_figma call = atomic**. If it errors, NOTHING is committed. So batch 2-3 slides max per call.
- **Always `return` something** with createdNodeIds — needed for follow-up calls.
- **Don't load library variables/components** unless Foundations file is published. Inline hex colors + bake structure into each slide.
- **Highlight discipline**: 1-2 coral hl words per cover MAX, 1 per CTA action. Over-highlighting kills the design.
- **«Одна думка = один слайд»**: enforce strictly. If a slide has 2 main points, split it.

## Output template (what to return to Viktor at the end)

```
✅ Карусель готова — [N] слайдів

🔗 Figma: [file_url]

[Slide 1 PNG inline]
[Slide 2 PNG inline]
...

📥 Export PNG: відкрий файл → виділи всі слайди → правий клік → Export → PNG.

Що хочеш покращити? Можу:
- Переписати конкретний слайд
- Додати/прибрати слайд
- Замінити stat-метрику
- Інший варіант coral-highlight
```
