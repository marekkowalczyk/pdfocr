"""Black-box CLI tests: invoke the pdfocr script as a subprocess and
check its exit codes and stdout/stderr, the same way a shell would."""

import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SCRIPT = Path(__file__).parent.parent / "pdfocr"

EX_OK = 0
EX_USAGE = 64
EX_NOINPUT = 66
EX_CONFIG = 78


def run(args, env=None, input=None, cwd=None):
    binary = isinstance(input, bytes)
    result = subprocess.run(
        [str(SCRIPT), *args],
        capture_output=True,
        text=not binary,
        env=env,
        input=input,
        cwd=cwd,
    )
    if binary:
        result.stdout = result.stdout.decode("utf-8", errors="replace")
        result.stderr = result.stderr.decode("utf-8", errors="replace")
    return result


def script_version():
    match = re.search(r'VERSION = "([\d.]+)"', SCRIPT.read_text())
    assert match, "could not find VERSION in script"
    return match.group(1)


def env_without_api_key(tmp_path):
    """A clean environment with no ~/.env and no MISTRAL_API_KEY,
    so tests don't depend on (or clobber) the developer's real key."""
    env = os.environ.copy()
    env.pop("MISTRAL_API_KEY", None)
    env["HOME"] = str(tmp_path)
    return env


def make_minimal_pdf(path):
    """Writes a minimal, syntactically valid single-page PDF (with correct
    xref offsets) containing the text 'Hello World', for real-API tests."""
    objects = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        b"2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n",
        b"3 0 obj\n<< /Type /Page /Parent 2 0 R "
        b"/Resources << /Font << /F1 4 0 R >> >> "
        b"/MediaBox [0 0 200 200] /Contents 5 0 R >>\nendobj\n",
        b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n",
    ]
    stream = b"BT /F1 24 Tf 20 100 Td (Hello World) Tj ET"
    objects.append(
        b"5 0 obj\n<< /Length %d >>\nstream\n%s\nendstream\nendobj\n"
        % (len(stream), stream)
    )

    body = b"%PDF-1.4\n"
    offsets = []
    for obj in objects:
        offsets.append(len(body))
        body += obj

    xref_offset = len(body)
    xref = b"xref\n0 %d\n0000000000 65535 f \n" % (len(objects) + 1)
    for off in offsets:
        xref += b"%010d 00000 n \n" % off

    trailer = (
        b"trailer\n<< /Size %d /Root 1 0 R >>\nstartxref\n%d\n%%%%EOF"
        % (len(objects) + 1, xref_offset)
    )
    path.write_bytes(body + xref + trailer)


HAS_REAL_KEY = os.path.exists(os.path.expanduser("~/.env"))


@pytest.fixture
def no_real_dotenv():
    """python-dotenv's load_dotenv() searches upward from the script's own
    file location (not cwd, not $HOME) for a bare '.env' — so simulating
    "no key present" on a machine that has a real ~/.env requires actually
    moving it aside. Always restored, even if the test fails."""
    real_env = Path.home() / ".env"
    backup = Path.home() / ".env.pytest-bak"
    moved = real_env.exists()
    if moved:
        shutil.move(str(real_env), str(backup))
    try:
        yield
    finally:
        if moved:
            shutil.move(str(backup), str(real_env))


def test_version():
    result = run(["--version"])
    assert result.returncode == EX_OK
    assert script_version() in result.stdout


def test_help():
    result = run(["--help"])
    assert result.returncode == EX_OK
    assert "usage:" in result.stdout


def test_missing_input_file(tmp_path):
    result = run(["nonexistent.pdf"], env=env_without_api_key(tmp_path))
    assert result.returncode == EX_NOINPUT
    assert "does not exist" in result.stderr


def test_missing_api_key(tmp_path, no_real_dotenv):
    real_pdf = tmp_path / "in.pdf"
    real_pdf.write_bytes(b"%PDF-1.4\n%%EOF")
    result = run([str(real_pdf)], env=env_without_api_key(tmp_path))
    assert result.returncode == EX_CONFIG
    assert "MISTRAL_API_KEY" in result.stderr


def test_usage_error_multiple_files_with_explicit_output(tmp_path):
    a, b = tmp_path / "a.pdf", tmp_path / "b.pdf"
    a.write_bytes(b"%PDF-1.4\n%%EOF")
    b.write_bytes(b"%PDF-1.4\n%%EOF")
    result = run(
        [str(a), str(b), "-o", "out.md"], env=env_without_api_key(tmp_path)
    )
    assert result.returncode == EX_USAGE
    assert "single explicit -o path" in result.stderr


def test_usage_error_double_stdin(tmp_path):
    result = run(["-", "-"], env=env_without_api_key(tmp_path))
    assert result.returncode == EX_USAGE
    assert "stdin" in result.stderr


def test_stdout_only_carries_output_on_error(tmp_path):
    """Diagnostics must go to stderr so stdout stays pipeable."""
    result = run(["nonexistent.pdf"], env=env_without_api_key(tmp_path))
    assert result.stdout == ""


def test_batch_continues_past_a_failing_file(tmp_path):
    """With multiple inputs, one missing file shouldn't stop the others
    from being attempted — and the overall exit code is generic (1),
    not the specific single-file code."""
    result = run(
        ["missing-1.pdf", "missing-2.pdf"], env=env_without_api_key(tmp_path)
    )
    assert result.returncode == 1
    assert "missing-1.pdf" in result.stderr
    assert "missing-2.pdf" in result.stderr


@pytest.mark.skipif(not HAS_REAL_KEY, reason="requires a real MISTRAL_API_KEY in ~/.env")
def test_real_ocr(tmp_path):
    pdf_path = tmp_path / "hello.pdf"
    make_minimal_pdf(pdf_path)
    result = run([str(pdf_path)])
    assert result.returncode == EX_OK
    assert result.stdout.strip() != ""


@pytest.mark.skipif(not HAS_REAL_KEY, reason="requires a real MISTRAL_API_KEY in ~/.env")
def test_real_ocr_stdin(tmp_path):
    pdf_path = tmp_path / "hello.pdf"
    make_minimal_pdf(pdf_path)
    result = run(["-"], input=pdf_path.read_bytes())
    assert result.returncode == EX_OK
    assert result.stdout.strip() != ""
