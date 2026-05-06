# Backlog

## Fix retry logic to include POST requests

`allowed_methods` only covers GET/HEAD/OPTIONS. The POST calls (file upload and OCR) won't retry on 429/5xx — the most common failure mode with API rate limits. Adding "POST" is safe since both endpoints are idempotent.

## Remove `include_image_base64: True` or make it a CLI flag

Base64 images are requested but never handled separately — they just bloat the markdown output. Default should be `False`, with an opt-in `--images` flag.

## Clean up uploaded files after processing

After OCR completes, the file remains on Mistral's servers. Call `DELETE /v1/files/{id}` to avoid accumulating orphaned files.

## Add progress feedback for large PDFs

Currently logs "Processing OCR..." once and blocks. For large documents, report page count or per-page progress.

## Change shebang to `python3`

`#!/usr/bin/env python3.11` fails on systems with 3.12+. Nothing in the script requires exactly 3.11.

## Add `.gitignore` and `.env.example`

Prevent accidental commit of `.env` with the API key. Provide `.env.example` documenting required variables.
