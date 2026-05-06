# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What This Is

A single-file Python CLI tool (`pdfocr`) that extracts text from PDFs using the Mistral OCR API and outputs Markdown. No build step, no tests, no package manager config.

## Running

The script is symlinked from `/usr/local/bin/pdfocr` so it's available system-wide.

```bash
# Requires MISTRAL_API_KEY in environment or .env file
pdfocr input.pdf            # output to stdout
pdfocr input.pdf -o         # output to input-ocr.md (auto-derived name)
pdfocr input.pdf -o out.md  # output to specific file
```

## Dependencies

Python 3.11, plus: `requests`, `python-dotenv`. Install with:
```bash
pip install requests python-dotenv
```

## Architecture

Single executable script (`pdfocr`), no shebang-less modules. The workflow is:
1. Upload PDF to Mistral's `/v1/files` endpoint
2. Get a signed URL via `/v1/files/{id}/url`
3. Call `/v1/ocr` with that URL, model `mistral-ocr-latest`
4. Concatenate per-page markdown output

Retry logic (5 retries with backoff) is built into the requests session for transient HTTP errors.

## Backlog

See `BACKLOG.md` for known improvement ideas.
