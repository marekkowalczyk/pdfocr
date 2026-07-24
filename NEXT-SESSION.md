# Next Session

**Released as [v1.3.0](https://github.com/marekkowalczyk/pdfocr/releases/tag/v1.3.0)** (2026-07-24).

v1.3.0 added the `-f`/`--fast` path: extract the PDF's embedded text layer via
`pdftotext` (poppler) instead of calling the OCR API — free, offline, plain
`.txt` output, no API key. It does no quality check by design; the user
decides when a text layer is trustworthy. Poppler is an optional runtime dep
(only needed for `-f`), deliberately kept out of `requirements.txt`.

See `BACKLOG.md` for unscoped future ideas (`--model` override, OCR
annotations/bounding boxes, content-hash caching). One follow-up worth noting:
`-f` currently has no automated tests (deliberate — user owns the judgment
call). If it ever grows a quality heuristic or auto-fallback to OCR, add
coverage then.

## System note

Shebang is `#!/usr/bin/env python3` — the script re-execs itself under this
project's own `.venv/bin/python3` (see `CLAUDE.md`). Do not hardcode an
absolute interpreter path in the shebang.
