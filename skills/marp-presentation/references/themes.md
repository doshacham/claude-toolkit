# Theme Catalog

15 hand-tuned Marp themes, each with its own aesthetic and intended use cases. When starting a new deck, present the user with a **ranked, reasoned list** of themes that fit the detected mode. Never silently pick.

All themes are registered via Marp's `--theme-set` (the `render.py` script handles this automatically). Reference them in frontmatter as `theme: <name>`.

---

## The 15 themes

### 1. midnight
**Vibe**: Deep navy background, cyan and magenta accents, Inter type, gradient lead slides.
**Audience**: Internal engineering, polished tech-product demos.
**Feels like**: Modern developer dashboard crossed with a design-system launch.
**Modes**: technical, architecture.
**Avoid when**: presenting to non-technical executives — too dark for a boardroom.

### 2. paper
**Vibe**: Warm cream background, ink-black Georgia serif, generous margins, editorial.
**Audience**: Research, writing-centric decks, book-club style discussions.
**Feels like**: A New Yorker long-form feature spread.
**Modes**: research, onboarding.
**Avoid when**: you need heavy code blocks — the serif fights monospace.

### 3. terminal
**Vibe**: Pure black, phosphor-green monospace, CRT scanline overlay, text-shadow glow.
**Audience**: Engineers who grew up on vim. Security/infra/low-level talks.
**Feels like**: Watching someone SSH into a legacy mainframe.
**Modes**: technical, architecture.
**Avoid when**: accessibility matters — green-on-black fails contrast in edge cases.

### 4. corporate
**Vibe**: White background, navy accents, Inter sans, zebra-striped tables, clean grid.
**Audience**: External stakeholders, executives, investors.
**Feels like**: A McKinsey deck that was actually designed.
**Modes**: narrative, data, onboarding.
**Avoid when**: you want the deck to feel personal or edgy.

### 5. brutalist
**Vibe**: Stark black-and-white, Helvetica 900, thick borders, text-as-art.
**Audience**: Design-forward teams, launches, editorial statements.
**Feels like**: A Swiss design-school thesis. Bauhaus ghost.
**Modes**: narrative.
**Avoid when**: the content is dense — brutalism wants white space.

### 6. neon
**Vibe**: Pitch-black background, hot pink and cyan glow text, oversized headings.
**Audience**: Product launches, gaming, crypto, consumer demos.
**Feels like**: A Blade Runner neon sign.
**Modes**: narrative.
**Font size**: 28px (below 30px baseline -- glow headings are oversized, so body text is pulled in tighter for balance).
**Avoid when**: you're presenting in a bright room (glow fades) or to a conservative audience.

### 7. academic
**Vibe**: Cream paper, EB Garamond small-caps, proper footnotes, math-friendly.
**Audience**: Academic conferences, PhD defenses, research groups.
**Feels like**: A published paper rehearsed for a colloquium.
**Modes**: research.
**Avoid when**: the audience wants energy — this is intentionally restrained.

### 8. dashboard
**Vibe**: Slate gray, giant tabular numerics, green accent bars, KPI hero slides.
**Audience**: Executive briefings, metrics reviews, ops teams.
**Feels like**: A Grafana board grown up into a slide deck.
**Modes**: data.
**Avoid when**: the deck is narrative — the numerical focus feels cold.

### 9. minimal
**Vibe**: Pure white, huge whitespace, thin Inter-light headings, em-dash bullets.
**Audience**: Design reviews, product vision, Apple-style restraint.
**Feels like**: A Jony Ive keynote.
**Modes**: research, onboarding, data.
**Avoid when**: you have more than one idea per slide.

### 10. gradient
**Vibe**: Sunset gradients (indigo → magenta → amber), glassmorphism cards.
**Audience**: Pitches, launches, marketing, SaaS decks.
**Feels like**: A 2024 Y Combinator demo day.
**Modes**: narrative, onboarding.
**Avoid when**: the content is technical — gradients distract from code.

### 11. blueprint
**Vibe**: Cyan grid on navy, courier monospace, bracketed headings, technical drawing.
**Audience**: Architecture reviews, systems design, infra.
**Feels like**: An engineering drafting table.
**Modes**: architecture, technical.
**Avoid when**: the deck has photos — the grid fights images.

