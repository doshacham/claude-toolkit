<%*
const topic = await tp.system.prompt("MOC topic");
await tp.file.rename(topic);
-%>
---
type: moc
created: <% tp.date.now("YYYY-MM-DD") %>
tags:
  - moc
---
# <% topic %>

## Overview
<% tp.file.cursor(1) %>

## Core notes
- <% tp.file.cursor(2) %>

## Related MOCs

## Open questions
