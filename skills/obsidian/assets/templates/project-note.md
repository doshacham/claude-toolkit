<%*
const name = await tp.system.prompt("Project name");
const statuses = ["planning", "active", "on-hold", "completed", "archived"];
const status = await tp.system.suggester(statuses, statuses, false, "Status");
await tp.file.rename(name);
-%>
---
type: project
status: <% status %>
created: <% tp.date.now("YYYY-MM-DD") %>
tags:
  - project
---
# <% name %>

## Overview
<% tp.file.cursor(1) %>

## Goals
- [ ] <% tp.file.cursor(2) %>

## Tasks

## Notes

## References
