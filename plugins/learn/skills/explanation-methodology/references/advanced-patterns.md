# Advanced Explanation Patterns

## Adapting Depth by Audience

### Beginner-Friendly

- Lead with the analogy before the definition
- Skip implementation details in the core explanation
- Use longer, more narrative examples
- Define every technical term inline

### Intermediate

- Standard template order works well
- Include implementation-level details
- Show code examples with brief annotations
- Reference related concepts freely

### Expert-Level

- Lead with the precise technical definition
- Skip or shorten the analogy
- Focus on edge cases, trade-offs, and performance
- Compare with alternatives

## Domain-Specific Adjustments

### Programming Concepts

- Always include a code snippet in the example
- Use the most common language for that concept (e.g., JavaScript for closures, Python for decorators)
- Show both the "naive" and "correct" approach when relevant
- Mention language-specific quirks

### System Design Concepts

- Include a simple ASCII diagram when describing architecture
- Describe the flow of data or requests
- Mention scale considerations
- List common real-world implementations

### Math / Algorithm Concepts

- State the formal definition, then immediately rephrase in plain language
- Walk through a small worked example step-by-step
- State time/space complexity if applicable
- Compare with brute-force approach

## Handling "vs" Questions

When explaining "X vs Y":

1. One-line definition of each
2. Side-by-side comparison table (3-5 rows)
3. When to use X vs when to use Y
4. Common misconception about the difference

## Handling "How to" Questions

When the question is procedural ("how to do X"):

1. One-line summary of what will be accomplished
2. Prerequisites (if any)
3. Step-by-step instructions (numbered)
4. Verification step (how to confirm it worked)
5. Common pitfalls

## Handling Abstract Concepts

For concepts that are hard to pin down (e.g., "what is abstraction", "what is idempotency"):

1. Start with the formal definition
2. Give TWO analogies from different domains
3. Show a "before/after" example — what changes when the concept is applied
4. Explicitly state what the concept is NOT (common misconceptions)
