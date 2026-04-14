<%*
const topic = await tp.system.prompt("Concept name");
const slug = topic.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
await tp.file.rename(slug);
-%>
---
title: <% topic %>
type: concept
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
sources: []
tags: []
---
# <% topic %>

<% tp.file.cursor(1) %>

## Key properties

-

## Related concepts

-

## Open questions

- <% tp.file.cursor(2) %>
