---
name: read-article
description: This skill fetches and summarizes web articles, blog posts, and non-arxiv papers from a URL. Use when the user asks to "read this article", "summarize this blog post", "what does this page say", "digest this link", or provides a URL to a web article or documentation page.
---

You will be given a URL of an article or paper, for example:

https://lilianweng.github.io/posts/2023-06-23-agent/

### Part 1: Fetch the content

Try WebFetch first to retrieve and process the page content. If the result is empty, truncated, or the URL points to a PDF:

- For PDFs: download with `curl` (on Windows use `--ssl-no-revoke`) to a temp file, then read it with the Read tool
- For HTML that WebFetch struggles with: try `curl` to download the raw HTML, then process it

After fetching, validate that you actually got meaningful content — not a login wall, CAPTCHA, cookie banner, or error page. If the content looks incomplete or broken, inform the user and suggest alternatives (e.g. a cached version, different URL format, or manual paste).

### Part 2: Read and understand the content

Read through the full article content. If the article is long and was truncated, fetch additional sections or pages as needed. For multi-page articles, follow pagination links.

### Part 3: Ask about report style

Before writing the report, ask the user:

> Should this summary be **project-aware** (tied to the current project with borrowable ideas) or **standalone** (general-purpose summary)?

Use AskUserQuestion to let the user choose.

### Part 4: Report

Once you've read the article, produce a summary into a markdown file at `./knowledge/summary_{tag}.md`. Generate a reasonable `tag` based on the article's topic, like e.g. `agent_architectures` or `distributed_training_tricks` — whatever fits. Make sure the tag doesn't already exist so you're not overwriting files.

If the user chose **project-aware**: remember that you're processing this article within the context of the current project repository, so most often we will be interested in how to apply the article and its lessons to this project. Therefore, you should feel free to "remind yourself" of the related project code by reading the relevant parts, and then explicitly make the connection of how this article might relate to the project or what are things we might be inspired about or try.

If the user chose **standalone**: produce a clean, self-contained summary — the article's key ideas, contributions, and takeaways on their own merits without tying them to any specific project.
