# Backlog

## Milestone: Unix hygiene

### Silence by default

Logging is hardcoded to DEBUG. Default should be WARNING (errors only). Add `-v`/`--verbose` flag for progress output.

### Don't log secrets

Verbose mode should not print the signed URL (it's a bearer-style token). Truncate or omit it.

### Add `--version` flag

Print version and exit. Argparse already provides `-h`/`--help`.

### Add `-q`/`--quiet` flag

Suppress all output except errors (complement to `-v`).

### Change shebang to `python3`

`#!/usr/bin/env python3.11` fails on systems with 3.12+. Nothing in the script requires exactly 3.11.

## Milestone: Correctness

### Fix retry logic to include POST requests

`allowed_methods` only covers GET/HEAD/OPTIONS. The POST calls (file upload and OCR) won't retry on 429/5xx — the most common failure mode with API rate limits. Adding "POST" is safe since both endpoints are idempotent.

### Clean up uploaded files after processing

After OCR completes, the file remains on Mistral's servers. Call `DELETE /v1/files/{id}` to avoid accumulating orphaned files.

## Milestone: Output quality

### Remove `include_image_base64: True` or make it a CLI flag

Base64 images are requested but never handled separately — they just bloat the markdown output. Default should be `False`, with an opt-in `--images` flag.

### Add progress feedback for large PDFs

Currently logs "Processing OCR..." once and blocks. For large documents, report page count or per-page progress (only in verbose mode).

## Milestone: Configuration

### Centralize API key in `~/.env`

The key is set somewhere on the system but its current location is unknown. Find it, then ensure it lives in `~/.env` as the single source. The script already uses `load_dotenv()` — may need to point it at `~/.env` explicitly or source `~/.env` from the shell profile.

### Add `.env.example`

Provide `.env.example` documenting required variables.
