# Obsidian Tasks Reference

## Table of contents

1. Task metadata (emoji format)
2. Dataview bracket format (alternative)
3. Priority levels
4. Recurrence rules
5. Query block syntax
6. Filters
7. Example queries
8. Dataview interaction

---

## 1. Task metadata (emoji format)

Appended in any order to the end of a task line. Dates are always `YYYY-MM-DD`:

Note: These emoji characters are the actual syntax of the Tasks plugin -- they are functional signifiers, not decoration.

| Field | Emoji | Example appended to task line |
|---|---|---|
| Due date | `📅` | `📅 2026-04-15` |
| Scheduled | `⏳` | `⏳ 2026-04-14` |
| Start | `🛫` | `🛫 2026-04-13` |
| Created | `➕` | `➕ 2026-04-12` |
| Done | `✅` | `✅ 2026-04-12` (auto-added on `[x]`) |
| Cancelled | `❌` | `❌ 2026-04-12` (auto-added on `[-]`) |
| Recurrence | `🔁` | `🔁 every week` |
| Highest priority | `🔺` | (no date, just the emoji) |
| High priority | `⏫` | |
| Medium priority | `🔼` | |
| Low priority | `🔽` | |
| Lowest priority | `⏬` | |
| Id | `🆔` | `🆔 dcf64c` |
| Depends on | `⛔` | `⛔ dcf64c,0h17ye` |
| On completion | `🏁` | `🏁 keep` or `🏁 delete` |

Full line example (emoji format):
```
- [ ] Ship the release ⏫ 🛫 2026-04-13 ⏳ 2026-04-14 📅 2026-04-15 🔁 every 2 weeks
```

Full line example (Dataview bracket format):
```
- [ ] Ship the release [priority:: high] [start:: 2026-04-13] [scheduled:: 2026-04-14] [due:: 2026-04-15]
```

---

## 2. Dataview bracket format (alternative)

Tasks also parses Dataview-style inline fields:

| Emoji field | Bracket equivalent |
|---|---|
| Due | `[due:: 2026-04-15]` |
| Scheduled | `[scheduled:: 2026-04-14]` |
| Start | `[start:: 2026-04-13]` |
| Created | `[created:: 2026-04-12]` |
| Done | `[completion:: 2026-04-12]` |
| Cancelled | `[cancelled:: 2026-04-12]` |
| Priority | `[priority:: high]` (highest/high/medium/low/lowest) |
| Id | `[id:: dcf64c]` |
| Depends on | `[dependsOn:: dcf64c]` |

Use `[]` (key+value shown) or `()` (value only). Separate multiple fields with 2+ spaces or commas.

---

## 3. Priority levels

From highest to lowest: `highest`, `high`, `medium`, (normal = no priority), `low`, `lowest`.

---

## 4. Recurrence rules

All start with `every`, placed after the recurrence signifier:

| Rule | Example |
|---|---|
| Daily | `every day` / `every 3 days` |
| Weekly | `every week` / `every week on Monday` / `every week on Tuesday, Friday` |
| Bi-weekly | `every 2 weeks` |
| Weekdays | `every weekday` |
| Monthly | `every month on the 15th` / `every month on the last` / `every month on the last Friday` |
| Quarterly | `every 6 months on the 2nd Wednesday` |
| Yearly | `every year` / `every January on the 15th` |

Suffix `when done` anchors next date to completion date instead of original reference: `every week when done`.

A recurring task needs at least one of due/scheduled/start to work.

---

## 5. Query block syntax

Fenced `tasks` code block. Instructions are one per line, case-insensitive:

````
```tasks
not done
due before tomorrow
priority is high
path includes Projects/
sort by due
group by folder
limit 10
hide backlinks
```
````

---

## 6. Filters

### Status filters
`not done`, `done`, `done this week`, `done last month`

### Date filters
- `due before tomorrow`, `due after yesterday`, `due on 2026-04-15`
- `due on or before today`, `due on or after next Monday`
- Range: `due 2026-04-01 2026-04-30`, `due next week`, `happens this month`
- `has due date`, `no due date`, `has scheduled date`, `no start date`

### Content filters
`description includes text`, `heading includes text`, `path includes folder/`

### Tag filters
`tags include #work`, `tags do not include #draft`

### Priority filter
`priority is high`, `priority above medium`, `priority below normal`

### Boolean combinations
`(due after yesterday) AND (due before in two weeks)`, `(tags include #inbox) OR (path includes Inbox)`, `NOT (path includes Archive)`

### Custom function filter
`filter by function task.due.year === 2026`

### Display instructions
`sort by due`, `sort by priority`, `sort by path`, `group by folder`, `group by filename`, `group by heading`, `limit 10`, `limit groups 5`, `hide backlinks`, `hide task count`, `hide priority`, `hide edit button`, `show urgency`, `show tree`, `explain`

---

## 7. Example queries

````
```tasks
not done
due before tomorrow
sort by due
group by folder
```
````

````
```tasks
not done
(due after yesterday) AND (due before in two weeks)
(tags include #inbox) OR (path includes Inbox)
sort by priority
```
````

````
```tasks
done this month
sort by done
limit 20
```
````

````
```tasks
not done
priority is high
path includes Projects/
group by filename
limit 10
hide backlinks
```
````

---

## 8. Dataview interaction

- Dataview's `TASK` query is a separate system. Clicking a checkbox in Dataview results does NOT spawn the next recurrence -- always check from the source line or use `Tasks: Toggle Done`.
- As of Dataview 0.5.43, all Tasks emoji fields EXCEPT recurrence are queryable from Dataview.
- Enable Dataview's "Automatic Task Completion" + "Use Emoji Shortcut for Completion" to make Dataview write the same done-date format Tasks uses.
