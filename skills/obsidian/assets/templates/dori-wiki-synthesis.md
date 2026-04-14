<%*
const topic = await tp.system.prompt("Synthesis topic");
const slug = topic.toLowerCase().replace(/\s+/g, '-').replace(/[^a-z0-9-]/g, '');
await tp.file.rename(slug);
-%>
---
title: <% topic %>
type: synthesis
created: <% tp.date.now("YYYY-MM-DD") %>
updated: <% tp.date.now("YYYY-MM-DD") %>
sources: []
tags: [synthesis]
---
# <% topic %>

## Thesis

<% tp.file.cursor(1) %>

## Evidence

### From [[sources/]]

-

### From [[sources/]]

-

## Analysis

<% tp.file.cursor(2) %>

## Conclusions

-

## Open questions

- <% tp.file.cursor(3) %>
