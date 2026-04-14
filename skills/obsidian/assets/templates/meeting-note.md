<%*
const attendee = await tp.system.prompt("Primary attendee");
-%>
---
type: meeting
date: <% tp.date.now("YYYY-MM-DD") %>
attendee: "<% attendee %>"
tags:
  - meeting
---
# Meeting - <% tp.date.now("YYYY-MM-DD HH:mm") %>

**Attendee:** <% attendee %>

## Agenda
<% tp.file.cursor(1) %>

## Discussion

## Action items
- [ ] <% tp.file.cursor(2) %>

## Follow-up
