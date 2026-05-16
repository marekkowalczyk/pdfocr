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

Set `MISTRAL_API_KEY` in your environment or in a `.env` file in the working directory.

## Usage

```bash
pdfocr input.pdf              # output to stdout
pdfocr input.pdf -o           # output to input-ocr.md (auto-derived)
pdfocr input.pdf -o out.md   # output to specific file
```

## How it works

1. Uploads the PDF to Mistral's `/v1/files` endpoint
2. Retrieves a signed URL for the uploaded file
3. Calls `/v1/ocr` with that URL (model: `mistral-ocr-latest`)
4. Concatenates per-page Markdown output

## License

MIT
