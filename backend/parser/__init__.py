"""
HRDash CV Parser
================
Modul utama untuk membaca file CV (PDF / DOCX) dan mengekstraksi
informasi terstruktur ke dalam format JSON sesuai spesifikasi
Progress Report Minggu ke-1.

Output schema:
{
    "nama":       str,
    "email":      str,
    "telepon":    str,
    "pendidikan": [{"institusi": str, "jenjang": str, "tahun_lulus": str}],
    "pengalaman": [{"perusahaan": str, "posisi": str, "durasi": str}],
    "skills":     [str, ...]
}
"""
from pathlib import Path

from .pdf_parser import extract_text_from_pdf
from .docx_parser import extract_text_from_docx
from .extractor import extract_all


SUPPORTED_EXTENSIONS = {".pdf", ".docx"}


def parse_cv(file_path: str | Path) -> dict:
    """Entry-point parser. Pilih extractor sesuai ekstensi file."""
    path = Path(file_path)
    ext = path.suffix.lower()

    if ext not in SUPPORTED_EXTENSIONS:
        raise ValueError(
            f"Format '{ext}' belum didukung. Gunakan PDF atau DOCX."
        )

    if ext == ".pdf":
        text = extract_text_from_pdf(path)
    else:
        text = extract_text_from_docx(path)

    if not text or not text.strip():
        raise ValueError(
            "Gagal mengekstraksi teks dari file. "
            "Kemungkinan CV berbasis gambar / hasil scan — "
            "silakan unggah ulang dalam format teks."
        )

    return extract_all(text)


__all__ = ["parse_cv", "SUPPORTED_EXTENSIONS"]
