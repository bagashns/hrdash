"""
Demo CLI: jalankan parser pada satu file CV dan cetak output JSON.

Pemakaian:
    python test_parser.py data/sample_cvs/cv_budi.pdf
    python test_parser.py data/sample_cvs/cv_dewi.docx
"""
import json
import sys
from pathlib import Path

from backend.parser import parse_cv
from backend.scoring import score_candidate


def main() -> int:
    if len(sys.argv) < 2:
        print("Pemakaian: python test_parser.py <path-ke-cv>")
        return 1

    cv_path = Path(sys.argv[1])
    if not cv_path.exists():
        print(f"File tidak ditemukan: {cv_path}")
        return 1

    print(f"\n=== Parsing: {cv_path.name} ===\n")

    try:
        parsed = parse_cv(cv_path)
    except ValueError as exc:
        print(f"ERROR: {exc}")
        return 1

    print(json.dumps(parsed, indent=2, ensure_ascii=False))

    print("\n=== Scoring (placeholder Minggu 1) ===\n")
    print(json.dumps(score_candidate(parsed), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
