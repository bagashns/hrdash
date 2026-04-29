# HRDash — AI-Based CV Screening Platform

MVP Minggu 1 (Kelompok 8). Platform untuk membantu HR menyaring CV kandidat
secara otomatis menggunakan parser rule-based + NLP, dengan tampilan
dashboard yang clean & minimal.

## Anggota Tim
- Bagas Heningswara — M0405241070
- Dhirendra Abisatya Arundaya — M0405241009
- Syahidah Asma Wardana — M0405241040

## Struktur Proyek

```
hrdash/
├── backend/
│   ├── main.py            # FastAPI entry point
│   ├── parser/            # CV Parser (PDF / DOCX -> JSON)
│   ├── scoring/           # AI Scoring (placeholder Minggu 1)
│   └── api/               # HTTP endpoints
├── frontend/
│   ├── index.html         # Halaman Upload CV
│   ├── dashboard.html     # Halaman Hasil Analisis
│   └── assets/            # CSS / JS / gambar
├── data/
│   └── sample_cvs/        # Dataset CV uji (25 sampel)
├── test_parser.py         # CLI demo parser
├── requirements.txt
└── README.md
```

## Persiapan

```bash
# 1. Buat virtual environment
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # macOS / Linux

# 2. Install dependensi
pip install -r requirements.txt

# 3. Download model spaCy (multilingual, untuk NER nama)
python -m spacy download xx_ent_wiki_sm
```

## Menjalankan

### A. Uji parser saja (CLI)

```bash
python test_parser.py data/sample_cvs/cv_budi.pdf
```

Output: JSON dengan field `nama`, `email`, `telepon`, `pendidikan`,
`pengalaman`, `skills` — sesuai spesifikasi PDF Bab 2.2.

### B. Jalankan server + frontend

```bash
uvicorn backend.main:app --reload
```

Buka:
- `http://localhost:8000/`           — Halaman Upload CV
- `http://localhost:8000/dashboard`  — Halaman Hasil Analisis
- `http://localhost:8000/docs`       — Swagger UI (API documentation)

## Endpoints API

| Method | Path           | Deskripsi                                     |
|--------|----------------|-----------------------------------------------|
| POST   | `/api/upload`  | Upload file CV (PDF/DOCX) -> kembalikan JSON  |
| GET    | `/api/health`  | Health check                                  |

## Tech Stack

- **Backend:** Python 3.11+, FastAPI, Uvicorn
- **Parser:** pdfplumber, python-docx, spaCy (xx_ent_wiki_sm), regex
- **Fallback PDF unstructured:** PyMuPDF (tindak lanjut Minggu 2)
- **Frontend:** HTML, CSS, JavaScript (vanilla)

## Roadmap

- [x] **Minggu 1** — Setup environment, CV Parser awal, dataset 25 CV, desain dashboard
- [ ] **Minggu 2** — AI Candidate Scoring (cosine similarity), integrasi end-to-end, dashboard dinamis
- [ ] **Minggu 3** — Internal testing & refinement
- [ ] **Minggu 4** — User testing dengan calon HR
