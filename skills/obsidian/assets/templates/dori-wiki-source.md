<%*
const title = await tp.system.prompt("Source title");
const author = await tp.system.prompt("Author");
const url = await tp.system.prompt("URL (or leave blank)", "");
const slug = title.toLowerCase().replace(/[^a-z0-9\s-]/g, '').replace(/\s+/g, '-').slice(0, 60);
await tp.file.rename(slug);
-%>
---
title: "<% title %>"
type: source
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
sources: [<% slug %>]
tags: []
---
# <% title %>

**Author:** <% author %>
**Published:** <% tp.file.cursor(1) %>
<%* if (url) { -%>
**URL:** <% url %>
<%* } -%>
**Local copy:** `raw/<% tp.file.cursor(2) %>`

## Summary

<% tp.file.cursor(3) %>

## Key claims

-

## Entities and concepts referenced

-

## Open questions

-
