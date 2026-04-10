# Newspaper Writing Guide for Dev-Blog Articles

This reference provides detailed techniques for writing dev-blog articles that read like
newspaper features — not technical documentation.

## The Inverted Pyramid

Newspaper journalism front-loads the most important information. Apply this to dev-blog
writing:

1. **Lead** — The core insight or tension (first 2–3 sentences)
2. **Nut graph** — Why this matters, what the article will deliver (paragraph 2)
3. **Supporting detail** — The evidence, examples, code (body)
4. **Background** — Context that enriches but isn't essential (later sections)
5. **Kicker** — A resonant closing line (final sentence)

A reader who stops after the lead should still get the point. A reader who finishes should
feel they gained something substantial.

## Headline Craft

### Anatomy of a Good Headline

A dev-blog headline must do two things: describe the content accurately and create enough
tension to earn a click.

**Patterns that work:**

| Pattern | Example |
|---------|---------|
| How + specific outcome | "How One Function Eliminated 80% of Our API Errors" |
| The Case For/Against | "The Case Against Dependency Injection in CLI Tools" |
| Gerund + surprising object | "Building a Database in 500 Lines of Rust" |
| Question that implies answer | "Why Does Every Go Project Reinvent Configuration?" |
| Contrarian claim | "Your ORM Is Doing More Harm Than Good" |
| X + Without + Y | "Type Safety Without Code Generation" |

**Patterns to avoid:**

- "A Deep Dive Into X" — overused, vague
- "Everything You Need to Know About X" — clickbait, never delivers
- "X: A Comprehensive Guide" — this is an article, not a guide
- "Introducing X" — only works if the reader already cares about X

### Headline Rules

- Keep under 12 words when possible
- Use active verbs ("Replaced", "Eliminated", "Built") over passive ("Was Improved")
- Name the technology or domain to attract the right audience
- Avoid jargon that only insiders understand — the headline must work for a broader
  developer audience

## Lead Writing

The lead paragraph is the article's handshake. It must accomplish three things in 2–3
sentences:

1. Establish what this is about
2. Create tension or curiosity
3. Signal that reading further will be worth the time

### Lead Patterns

**Anecdotal Lead** — Start with a concrete scene or moment:

> Every Friday at 3pm, the deploy queue backed up. Three engineers would spend the next
> hour babysitting a shell script that hadn't been updated since 2019. The script worked —
> mostly. When it didn't, nobody knew why.

**Declarative Lead** — State the thesis directly:

> Most ORMs solve a problem that doesn't exist anymore. With modern SQL tooling and
> type-safe query builders, the abstraction layer costs more than it saves.

**Contrarian Lead** — Challenge received wisdom:

> The conventional wisdom says microservices scale better than monoliths. This project
> started as microservices, hit a wall at 50 requests per second, and became a monolith
> that handles 10,000.

**Mystery Lead** — Pose a question the article will answer:

> A single TypeScript function, 47 lines long, eliminated an entire category of production
> bugs. It wasn't clever. It wasn't complex. It just enforced something the team had been
> ignoring.

### Lead Anti-Patterns

Never open with:

- "In this article, we will explore..." — passive, boring, tells instead of shows
- "X is a Y that does Z" — dictionary definition, not a story
- "In today's fast-paced world..." — meaningless filler
- "Have you ever wondered..." — condescending rhetorical question
- A dictionary definition of any term

## Weaving Technical Detail into Narrative

The central challenge of dev-blog writing: include enough technical depth to be valuable
without losing readers in a code walkthrough.

### The Sandwich Technique

Wrap every technical section between narrative slices:

1. **Context** (1–2 sentences) — Why does this matter? What problem does it solve?
2. **Technical detail** — The code, the architecture decision, the pattern
3. **Implication** (1–2 sentences) — So what? What does this enable or prevent?

**Example:**

