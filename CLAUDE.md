# CLAUDE.md

CLI tool that extracts text from PDFs using the Mistral OCR API and outputs Markdown.

See [README.md](README.md) for installation, usage, and configuration — this file only carries notes that don't belong in user-facing docs.

## Project structure

- `pdfocr` — single-file Python script, symlinked to `/usr/local/bin/`
- `requirements.txt` — pinned runtime dependencies (`requests`, `python-dotenv`)
- `requirements-dev.txt` — adds `pytest` for running `tests/`
- `tests/` — black-box CLI tests (invoke the script as a subprocess)
- `.venv/` — project-local virtual environment (git-ignored)
- `~/.env` — API key (outside the repo, not git-ignored since it's not tracked)

## Notes

- Shebang is `#!/usr/bin/env python3`; the script re-execs itself under this project's own `.venv/bin/python3` (resolved from the script's real file path). Do not hardcode an absolute interpreter path in the shebang — that breaks portability across machines/users, and has bitten this project before (see `AAR.md`).
- Retry logic covers both GET and POST — the OCR/upload calls are POSTs, and 429/5xx is the most common failure mode with API rate limits.
- The API key check happens inside `main()` (not at import time) so `--version`/`--help` work without a key set.
- **Gotcha:** the bare `load_dotenv()` call (loading local `.env`) searches *upward from the script's own file location* for a `.env` file — not from the process's cwd, and not affected by `$HOME`. If an ancestor directory of the repo has its own `.env`, it gets picked up. Tests that need to simulate "no API key present" on a machine that already has a real `~/.env` must move it aside for the duration of the test (see the `no_real_dotenv` fixture in `tests/test_pdfocr.py`) — env-var/HOME tricks alone don't defeat this search.
- Exit codes follow `sysexits.h` conventions and signals exit `128+signum` — see README for the full mapping. Bump `VERSION` (semver) whenever a change alters user-facing behavior — new flags, exit codes, output format, etc.

## Testing

```bash
.venv/bin/python -m pytest tests/                     # all tests
.venv/bin/python -m pytest tests/ -k "not real_ocr"    # skip real-API tests
```

Most tests need no network access or API key. Two (`test_real_ocr`, `test_real_ocr_stdin`) hit the real Mistral API and are skipped automatically unless `~/.env` exists — each costs a small amount ($4/1000 pages). Run the suite before tagging a release, and whenever exit-code or argument-parsing logic changes.

## Backlog

See `BACKLOG.md`.
