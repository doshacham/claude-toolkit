# The Six Modes

Every presentation task maps to one of these six modes. Each has its own structure, rhythm, and set of slide archetypes. When in doubt which mode fits, ask the user.

Slide counts below are **targets**, not hard limits. The `lint.py` script warns when a deck is outside the band.

---

## 1. Technical codebase deep-dive

**Goal**: explain how a feature, subsystem, or module works to an audience of engineers.

**Budget**: 12-25 slides.

**Structure**:
1. **Title + TL;DR** — what this is, why it matters, one-sentence takeaway
2. **Context** — where this lives in the larger system
3. **The problem** — what forced this code into existence
4. **Architecture at a glance** — one Mermaid `flowchart` or `C4Container`
5. **Zoom 1** — the first component (code + file:line citations)
6. **Zoom 2** — the second component
7. **Zoom 3** — the third (stop at 3 unless necessary)
8. **Data flow** — one `sequenceDiagram` for the critical path
9. **Failure modes** — table of mode / trigger / mitigation
10. **Observability** — how we know when it breaks
11. **What we'd change** — retrospective honesty
12. **Takeaways** — one learning, one open question, one follow-up

**Slide archetypes**:
- Code block with file:line citations in comments
- Sequence diagram for API / protocol flows
- Failure mode table
- Before/after code contrasts

**Do**: Cite `file:line` for every claim. The audience must be able to jump straight from the slide to the code.

**Don't**: Dump entire function bodies. Show the 5 lines that matter.

**Recommended themes**: terminal, midnight, blueprint, monochrome, corporate, high_contrast.

---

## 2. Research paper to conference talk

**Goal**: turn a paper (often from `read-arxiv` summary) into a 10-20 minute talk.

**Budget**: 10-20 slides (~1 min/slide rule).

**Structure**:
1. **Title** — paper title, authors, venue
2. **Hook** — the one thing that would make a busy researcher stop scrolling
3. **Motivation** — why this problem matters
4. **Prior work** — 2-3 bullets, cite each
5. **Contribution** — three one-line statements
6. **Method** — the core idea, one equation max
7. **Method deep-dive** — one more slide if the method is non-trivial
8. **Experiments** — headline result table
9. **Ablations** — which components matter
10. **Qualitative results** — a telling example
11. **Limitations** — what it doesn't handle
12. **Future work** — directions
13. **Thank you + questions**

**Slide archetypes**:
- One-equation slide with plain-English gloss below
- Results table (bold the winning row)
- Qualitative example figure
- Ablation bar chart

**Do**: Check `./knowledge/summary_*.md` first — the `read-arxiv` skill may have already produced a summary. Read it before reading the paper yourself.

**Don't**: Reproduce every table from the paper. Pick the two that matter.

**Recommended themes**: academic, paper, minimal, monochrome, high_contrast.

---

## 3. Narrative storytelling deck

**Goal**: pitch / vision / launch / all-hands. Move an audience emotionally and get them to act.

**Budget**: 6-15 slides. Shorter is almost always better.

**Structure** (classic narrative arc):
1. **Hook** — one sentence that makes them lean in
2. **Status quo** — the world as it is
3. **Problem** — what hurts, who hurts, emotional stakes
4. **Why now** — what changed that makes this urgent
5. **The turn** — the insight that reframes the problem
6. **The solution** — what we are building
7. **How it works** — one slide, no more
8. **Proof** — quotes, numbers, early results
9. **The vision** — where this goes
10. **The ask** — what we need from this room

**Slide archetypes**:
- Big-type hero slides (one sentence, giant font)
- One-image slides (no text, image carries the weight)
- Customer quote slides
- Before/after contrasts
- One metric slide (the number, nothing else)

**Do**: Ask the user for the *hook* and the *ask* before outlining. If they can't articulate either, the deck isn't ready to write.

**Don't**: Bullet everything. Narrative decks breathe; bulleted decks suffocate.

**Recommended themes**: neon, gradient, brutalist, corporate, pastel.

---

## 4. Data to insight briefing

**Goal**: executive briefing — translate numbers into a recommendation.

**Budget**: 5-12 slides. Executives read fast.

**Structure**:
1. **Headline finding** — one sentence, giant number
2. **Where it came from** — data source + time window
3. **Supporting chart** — one, not three
4. **Drill-down 1** — by cohort
5. **Drill-down 2** — by channel / region / whatever matters
6. **Anomalies** — what the data didn't show that we expected
7. **Hypothesis** — what we think is causing it
8. **Recommendation** — what to do, by when, owner
9. **Next read** — what data to look at next week

**Slide archetypes**:
- Big-number slide (the headline KPI, nothing else)
- Single-chart slide (title = the finding in words)
- Cohort comparison table
- Recommendation slide (three action bullets max)

**Do**: Put the recommendation on slide 1 in the title. Executives may not reach slide 8. The rest is backup.

**Don't**: Label charts "Chart 1" — label them with the finding: "New users drove 73% of the lift".

**Recommended themes**: dashboard, corporate, minimal, monochrome, high_contrast.

---

## 5. Onboarding deck from repo

**Goal**: day-one deck for a new engineer joining a codebase.

**Budget**: 8-18 slides.

**Structure**:
1. **Welcome + what this project does** — one sentence
2. **Who uses it** — personas, scale, scope
3. **How money / value flows** — the business context
4. **Tech stack at a glance** — language, framework, DB, infra
5. **The repo map** — directory tree with one-liners
6. **The critical path** — what runs when a user does the primary action
7. **Local dev setup** — commands to get running
8. **How we deploy** — CI, environments, feature flags
9. **Where the bodies are buried** — known gotchas, weird workarounds, legacy zones
10. **First PR ideas** — good first issues
11. **Who to ask** — humans by area (placeholder for user to fill)
12. **Resources** — runbooks, dashboards, docs

**Slide archetypes**:
- Directory tree (ASCII or Mermaid `flowchart`)
- Command block (shell commands)
- Persona card (who uses this)
- "Here be dragons" gotcha slide

**Do**: Read the README first. Walk the top-level directories. Run the test suite locally if possible before writing this.

**Don't**: Assume a deep prior. This is day one. Explain acronyms.

**Recommended themes**: paper, minimal, corporate, gradient, pastel, kraft.

---

## 6. Architecture showcase

**Goal**: visualize and explain a system's architecture to technical reviewers.

**Budget**: 8-18 slides.

**Structure**:
1. **30-second summary** — what this system does
2. **Context diagram** — C4 level 1, the system + its neighbors
3. **Container diagram** — C4 level 2, services and data stores
4. **Key component 1** — C4 level 3, zoomed in
5. **Key component 2**
6. **Critical data flow** — `sequenceDiagram` for the main interaction
7. **Scale characteristics** — RPS, latency, data volume
8. **Reliability** — SLOs, failure domains, what can degrade
9. **Security** — authn/authz, secret management, threat model highlights
10. **Trade-offs** — what we chose and why, what we rejected
11. **What would we change** — known tech debt and the plan to address it

**Slide archetypes**:
- C4 context diagram (`C4Context`)
- C4 container diagram (`C4Container`)
- Sequence diagram for critical flows
- SLO table (metric / target / actual)
- Trade-off matrix (2x2 or quadrantChart)

**Do**: Use C4 zoom levels deliberately. Start wide, end narrow. Don't mix levels on one slide.

**Don't**: Draw boxes without labels. Every arrow needs a verb.

**Recommended themes**: blueprint, terminal, midnight, dashboard, monochrome.
