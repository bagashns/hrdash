"""
PDF text extraction.

Strategi:
  1. pdfplumber  -> primary (sesuai stack Minggu 1)
  2. PyMuPDF     -> fallback bila hasil pdfplumber kosong
                    (tindak lanjut Minggu 2 untuk PDF unstructured)
"""
from pathlib import Path

import pdfplumber


def _extract_with_pdfplumber(path: Path) -> str:
    pages = []
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            text = page.extract_text() or ""
            pages.append(text)
    return "\n".join(pages).strip()


def _extract_with_pymupdf(path: Path) -> str:
    try:
        import fitz  # PyMuPDF
    except ImportError:
        return ""

    doc = fitz.open(path)
    pages = [page.get_text() for page in doc]
    doc.close()
    return "\n".join(pages).strip()


def extract_text_from_pdf(path: Path) -> str:
    """Ekstrak teks dari PDF, dengan fallback PyMuPDF bila perlu."""
    text = _extract_with_pdfplumber(path)

    # Fallback bila pdfplumber gagal pada PDF berbasis grafis kompleks
    if len(text) < 50:
        text = _extract_with_pymupdf(path) or text

    return text