### 12. monochrome
**Vibe**: Grayscale Swiss grid, Helvetica Neue, zebra tables, headline borders.
**Audience**: Research, editorial, design-conscious technical decks.
**Feels like**: A Massimo Vignelli subway map pitch.
**Modes**: research, technical, data.
**Avoid when**: you want color to carry meaning.

### 13. kraft
**Vibe**: Brown paper background, Kalam handwritten font, dashed borders, sticky-note accents, subtle rotation.
**Audience**: Workshops, design jams, retrospectives, new-hire welcomes.
**Feels like**: A whiteboarding session photographed.
**Modes**: onboarding.
**Avoid when**: the audience is skeptical of "playful" — some exec rooms reject it.

### 14. high_contrast
**Vibe**: Pure white + pure black, Atkinson Hyperlegible font, yellow highlights, maximum WCAG.
**Audience**: Accessibility-first presentations, public sector, large venues.
**Feels like**: A keynote engineered for the back row.
**Modes**: any.
**Font size**: 32px (above 30px baseline -- deliberately oversized for accessibility and large-venue legibility).
**Avoid when**: you want stylistic flair — this is function-first.

### 15. pastel
**Vibe**: Soft pink/blue/lavender radial backgrounds, Nunito rounded sans, wavy underlines.
**Audience**: Onboarding, creative work, lifestyle brands, educational.
**Feels like**: A modern children's-book illustration spread.
**Modes**: onboarding, narrative.
**Avoid when**: presenting to a skeptical technical audience.

---

## Mode → ranked theme recommendations

When the user picks a mode, present the top 5-6 themes **ranked with reasoning**. Format:

```
For mode TECHNICAL CODEBASE, here are the themes ranked:

1. terminal — pure black + green monospace. Use when the audience is engineers and the deck is 60%+ code.
2. midnight — dark navy, polished. Good default for internal tech talks.
3. blueprint — cyan grid, technical-drawing feel. Fits heavy-diagram decks.
4. monochrome — grayscale Swiss grid. Neutral, editorial.
5. corporate — white + navy. Use when presenting to non-technical stakeholders.
6. high_contrast — WCAG AAA. Use when legibility is non-negotiable.

Which should I use? (Name, number, or say "pick" for #1.)
```

### Technical codebase
1. **terminal** — engineers will feel at home; code is the star
2. **midnight** — more polished than terminal, still technical
3. **blueprint** — best when the deck has many diagrams
4. **monochrome** — neutral, editorial, lets code breathe
5. **corporate** — when mixed audience (tech + exec)
6. **high_contrast** — when legibility is non-negotiable

### Research paper
1. **academic** — purpose-built for this
2. **paper** — warmer, less stiff
3. **minimal** — when the audience wants restraint
4. **monochrome** — Swiss editorial feel
5. **high_contrast** — conferences with big rooms

### Narrative pitch
1. **neon** — maximum energy, launches
2. **gradient** — modern SaaS pitch
3. **brutalist** — editorial statement
4. **corporate** — investor meetings
5. **pastel** — consumer/creative brands

### Data briefing
1. **dashboard** — purpose-built for KPIs
2. **corporate** — executive readiness
3. **minimal** — when numbers should breathe
4. **monochrome** — editorial analysis
5. **high_contrast** — public-sector reviews

### Onboarding
1. **paper** — warm welcome feel
2. **minimal** — clean, uncluttered
3. **corporate** — if brand-aligned
4. **pastel** — playful, lower-stakes teams
5. **kraft** — workshop/whiteboard vibe
6. **gradient** — modern SaaS cultures

### Architecture
1. **blueprint** — purpose-built
2. **terminal** — infra/systems programming
3. **midnight** — polished internal reviews
4. **dashboard** — scale/ops emphasis
5. **monochrome** — neutral editorial

---

## Adding a new theme

Drop a `<name>.css` file in `themes/` with the copyright header first, then `/* @theme <name> */` on the next line. Add the name to the `THEMES` set in `scripts/new_deck.py`. Document it in this file.

Themes should extend `default`:

```css
/* @theme my-theme */

@import 'default';

section {
  background: /* ... */;
  color: /* ... */;
  /* ... */
}
```
