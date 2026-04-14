# Add License Header

When creating new files, add a copyright header as the first line(s) of the file.

## Header content

```
Copyright (c) 2026 Dor Shacham <dorishacham52@gmail.com>. All rights reserved.
SPDX-License-Identifier: Proprietary
```

## Comment style by language

Use the file's native comment syntax:

| Style | Languages |
|---|---|
| `//` | Go, C, C++, Java, JavaScript, TypeScript, Rust, Swift, Kotlin, C# |
| `#` | Python, Ruby, Shell, Bash, Nix, YAML, Perl, R, PowerShell |
| `--` | SQL, Lua, Haskell |
| `/* */` | CSS |
| `<!-- -->` | HTML, XML, SVG, Markdown |
| `%` | LaTeX, Erlang |
| `;;` | Lisp, Clojure |
| `rem` | Batch |

## Rules

- Header goes on the very first line of the file (after shebang if present)
- One blank line between the header and the rest of the content
- Do NOT add headers to: `.json`, `.lock`, `.env`, `.gitignore`, `.md` (data/config files that don't support comments or where it's unconventional)
- If a file already has a copyright header, do not duplicate it
