# Next Session

**Released as [v1.2.0](https://github.com/marekkowalczyk/pdfocr/releases/tag/v1.2.0)** (2026-07-21).

No open backlog items from the Unix citizenship milestone — all implemented
(sysexits exit codes, 128+signum signals, stdin/batch input). See
`BACKLOG.md` for unscoped future ideas (`--model` override, OCR
annotations/bounding boxes, content-hash caching).

## System note

Shebang is `#!/usr/bin/env python3` — the script re-execs itself under this
project's own `.venv/bin/python3` (see `CLAUDE.md`). Do not hardcode an
absolute interpreter path in the shebang.
