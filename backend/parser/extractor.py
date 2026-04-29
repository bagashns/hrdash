"""
Rule-based extractor (regex + spaCy NLP) — Minggu 1.

Mengekstrak elemen kunci dari teks CV menjadi format JSON sesuai
spesifikasi PDF Progress Report Minggu ke-1, Bab 2.2.
"""
from __future__ import annotations

import re
from typing import Optional

from .skills_db import SKILL_LOOKUP


# ============================================================
#  spaCy loader (lazy, cached)
# ============================================================
_NLP = None


def _get_nlp():
    """Load spaCy multilingual model sekali saja."""
    global _NLP
    if _NLP is None:
        try:
            import spacy
            _NLP = spacy.load("xx_ent_wiki_sm")
        except Exception:
            _NLP = False  # tandai gagal — fallback ke heuristik regex
    return _NLP if _NLP else None


# ============================================================
#  Pattern dasar
# ============================================================
EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}")

# Telepon Indonesia: 0812..., 62812..., +62812...
PHONE_RE = re.compile(
    r"(?:\+?62|0)\s?8[1-9][\s\-]?\d{2,4}[\s\-]?\d{3,5}[\s\-]?\d{0,5}"
)

YEAR_RE = re.compile(r"\b(19|20)\d{2}\b")
YEAR_RANGE_RE = re.compile(
    r"\b(19|20)\d{2}\s*[-–—]\s*(?:(19|20)\d{2}|sekarang|present|now)\b",
    re.IGNORECASE,
)

# Jenjang pendidikan (Indonesia + umum)
DEGREE_PATTERNS = [
    (re.compile(r"\bs[\s\-]?1\b|\bsarjana\b|\bbachelor\b", re.I), "S1"),
    (re.compile(r"\bs[\s\-]?2\b|\bmagister\b|\bmaster\b", re.I), "S2"),
    (re.compile(r"\bs[\s\-]?3\b|\bdoktor\b|\bph\.?d\b", re.I), "S3"),
    (re.compile(r"\bd[\s\-]?3\b|\bdiploma\s*3\b", re.I), "D3"),
    (re.compile(r"\bd[\s\-]?4\b|\bdiploma\s*4\b", re.I), "D4"),
    (re.compile(r"\bsmk\b", re.I), "SMK"),
    (re.compile(r"\bsma\b|\bman\b", re.I), "SMA"),
]

EDU_INSTITUTION_KEYWORDS = (
    "universitas", "university", "institut", "institute",
    "politeknik", "polytechnic", "sekolah tinggi", "akademi",
    "smk", "sma", "man", "smp",
)

COMPANY_HINTS = ("pt.", "pt ", "cv.", "cv ", "tbk", "inc.", "inc ",
                 "ltd", "llc", "co.,", "studio", "startup")

# Section headers (Bahasa Indonesia + Inggris)
SECTION_HEADERS = {
    "pendidikan": [
        "pendidikan", "riwayat pendidikan", "education",
        "academic background", "educational background",
    ],
    "pengalaman": [
        "pengalaman kerja", "pengalaman", "work experience",
        "experience", "professional experience", "riwayat pekerjaan",
    ],
    "skills": [
        "keahlian", "kemampuan", "skill", "skills",
        "technical skills", "kompetensi", "expertise",
    ],
    "organisasi": [
        "pengalaman organisasi", "organisasi", "organization",
        "organizational experience",
    ],
}

# Section-end signal: header lain
ALL_HEADERS = sum(SECTION_HEADERS.values(), [])


# ============================================================
#  Helper: identitas
# ============================================================
def extract_email(text: str) -> str:
    m = EMAIL_RE.search(text)
    return m.group(0) if m else ""


def extract_phone(text: str) -> str:
    m = PHONE_RE.search(text)
    if not m:
        return ""
    # Normalisasi: hilangkan spasi/dash internal
    return re.sub(r"[\s\-]", "", m.group(0))


def extract_name(text: str) -> str:
    """
    Heuristik:
      1. spaCy NER -> ambil entitas PERSON pertama
      2. Fallback: baris pertama yang TAMPAK seperti nama
         (2-4 kata, kapitalisasi, tanpa email/telepon/angka).
    """
    nlp = _get_nlp()
    if nlp:
        doc = nlp(text[:1500])  # cukup ambil bagian header
        for ent in doc.ents:
            if ent.label_ == "PER" and 2 <= len(ent.text.split()) <= 5:
                return ent.text.strip()

    # Fallback heuristik: scan 6 baris pertama
    for line in text.splitlines()[:6]:
        line = line.strip()
        if not line or "@" in line or any(c.isdigit() for c in line):
            continue
        words = line.split()
        if 2 <= len(words) <= 5 and all(w[0].isupper() for w in words if w):
            return line

    return ""


# ============================================================
#  Helper: split section
# ============================================================
def _split_sections(text: str) -> dict[str, str]:
    """
    Bagi teks CV menjadi blok per-section berdasarkan header.
    Return: {"pendidikan": "...", "pengalaman": "...", ...}
    """
    lines = text.splitlines()
    sections: dict[str, list[str]] = {k: [] for k in SECTION_HEADERS}
    current: Optional[str] = None

    for raw in lines:
        line = raw.strip()
        low = line.lower().rstrip(":").strip()

        # Apakah baris ini adalah header section?
        matched = None
        for key, headers in SECTION_HEADERS.items():
            if low in headers or any(low.startswith(h) for h in headers):
                matched = key
                break

        if matched:
            current = matched
            continue

        if current and line:
            sections[current].append(line)

    return {k: "\n".join(v) for k, v in sections.items()}


