# LinkedIn Design Skills

Two Claude Code skills that turn raw text into on-brand LinkedIn creatives **directly in Figma** via the Figma MCP:

- **`/infographic`** — single-image infographic 1080×1350 (comparison tables, step grids, donut/funnel/growth-curve/timeline charts)
- **`/linkedin-carousel`** — full carousel 1080×1350 (cover → content → stat → CTA slides)

They ship with a **placeholder brand** (coral disc avatar, "YOUR LOGO"). Fork, rebrand in ~5 min, done.

> These are the working skills behind [Viktor Shulha](https://victorshulga.com)'s LinkedIn content — released as a rebrandable template.

---

## Prerequisites

1. **Claude Code** installed.
2. **Figma desktop app** open + logged in, with the **local MCP server enabled** (`Figma → Preferences → Enable local MCP server`).
3. Figma MCP registered in Claude: `claude mcp add figma` → authorize.
   Check the tools appear: `use_figma`, `create_new_file`, `get_screenshot`, `whoami`, `upload_assets`.

The `figma-use` / `figma-create-new-file` skills these depend on are **shipped by the Figma MCP plugin itself** — you don't install them, they appear automatically once the MCP is connected.

---

## Install

```bash
curl -sL https://raw.githubusercontent.com/victor-shulga/linkedin-design-skills/main/install.sh | bash
```

Or manually:

```bash
git clone https://github.com/victor-shulga/linkedin-design-skills.git
cp -R linkedin-design-skills/skills/* ~/.claude/skills/
```

Restart Claude Code. Then just paste text and say `/infographic` or `/linkedin-carousel`.

---

## Rebrand in 5 minutes

Out of the box these produce **placeholder-branded** output. Swap these before you post.

> **No brand kit yet?** Your colours and fonts already live on your website — you just haven't written them down. Generate a full design system from your URL with
> **[design-system-generator](https://github.com/victor-shulga/design-system-generator)** — it extracts colours, fonts, spacing and even outputs LinkedIn artifacts (banner, post footer, carousel cover) in your brand. Take the hex + font pairing from there into the steps below.

Swap these before you post:

### 1. Assets — replace the PNGs in each skill's `assets/`
| File | What | Size |
|---|---|---|
| `avatar.png` | Your headshot on a coloured disc | 1080×1080 |
| `wordmark.png` | Your logo | ~200×100 |
| `cover-photo.png` *(carousel only)* | Cropped portrait for the cover slide | 590×1010 |

### 2. Plan key — your Figma team
Both skills use `team::YOUR_PLAN_KEY`. Get yours by running the `whoami` tool (it returns your `plans[].key`) and replace the placeholder, **or** just let the skill call `whoami` at runtime.

### 3. Asset hashes — must match your PNGs
The builders reference content-addressed image hashes. After replacing a PNG, update its hash (sha1 of the file):
| Skill · line | Constant |
|---|---|
| `infographic` · L113 | `IMG.avatar` |
| `linkedin-carousel` · L241 | avatar `imageHash` |
| `linkedin-carousel` · L223 | wordmark `imageHash` |
| `linkedin-carousel` · L363 | cover `imageHash` |

```bash
shasum -a 1 skills/infographic/assets/avatar.png   # → paste into IMG.avatar
```

### 4. Palette — the `const C = {...}` block (top of each skill)
```js
coral:  { r: 232/255, g: 90/255,  b: 79/255 }   // your accent
forest: { r: 46/255,  g: 125/255, b: 91/255 }   // your "positive"
text:   { r: 30/255,  g: 30/255,  b: 30/255 }   // your ink
```

### 5. Author strings
| Where | Change |
|---|---|
| `infographic` · L168 / `carousel` · L252 | `"Victor Shulga"` → your name |
| `infographic` · L174 | `"FRACTIONAL CRO"` → your role |
| `carousel` · L259 | `"Fractional CRO"` → your role |
| `infographic` · L150 | `"victorshulga.com"` → your domain |

That's it — everything else (layout engine, chart atoms, brand-rule enforcement) stays.

---

## Brand rules the skills enforce (worth keeping)

- Main title **ALL CAPS + centered**; coral highlight pills always have **white** text.
- White background only — no cream/off-white.
- One thought = one slide (carousel).
- Chart-first for infographics: if the data has a shape (proportion, drop-off, change over time), draw a chart, not a text grid.

---

## License

MIT — see [LICENSE](LICENSE). Rebrand freely. The placeholder assets are generic; no third-party brand is bundled.
