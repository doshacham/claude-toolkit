---
date: <% tp.date.now("YYYY-MM-DD") %>
tags:
  - daily
---
# <% tp.date.now("dddd, Do MMMM YYYY") %>

Yesterday: [[<% tp.date.yesterday("YYYY-MM-DD") %>]]
Tomorrow: [[<% tp.date.tomorrow("YYYY-MM-DD") %>]]

## Tasks
- [ ] <% tp.file.cursor(1) %>

## Notes
<% tp.file.cursor(2) %>

## Log
