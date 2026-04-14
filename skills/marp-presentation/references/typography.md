# Typography System

The baseline every theme inherits from, and the rules the agent enforces while authoring slides. Read this when designing a new theme or when the layout feels off.

## Baseline constants

Marp renders slides at **1280 × 720 px** by default (16:9). The `default` theme sets `section { font-size: 35px }`. Every bundled theme extends `default` via `@import 'default';` and overrides to `font-size: 24px` for compact, professional slides that avoid overflow. Two documented exceptions: **neon** (22px — glow headings are oversized, body text compensates) and **high_contrast** (26px — accessibility-first, large-venue legibility). All themes set `overflow-y: auto` as a safety net for edge cases.

| Constant | Value | Why |
|---|---|---|
| Base font size | 24px | Compact enough for dense content while remaining legible on projection |
| Body line-height | 1.5 | Optimal for slide reading distance |
| Heading line-height | 1.2 | Tight, confident headlines |
| Code/pre font-size | 0.85em (~20px) | Legible code without dominating |
| Vertical padding | 40-48px | Maximizes content area within 720px viewport |
| Horizontal padding | 52-64px | 55-70 character line length |
| Max line length | ~65 chars | Reading research optimum |

## The typographic scale

Per-theme scale (approximate — themes can deviate for effect):

| Element | Scale | Weight |
|---|---|---|
| h1 (content) | 1.5-1.8em | 700-800 |
| h1 (lead slide) | 2.0-3.6em | 800-900 |
| h2 | 1.15-1.4em | 600-700 |
| h3 | 1.0-1.15em | 500-600 |
| body | 1em | 400 |
| code/pre | 0.85em | 400 |
| footnotes / small | 0.75em | 400 |
| header/footer | 0.75-0.8em | 300-400 |

## Color contrast (WCAG AA minimums)

Every theme must meet these for body text:

- **Normal text (body)**: 4.5:1 against background
- **Large text (h1/h2)**: 3:1 against background
- **Interactive elements (links, buttons)**: 3:1 against background

Themes that need extra attention for contrast:

- **neon** — hot pink/cyan glows look great for headings; body text uses a softer `#e9d5ff` to meet 4.5:1 against `#0a0015`
- **terminal** — green-on-black is high contrast (19:1), but scanline overlay must not knock it below 4.5:1; capped at 1.8% alpha
- **gradient** — white on sunset gradient is borderline in the amber zone; bold text used for body
- **kraft** — dark ink on kraft paper meets 4.5:1; handwritten font weight helps

## Font stacks

Themes use Google Fonts for primary typefaces, with system fallbacks. All theme CSS files import their fonts at the top:

```css
/* @theme midnight */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&family=JetBrains+Mono:wght@400;600&display=swap');
@import 'default';
```

| Theme | Primary font | Fallback |
|---|---|---|
| midnight | Inter + JetBrains Mono | system-ui, Cascadia Mono |
| paper | Georgia (system) | Times New Roman, serif |
| terminal | JetBrains Mono (system if available) | Cascadia Mono, Consolas |
| corporate | Inter | -apple-system, Segoe UI |
| brutalist | Helvetica Neue (system) | Helvetica, Arial |
| neon | Inter | system-ui |
| academic | EB Garamond | Georgia, Times New Roman |
| dashboard | Inter + JetBrains Mono | system-ui |
| minimal | Inter | -apple-system |
| gradient | Inter | system-ui |
| blueprint | Courier New (system) | JetBrains Mono, monospace |
| monochrome | Helvetica Neue (system) | Helvetica, Arial |
| kraft | Kalam | Comic Sans MS, Marker Felt |
| high_contrast | Atkinson Hyperlegible | Verdana, Arial |
| pastel | Nunito | Quicksand, Inter |

## Authoring rules (the agent must follow these)

### 1. Never overlay content

The **most important rule**. Nothing on a slide should overlap anything else. No text over a background image where the text becomes unreadable. No two elements sharing screen space if one obscures the other. If an overlay is intentional (e.g. a quote over a hero image), the Playwright QA loop must confirm the text still passes contrast.

### 2. Respect the content budget

Per-slide content budget (rough):

| Element | Max |
|---|---|
| h1 | 1 per slide |
| h2 | 3 (usually 1) |
| Bullets | 5 |
| Source lines (total) | 25 |
| Code block height | half the slide |
| Images | 1 hero + 1 inline, max |

The `lint.py` script enforces these as warnings.

### 3. Pick ONE accent color per slide

Each theme defines 3-5 accent colors. On any given slide, use only ONE dominant accent plus the body text color. Three accents on one slide = visual noise.

### 4. Leave breathing room

If a slide feels "full", it IS full. Split it. Eight slides that breathe beat four that are packed.

### 5. Titles as sentences, not topics

`lint.py` flags topic-style titles. Prefer "We lost 12% of sessions after the rewrite" over "Session metrics".

## When to deviate from the baseline

Acceptable reasons to override the system:

- **Lead/hero slides** — larger font for the title slide is canon
- **Big-number slides** — data-mode hero numbers can be 5-7em
- **Quote slides** — one big quote can break the 5-bullet rule (it's not a bullet)
- **Intentional Swiss-grid aesthetic** — `brutalist`, `monochrome` use scale for statement

Unacceptable reasons to override:

- "The content won't fit" — that's a signal to split the slide, not shrink the type
- "I wanted it to look different" — pick a different theme instead
- "The client likes big logos" — put the logo in header/footer
