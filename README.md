# pdfocr

Extract text from PDFs using the Mistral OCR API. Outputs Markdown.

## Installation

Requires Python 3.11+ and:

```bash
pip install requests python-dotenv
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
pdfocr --version              # print version and exit
```

## How it works

1. Uploads the PDF to Mistral's `/v1/files` endpoint
2. Retrieves a signed URL for the uploaded file
3. Calls `/v1/ocr` with that URL (model: `mistral-ocr-latest`)
4. Concatenates per-page Markdown output
5. Deletes the uploaded file from Mistral's servers

## License

MIT