> The authentication middleware had a subtle bug: it validated tokens on every request but
> cached the validation result using the token itself as the key. When tokens rotated, the
> cache grew unbounded.
>
> ```typescript
> const cache = new Map<string, AuthResult>();
> // This map never shrinks — every rotated token stays forever
> ```
>
> Replacing the token-keyed cache with a time-based LRU cut memory usage by 60% and
> eliminated the mysterious OOM crashes that had plagued the service for months.

Without the narrative wrapper, the code snippet means nothing. Without the code, the
narrative is vague.

### Code Snippet Rules

- **Maximum 25 lines.** If the snippet is longer, extract the essential part and note
  what was trimmed.
- **Always introduce.** Never drop a code block without explaining what the reader is
  about to see.
- **Always follow up.** After the snippet, explain what it proves or enables.
- **Use real code.** Pull from the actual codebase. Fabricated examples undermine trust.
- **Trim boilerplate.** Remove imports, type annotations, and error handling that don't
  serve the point. Use `// ...` to indicate omissions.
- **Annotate inline** when the logic isn't obvious. One or two comments inside the
  snippet can guide the reader's eye.

### When NOT to Show Code

Skip the code snippet when:

- The point is about architecture, not implementation
- The insight is in the decision, not the syntax
- A diagram or description would be clearer
- The code is straightforward and the reader can imagine it

## Tone Calibration

### The Target Voice

Write like a senior engineer explaining something interesting to a peer over coffee.
Not lecturing. Not selling. Not dumbing down. Sharing.

**Characteristics:**

- **Confident but not arrogant.** State claims directly. "This approach eliminates X"
  not "We believe this approach might help reduce X."
- **Technical but accessible.** Use precise terminology but define niche terms on first
  use. Assume the reader knows how to code but may not know this specific domain.
- **Honest about tradeoffs.** The best dev-blog articles acknowledge what doesn't work.
  "This approach breaks down when..." builds more trust than "This solves everything."
- **Concise.** Every sentence must earn its place. If a paragraph can lose a sentence
  without losing meaning, cut it.

### Words and Phrases to Avoid

| Avoid | Why | Use Instead |
|-------|-----|-------------|
| "delves into" | AI tell | "examines", "covers", or just cut it |
| "it's important to note" | Padding | Just state the thing |
| "leverage" (as verb) | Corporate speak | "use" |
| "utilize" | Same | "use" |
| "robust" | Meaningless without context | Describe what makes it robust |
| "seamless" | Almost never true | Describe the actual integration |
| "cutting-edge" | Subjective, dated | Name the specific technology |
| "paradigm shift" | Overblown | Describe the actual change |
| "ecosystem" | Vague | Name the specific tools/libraries |
| "in the ever-evolving landscape" | Terminal AI fluff | Delete entirely |

## Paragraph Structure

### Length

- Target 3–5 sentences per paragraph
- Single-sentence paragraphs work for emphasis — use sparingly (once or twice per article)
- Never exceed 7 sentences in one paragraph

### Transitions

Connect paragraphs with logical flow, not transition phrases. The last sentence of one
paragraph should naturally lead to the first sentence of the next.

**Weak transition:** "Moving on to the next topic, let's discuss the database layer."

**Strong transition:** End paragraph about API design with a hint about data persistence.
Start next paragraph with the database decision.

### The "So What" Test

After writing each paragraph, ask: "If a reader stopped here, would they have gained
something?" If not, the paragraph needs a sharper point or should be merged with
the next one.

## Closing Techniques

### The Kicker

The last sentence should resonate. It's the line the reader remembers.

**Techniques:**

- **Circle back** to the opening image or problem, showing how it's resolved
- **Zoom out** from the specific project to a general principle
- **End on a question** that the reader takes away to think about
- **State the lesson** in its most compressed form

**Examples:**

> The Friday deploy queue is empty now. Not because the script got better — because
> it got deleted.

> Sometimes the best architecture decision is the one that makes your code boring.

> The next time you reach for a framework, ask what you're afraid of building yourself.

### Closings to Avoid

- "In conclusion..." — the reader knows it's the conclusion
- Summarizing everything just said — wastes the reader's time
- "I hope this was helpful" — undermines authority
- A call to action to star the repo — this is an article, not a README
