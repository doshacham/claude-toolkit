<%*
const topic = await tp.system.prompt("Topic");
const types = ["concept", "reference", "fleeting", "permanent"];
const type = await tp.system.suggester(types, types, false, "Note type");
const uid = tp.date.now("YYYYMMDDHHmmss");
await tp.file.rename(`${uid} ${topic}`);
-%>
---
id: <% uid %>
type: <% type %>
tags:
  - <% type %>
created: <% tp.date.now("YYYY-MM-DD") %>
---
# <% topic %>

<% tp.file.cursor() %>

---
## References
