# pdfocr

Extract text from PDFs using the Mistral OCR API. Outputs Markdown.

## Installation

Requires Python 3. Set up the project-local virtual environment (the script
re-execs itself into it automatically, so no manual activation is needed):

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt   # or requirements-dev.txt to also run tests
```

Symlink the script somewhere on your PATH:

```bash
ln -s /path/to/pdfocr /usr/local/bin/pdfocr
```

## Configuration

Set `MISTRAL_API_KEY` in `~/.env` (global) or a `.env` in the working directory. See `.env.example`.

## Usage

```bash
pdfocr input.pdf              # output to stdout
pdfocr input.pdf -o           # output to input-ocr.md (auto-derived)
pdfocr input.pdf -o out.md    # output to specific file
pdfocr input.pdf -v           # verbose progress output
pdfocr input.pdf -q           # suppress all output except errors
pdfocr input.pdf --images     # include base64-encoded images in output
pdfocr a.pdf b.pdf -o         # batch: process multiple files, each auto-derived
pdfocr - < input.pdf          # read a single PDF from stdin
pdfocr --version              # print version and exit
```

Exit codes follow `sysexits.h` conventions (0 success, 64 usage error, 66 input
file missing, 69 network/API unavailable, 73 can't write output, 76 bad API
response, 78 missing API key), so calling scripts can branch on failure type.
When multiple files are given, a per-file failure doesn't stop the batch; the
overall exit code is 1 if any file failed.

## How it works

1. Uploads the PDF to Mistral's `/v1/files` endpoint
2. Retrieves a signed URL for the uploaded file
3. Calls `/v1/ocr` with that URL (model: `mistral-ocr-latest`)
4. Concatenates per-page Markdown output
5. Deletes the uploaded file from Mistral's servers

## Tests

```bash
.venv/bin/pip install -r requirements-dev.txt
.venv/bin/python -m pytest tests/
```

Tests invoke the script as a subprocess and check exit codes/output. The two
real-network tests (`test_real_ocr`, `test_real_ocr_stdin`) are skipped
automatically if `~/.env` doesn't exist, and cost a small amount ($4/1000
pages) each time they run.

## License

MIT
