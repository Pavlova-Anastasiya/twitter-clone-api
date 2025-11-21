"""
Роутер для загрузки медиа-файлов.
POST /api/medias — принимает multipart/form-data (поле "file"), сохраняет в MEDIA_DIR и возвращает media_id.
"""
from __future__ import annotations

import os
from pathlib import Path

from fastapi import APIRouter, Depends, File, UploadFile, HTTPException, status
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.deps import get_current_user
from app.crud import create_media
from app.schemas import MediaUploadResponse, ErrorResponse

router = APIRouter(prefix="/medias", tags=["Medias"])


@router.post("", response_model=MediaUploadResponse, responses={400: {"model": ErrorResponse}})
async def upload_media(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    _user=Depends(get_current_user),
):
    """
    Загрузить файл.

    Требования:
        - Заголовок `api-key`.
        - Поле формы: file=<binary>.

    Возвращает:
        media_id: идентификатор созданной записи в БД.

    Ошибки:
        400 — если не удалось сохранить файл.
    """
    try:
        Path(settings.media_dir).mkdir(parents=True, exist_ok=True)
        filename = file.filename or "upload.bin"
        safe_name = filename.replace("/", "_").replace("\\", "_")
        dest_path = os.path.join(settings.media_dir, safe_name)

        # уникализируем имя, если занято
        base, ext = os.path.splitext(dest_path)
        i = 1
        while os.path.exists(dest_path):
            dest_path = f"{base}_{i}{ext}"
            i += 1

        with open(dest_path, "wb") as f:
            f.write(await file.read())

        media = create_media(db, path=os.path.relpath(dest_path, start="."))  # относительный путь
        return MediaUploadResponse(media_id=media.id)
    except Exception as e:  # noqa: BLE001
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"result": False, "error_type": "UploadError", "error_message": str(e)},
        )
