# Backlog

Unix citizenship milestone implemented as of 2026-07-21 (sysexits-style exit
codes, 128+signum on signal exit, stdin/batch input support). Remaining ideas
below are unscoped — not yet committed to, just captured for future
consideration.

## Milestone: OCR model

### `--model` flag to override the hardcoded model

`process_ocr` hardcodes `"model": "mistral-ocr-latest"`. Mistral publishes
distinct pinned model IDs per OCR version (e.g. `mistral-ocr-4-0+2` for
OCR 4) alongside the rolling `latest` alias. A `--model` flag would let
callers pin a specific version instead of always riding `latest`.

### Opt-in support for OCR 4 annotations / bounding boxes

OCR 4 adds paragraph-level bounding box extraction and structured
annotations (at a higher $5/1000-page tier, vs. $4/1000 standard). Not
needed today, but could be added as an opt-in flag (similar to `--images`)
if a future use case wants structured output instead of plain markdown.

## Milestone: Output quality

### Cache/skip unchanged files

Re-running `pdfocr` on the same file re-uploads and re-OCRs it every
time, at full API cost. A content-hash-based cache (skip or reuse prior
output for an unchanged file) could avoid redundant spend.
