"""
AI Candidate Scoring (placeholder Minggu 1).

Implementasi penuh akan dikembangkan pada Minggu 2 menggunakan
pendekatan cosine similarity antara profil kandidat (output Parser)
dan deskripsi pekerjaan, sesuai Bab 5 PDF Progress Report.
"""


def score_candidate(parsed_cv: dict, job_description: str = "") -> dict:
    """Stub function — return skor placeholder agar dashboard tetap demo-able."""
    skill_count = len(parsed_cv.get("skills", []))
    has_exp = bool(parsed_cv.get("pengalaman"))
    has_edu = bool(parsed_cv.get("pendidikan"))

    # Skor sederhana berbasis kelengkapan (placeholder)
    score = min(100, skill_count * 8 + (20 if has_exp else 0) + (15 if has_edu else 0))

    return {
        "score": score,
        "breakdown": {
            "skills": skill_count * 8,
            "experience": 20 if has_exp else 0,
            "education": 15 if has_edu else 0,
        },
        "note": "Placeholder Minggu 1 — model cosine similarity menyusul Minggu 2.",
    }
