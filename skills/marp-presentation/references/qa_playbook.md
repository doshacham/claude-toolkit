# QA Playbook — Playwright + Lint, with Loop

**This is the most important document in the skill.** The agent must not declare a deck done until it has executed this playbook end-to-end with zero errors.

The rule that trumps everything: **nothing on a slide may overlap anything else.** Not text over text. Not text clipped by an edge. Not a code block that extends past the slide. Not a diagram obscured by a header. If any element overlaps another, the deck is not done.

---

## The loop

```
┌─────────────────────────────────────────────────────┐
│   1. lint                                            │
│   2. render html                                     │
│   3. Playwright audit                                │
│   4. any errors?                                     │
│      yes → fix source → go to step 1                 │
│      no  → done                                      │
└─────────────────────────────────────────────────────┘
```

Never skip the loop. Never "ship with one known warning" unless the user explicitly accepts it. Iterate until the report is clean.

---

## Step 0 — Deterministic lint

```bash
python "${CLAUDE_SKILL_DIR}/scripts/lint.py" --input ./deck.md --mode <mode> --format text
```

- Fix every **error** before moving on
- Fix every **warning** unless the user accepted it
- `info`-level findings are advisory

---

## Step 1 — Render HTML

```bash
python "${CLAUDE_SKILL_DIR}/scripts/render.py" --input ./deck.md --format html --allow-local-files
```

Confirm `./deck.html` exists and is non-empty. If render fails, check Marp frontmatter and theme name.

---

## Step 2 — Open with Playwright MCP

The presenter agent has Playwright MCP attached. Navigate to the rendered HTML:

```
file:///C:/Users/User/path/to/deck.html
```

Wait for `networkidle`. Set viewport to 1280×720 to match Marp's native slide size.

---

## Step 3 — Structural check

```javascript
// Slide count
document.querySelectorAll('section').length
```

Compare against your outline. Mismatch usually means a stray `---` inside a code block or a missing separator.

---

## Step 4 — Overflow detection (hard rule)

For each slide, run:

```javascript
(() => {
  const results = [];
  const sections = document.querySelectorAll('section');
  sections.forEach((s, i) => {
    const overflow = {
      slide: i + 1,
      verticalOverflow: s.scrollHeight - s.clientHeight,
      horizontalOverflow: s.scrollWidth - s.clientWidth,
      clientH: s.clientHeight,
      scrollH: s.scrollHeight,
    };
    if (overflow.verticalOverflow > 0 || overflow.horizontalOverflow > 0) {
      results.push(overflow);
    }
  });
  return results;
})()
```

**Any non-zero result is an error.** Fix by splitting slides, shrinking blocks, or removing content. Do not shrink the font.

---

## Step 5 — Overlap detection (the core rule)

For each slide, collect bounding boxes for every direct child of `<section>` and check that no two boxes overlap:

```javascript
(() => {
  const violations = [];
  const sections = document.querySelectorAll('section');

  function rectsOverlap(a, b) {
    return !(a.right  <= b.left  ||
             b.right  <= a.left  ||
             a.bottom <= b.top   ||
             b.bottom <= a.top);
  }

  sections.forEach((section, idx) => {
    const children = Array.from(section.children).filter(el => {
      const cs = getComputedStyle(el);
      if (cs.display === 'none' || cs.visibility === 'hidden') return false;
      if (el.tagName === 'HEADER' || el.tagName === 'FOOTER') return false;
      return true;
    });
    const boxes = children.map(el => ({
      el: el.tagName + (el.className ? '.' + el.className : ''),
      rect: el.getBoundingClientRect(),
    }));
    for (let i = 0; i < boxes.length; i++) {
      for (let j = i + 1; j < boxes.length; j++) {
        if (rectsOverlap(boxes[i].rect, boxes[j].rect)) {
          violations.push({
            slide: idx + 1,
            a: boxes[i].el,
            b: boxes[j].el,
            rectA: boxes[i].rect,
            rectB: boxes[j].rect,
          });
        }
      }
    }
  });
  return violations;
})()
```

**Any violation is an error.** Common causes and fixes:

| Cause | Fix |
|---|---|
| Code block extends past sibling bullets | Split slide or shorten code |
| Background image `bg right` clipping text | Resize background or shrink text column |
| Header/footer overlapping content | Reduce content margins or remove header for this slide |
| Absolute-positioned quote box over body | Remove absolute positioning; let it flow |
| Heading font too large for container | Theme scale too aggressive — reduce h1 em |

---

## Step 6 — Text clipping (edge check)

Detect text that's within the section but hidden by the section's own padding (partial clipping):

