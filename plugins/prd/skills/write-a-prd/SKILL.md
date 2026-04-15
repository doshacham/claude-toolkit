---
name: write-a-prd
description: Create a PRD through structured user interview, covering problem, users, requirements, and success criteria, then submit as a GitHub issue. Use when user wants to write a PRD, create product requirements, document a feature spec, or mentions "PRD".
---

# Write a PRD

Create a Product Requirements Document through a structured interview with the user, then submit it as a GitHub issue.

## Process

### 1. Understand the domain

If the project has a codebase, briefly explore it to understand the existing product, tech stack, and conventions. This context helps ask better questions.

### 2. Interview the user

Conduct a structured interview to gather all the information needed for the PRD. Ask questions in logical groups, waiting for answers before proceeding.

**Round 1 — The Problem**

- What problem are you solving? Who has this problem today?
- What does the current experience look like (workarounds, pain points)?
- Why solve this now? What's the trigger or urgency?

**Round 2 — Users & Scope**

- Who are the target users? Are there distinct user types with different needs?
- What is IN scope and what is explicitly OUT of scope?
- Are there any hard constraints (technical, business, regulatory)?

**Round 3 — Requirements**

- Walk through the key user stories: "As a [user], I want to [action] so that [outcome]"
- For each story, ask about edge cases and error states
- What are the non-functional requirements (performance, security, accessibility)?

**Round 4 — Success & Dependencies**

- How will you measure success? What metrics matter?
- Are there dependencies on other teams, services, or features?
- What's the rough timeline or priority level?

Iterate until the user confirms all information is captured. If the user says "you decide" on any point, state your recommendation and get explicit confirmation.

### 3. Draft the PRD

Write the PRD using the template below. Be specific and concrete — avoid vague language.

<prd-template>
# PRD: <Feature Name>

## Problem statement

What problem this solves and why it matters now.

## Target users

Who benefits and how their needs differ (if multiple user types).

## User stories

Numbered list of user stories in "As a [user], I want to [action] so that [outcome]" format.

1. As a ..., I want to ... so that ...
2. As a ..., I want to ... so that ...

## Requirements

### Functional requirements

- Requirement 1
- Requirement 2

### Non-functional requirements

- Performance: ...
- Security: ...
- Accessibility: ...

## Scope

### In scope

- Item 1
- Item 2

### Out of scope

- Item 1
- Item 2

## Success criteria

- Metric 1: target
- Metric 2: target

## Dependencies

- Dependency 1
- Dependency 2

## Open questions

- Question 1
- Question 2
</prd-template>

### 4. Review with the user

Present the full PRD draft. Ask the user to review:

- Are the user stories complete and accurate?
- Is anything missing from scope?
- Do the success criteria make sense?

Iterate until the user approves.

### 5. Submit as GitHub issue

Create the PRD as a GitHub issue using `gh issue create`. Use the feature name as the issue title, prefixed with "[PRD]". Apply a "prd" label if the repo supports it.

Confirm the issue URL with the user.