# ============================================================
#  Helper: pendidikan
# ============================================================
def _detect_degree(line: str) -> str:
    for pat, label in DEGREE_PATTERNS:
        if pat.search(line):
            # Coba tangkap juga jurusan: "S1 Teknik Informatika"
            m = re.search(
                rf"{pat.pattern}\s+([A-Z][\w\s&]+?)(?=\s*[,;\-\n]|$)",
                line, re.I,
            )
            if m and m.group(1):
                return f"{label} {m.group(1).strip()}"
            return label
    return ""


def _detect_institution(line: str) -> str:
    low = line.lower()
    for kw in EDU_INSTITUTION_KEYWORDS:
        idx = low.find(kw)
        if idx != -1:
            # ambil 4 kata mulai dari keyword
            tail = line[idx:].split(",")[0].split("|")[0].strip()
            return " ".join(tail.split()[:5])
    return ""


def extract_education(text: str) -> list[dict]:
    """Ekstrak daftar entri pendidikan."""
    section = _split_sections(text).get("pendidikan", "") or text
    results: list[dict] = []

    # Pisahkan per blok berdasarkan baris kosong / "•" / tahun
    blocks = re.split(r"\n{2,}|^\s*[•\-\*]\s*", section, flags=re.M)

    for block in blocks:
        block = block.strip()
        if not block:
            continue

        institusi = _detect_institution(block)
        jenjang = _detect_degree(block)
        years = YEAR_RE.findall(block)
        tahun_lulus = years[-1] if years else ""

        # Hanya simpan bila ada minimal 1 sinyal pendidikan
        if institusi or jenjang:
            # YEAR_RE.findall returns capturing group ("19"/"20"); recompute full year
            full_years = re.findall(r"\b(?:19|20)\d{2}\b", block)
            results.append({
                "institusi": institusi,
                "jenjang": jenjang,
                "tahun_lulus": full_years[-1] if full_years else "",
            })

    return results


# ============================================================
#  Helper: pengalaman kerja
# ============================================================
def _detect_company(line: str) -> str:
    low = line.lower()
    for hint in COMPANY_HINTS:
        if hint in low:
            # ambil potongan sampai pemisah
            seg = line.split(",")[0].split("|")[0].split(" - ")[0]
            return seg.strip()
    return ""


def _calc_duration(block: str) -> str:
    """Hitung durasi dari rentang tahun, atau kembalikan literal jika sudah disebut."""
    # Cek literal "X tahun", "X bulan"
    m = re.search(r"(\d+)\s*(tahun|bulan|year|month)", block, re.I)
    if m:
        unit = m.group(2).lower()
        unit_id = {"year": "tahun", "month": "bulan"}.get(unit, unit)
        return f"{m.group(1)} {unit_id}"

    # Cek rentang tahun: 2021 - 2023 / 2022 - sekarang
    m = YEAR_RANGE_RE.search(block)
    if m:
        start = int(m.group(0)[:4])
        end_token = m.group(0)[-4:].lower()
        if end_token.isdigit():
            diff = int(end_token) - start
            return f"{diff} tahun" if diff > 0 else "kurang dari 1 tahun"
        return "hingga sekarang"

    return ""


def extract_experience(text: str) -> list[dict]:
    section = _split_sections(text).get("pengalaman", "")
    if not section:
        return []

    results: list[dict] = []
    blocks = re.split(r"\n{2,}|^\s*[•\-\*]\s*", section, flags=re.M)

    for block in blocks:
        block = block.strip()
        if not block or len(block) < 10:
            continue

        lines = [l.strip() for l in block.splitlines() if l.strip()]
        if not lines:
            continue

        perusahaan = _detect_company(block)
        durasi = _calc_duration(block)

        # Posisi: biasanya baris pertama atau baris dengan keyword job title
        posisi = ""
        for line in lines[:3]:
            if re.search(
                r"\b(developer|engineer|manager|analyst|designer|"
                r"intern|magang|staff|officer|specialist|consultant|"
                r"director|lead|architect|programmer)\b",
                line, re.I,
            ):
                posisi = line.split(",")[0].split("|")[0].strip()
                break

        if not posisi and lines:
            posisi = lines[0]

        if perusahaan or posisi:
            results.append({
                "perusahaan": perusahaan,
                "posisi": posisi,
                "durasi": durasi,
            })

    return results


# ============================================================
#  Helper: skills
# ============================================================
def extract_skills(text: str) -> list[str]:
    """
    Cari skill di seluruh dokumen (bukan hanya section "Skills"),
    karena banyak kandidat menyebut tools di bagian pengalaman.
    """
    found: dict[str, str] = {}  # canonical -> first-seen index, untuk preservasi urutan
    text_lower = text.lower()

    for token_lower, canonical in SKILL_LOOKUP.items():
        # Word-boundary, kecuali skill mengandung spasi (misal "Machine Learning")
        if " " in token_lower or "." in token_lower or "+" in token_lower:
            if token_lower in text_lower:
                found[canonical] = canonical
        else:
            pattern = rf"\b{re.escape(token_lower)}\b"
            if re.search(pattern, text_lower):
                found[canonical] = canonical

    return list(found.values())


# ============================================================
#  Entry point
# ============================================================
def extract_all(text: str) -> dict:
    """Gabungkan semua sub-extractor menjadi output JSON final."""
    return {
        "nama":       extract_name(text),
        "email":      extract_email(text),
        "telepon":    extract_phone(text),
        "pendidikan": extract_education(text),
        "pengalaman": extract_experience(text),
        "skills":     extract_skills(text),
    }
