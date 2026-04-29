"""
HTTP endpoint: upload CV -> jalankan parser -> kembalikan JSON.

POST /api/upload   (multipart/form-data, field 'file')
"""
import shutil
import tempfile
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from ..parser import SUPPORTED_EXTENSIONS, parse_cv
from ..scoring import score_candidate


router = APIRouter(tags=["CV Parser"])

MAX_FILE_BYTES = 10 * 1024 * 1024  # 10 MB (sesuai info di halaman upload)


@router.post("/upload")
async def upload_cv(file: UploadFile = File(...)):
    ext = Path(file.filename or "").suffix.lower()
    if ext not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Format '{ext}' tidak didukung. Gunakan PDF atau DOCX.",
        )

    # Simpan ke file temporer agar parser dapat membaca dari disk
    with tempfile.NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        size = 0
        while chunk := await file.read(1024 * 1024):
            size += len(chunk)
            if size > MAX_FILE_BYTES:
                tmp.close()
                Path(tmp.name).unlink(missing_ok=True)
                raise HTTPException(
                    status_code=413,
                    detail="Ukuran file melebihi batas 10 MB.",
                )
            tmp.write(chunk)
        tmp_path = Path(tmp.name)

    try:
        parsed = parse_cv(tmp_path)
        scored = score_candidate(parsed)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    finally:
        tmp_path.unlink(missing_ok=True)

    return {
        "filename": file.filename,
        "parsed":   parsed,
        "scoring":  scored,
    }


@router.get("/health")
async def health():
    return {"status": "ok", "service": "HRDash CV Parser", "version": "0.1.0"}
