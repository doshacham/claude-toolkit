---
type: weekly-review
week: <% tp.date.now("gggg-[W]ww") %>
date_range: <% tp.date.weekday("YYYY-MM-DD", 0) %> to <% tp.date.weekday("YYYY-MM-DD", 6) %>
tags:
  - review
  - weekly
---
# Weekly Review - <% tp.date.now("gggg-[W]ww") %>

<% tp.date.weekday("YYYY-MM-DD", 0) %> to <% tp.date.weekday("YYYY-MM-DD", 6) %>

## Wins
- <% tp.file.cursor(1) %>

## Challenges
-

## Tasks completed this week

```tasks
done after <% tp.date.weekday("YYYY-MM-DD", 0) %>
done before <% tp.date.weekday("YYYY-MM-DD", 6) %>
sort by done
```

## Carry-over tasks

```tasks
not done
due before <% tp.date.weekday("YYYY-MM-DD", 6) %>
sort by due
limit 15
```

## Notes created this week

```dataview
LIST file.ctime
WHERE file.cday >= date("<% tp.date.weekday("YYYY-MM-DD", 0) %>")
  AND file.cday <= date("<% tp.date.weekday("YYYY-MM-DD", 6) %>")
SORT file.ctime DESC
```

## Focus for next week
- [ ] <% tp.file.cursor(2) %>

## Reflections
<% tp.file.cursor(3) %>
