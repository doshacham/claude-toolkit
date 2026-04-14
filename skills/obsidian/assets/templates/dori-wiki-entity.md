<%*
const name = await tp.system.prompt("Entity name (person, tool, project)");
const slug = name.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
await tp.file.rename(slug);
-%>
---
title: <% name %>
type: entity
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
sources: []
tags: []
---
# <% name %>

<% tp.file.cursor(1) %>

## Key facts

-

## Connections

- <% tp.file.cursor(2) %>
