# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A single-file Python CLI tool (`pdfocr`) that extracts text from PDFs using the Mistral OCR API and outputs Markdown. No build step, no tests, no package manager config.

## Running

The script is symlinked from `/usr/local/bin/pdfocr` so it's available system-wide.

```bash
# Requires MISTRAL_API_KEY in ~/.env or local .env
pdfocr input.pdf            # output to stdout
pdfocr input.pdf -o         # output to input-ocr.md (auto-derived name)
pdfocr input.pdf -o out.md  # output to specific file
pdfocr input.pdf -v         # verbose progress output
pdfocr input.pdf -q         # suppress all output except errors
pdfocr input.pdf --images   # include base64-encoded images in output
pdfocr --version            # print version and exit
```

## Dependencies

Python 3.11 (shebang is `python3.11` — do NOT change to `python3`, which resolves to 3.13 on this machine and does not have the required packages). Packages: `requests`, `python-dotenv`.

```bash
pip install requests python-dotenv
```

## Architecture

Single executable script (`pdfocr`), no shebang-less modules. The workflow is:
1. Upload PDF to Mistral's `/v1/files` endpoint
2. Get a signed URL via `/v1/files/{id}/url`
3. Call `/v1/ocr` with that URL, model `mistral-ocr-latest`
4. Concatenate per-page markdown output
5. Delete the uploaded file via `DELETE /v1/files/{id}`

Retry logic (5 retries with backoff) covers GET and POST requests. API key is loaded from `~/.env` first, then local `.env` (local overrides global). Key check happens inside `main()` so `--version`/`--help` work without a key.

## Backlog

See `BACKLOG.md`.
