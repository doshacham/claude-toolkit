---
description: Explain a concept
argument-hint: [topic or question]
allowed-tools: Read, Glob, Grep
---

# Learn: $ARGUMENTS

Explain the concept or answer the question: **$ARGUMENTS**

## Instructions

Follow the explanation methodology from the `explanation-methodology` skill. Structure the explanation with:

1. **One-line definition** — jargon-free, self-contained
2. **Analogy** — real-world metaphor that maps to the concept
3. **Core explanation** — what it is, how it works, why it exists
4. **Practical example** — minimal, concrete, annotated (code snippet for programming topics)
5. **Key takeaways** — 2-4 bullet points, independently useful
6. **Related concepts** — 2-3 terms to explore next (if relevant)

## Output

Present the full explanation directly in the conversation.

## Edge Cases

- If `$ARGUMENTS` is empty, ask the user what concept they want to learn about using AskUserQuestion
- If the topic is ambiguous (e.g., "pool" could be thread pool, connection pool, or swimming pool), ask for clarification
- If the topic is a comparison ("X vs Y"), use the comparison format: define both, comparison table, when to use each
- If the topic is procedural ("how to X"), use the procedural format: summary, prerequisites, steps, verification