```javascript
(() => {
  const problems = [];
  document.querySelectorAll('section').forEach((s, idx) => {
    const sRect = s.getBoundingClientRect();
    const sStyles = getComputedStyle(s);
    const padTop = parseFloat(sStyles.paddingTop);
    const padRight = parseFloat(sStyles.paddingRight);
    const padBottom = parseFloat(sStyles.paddingBottom);
    const padLeft = parseFloat(sStyles.paddingLeft);
    const innerBox = {
      top: sRect.top + padTop,
      right: sRect.right - padRight,
      bottom: sRect.bottom - padBottom,
      left: sRect.left + padLeft,
    };
    s.querySelectorAll('h1, h2, h3, h4, p, li, pre, code, img').forEach(el => {
      const r = el.getBoundingClientRect();
      if (r.width === 0 || r.height === 0) return;
      const clipped = r.top < innerBox.top || r.bottom > innerBox.bottom ||
                      r.left < innerBox.left || r.right > innerBox.right;
      if (clipped) {
        problems.push({ slide: idx + 1, tag: el.tagName, text: (el.textContent || '').slice(0, 40) });
      }
    });
  });
  return problems;
})()
```

Any problem is an error. Fix the source.

---

## Step 7 — Screenshot each slide

Use the Playwright MCP `screenshot` tool per slide. Save to `./qa/slide_NN.png`. Review them visually:

- Text legible at intended zoom
- No obvious clipping at the edge
- Diagrams render (Mermaid, images)
- Theme looks correct (colors, fonts, spacing)
- Emojis render if used (some themes strip emoji color glyphs)

If a screenshot shows a visual problem the JS checks missed, fix the source.

---

## Step 8 — Accessibility (axe-core)

Inject axe from CDN and run:

```javascript
// Axe inject
await new Promise(r => {
  const s = document.createElement('script');
  s.src = 'https://unpkg.com/axe-core@4/axe.min.js';
  s.onload = r;
  document.head.appendChild(s);
});
const results = await axe.run(document);
return results.violations.filter(v => ['critical', 'serious'].includes(v.impact));
```

Report every critical/serious violation. Common:

- **image-alt** → add alt text to every `![...](...)` link
- **color-contrast** → theme problem; if consistent, swap theme or surface the trade-off to the user
- **heading-order** → don't skip h1 → h3

---

## Step 9 — Font + image health

```javascript
// Fonts
const fonts = Array.from(document.fonts).map(f => ({
  family: f.family, weight: f.weight, status: f.status
}));

// Broken images
const broken = Array.from(document.querySelectorAll('img'))
  .filter(img => !img.complete || img.naturalWidth === 0)
  .map(img => img.src);

return { fonts, broken };
```

All fonts must be `loaded`. No broken images. Any failure is an error.

---

## Step 10 — Link check (non-blocking)

Lint.py already does this. Re-confirm visually if the user cares:

```bash
python "${CLAUDE_SKILL_DIR}/scripts/lint.py" --input ./deck.md --format text
```

---

## Step 11 — Report

Produce a structured report:

```markdown
## QA Report — deck.md

**Pass count**: 2 (iteration 1, iteration 2)
**Slides**: 14 expected, 14 rendered. OK.
**Overflow**:    0 errors
**Overlap**:     0 errors
**Clipping**:    0 errors
**Accessibility**: 0 critical, 0 serious
**Fonts**: all loaded (Inter, JetBrains Mono)
**Images**: all loaded
**Links**: 12/12 OK

### Status
DONE. The deck is clean.
```

If any check fails, the report must look like:

```markdown
## QA Report — deck.md

**Pass count**: 1
**Status**: BLOCKED

### Errors
- Slide 7: overlap between H2 and PRE (code extends 42px past the next heading)
- Slide 11: vertical overflow (+28px)
- Slide 4: broken image ./charts/missing.png

### Actions
- Slide 7: split the code block in half, move the continuation to slide 7b
- Slide 11: rewrite the bullet list as two shorter slides
- Slide 4: fix image path or remove the slide

Re-running Playwright after fixes.
```

---

## Exit criteria (all must be true)

1. Lint: 0 errors
2. Slide count matches outline
3. Overflow: 0 violations
4. Overlap: 0 violations
5. Clipping: 0 violations
6. Accessibility: 0 critical, 0 serious
7. All fonts loaded
8. No broken images
9. Screenshots look clean to a human reviewer

Only then say "the deck is done". Never before.

---

## When to reconsider the theme

Sometimes the loop won't converge because the theme itself is wrong for the content. Symptoms:

- Repeated overflow errors on multiple slides regardless of source edits
- Accessibility (color-contrast) failures on most slides
- Screenshots look cluttered even after trimming content

In that case, **stop the loop and re-propose themes.** Read `references/themes.md` and present 3 alternatives ranked for the current content. Let the user pick. Then restart the loop.

The loop is not meant to force a bad theme to work. It's meant to verify a good theme is rendering cleanly.
