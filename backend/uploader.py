import os
import uuid
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import Session

from database import Base, get_db

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------

BASE_URL = os.getenv("BASE_URL", "http://localhost:8001")

MEDIA_DIR = Path(__file__).parent / "media"
IMAGES_DIR = MEDIA_DIR / "images"
IMAGES_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_CONTENT_TYPES = {"image/jpeg", "image/png"}
EXTENSIONS = {"image/jpeg": ".jpg", "image/png": ".png"}


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    # Used to attach the image to another object (safe to share with clients)
    attachment_key = Column(String, unique=True, index=True, nullable=False)
    # Used to build the file path; not exposed until the image is attached
    public_id = Column(String, unique=True, nullable=False)
    # Relative path: "images/<public_id>.<ext>"
    file_path = Column(String, nullable=False)
    description = Column(String, nullable=True)
    uploaded_on = Column(DateTime, nullable=False)

    @property
    def url(self) -> str:
        return f"{BASE_URL}/media/{self.file_path}"


# ---------------------------------------------------------------------------
# Schema
# ---------------------------------------------------------------------------


class ImageOut(BaseModel):
    attachment_key: str
    description: str | None
    uploaded_on: datetime
    url: str


# ---------------------------------------------------------------------------
# Router
# ---------------------------------------------------------------------------

router = APIRouter(prefix="/uploads", tags=["uploads"])


@router.post("/images/", response_model=ImageOut, status_code=201)
async def upload_image(
    file: UploadFile,
    description: str = "",
    db: Session = Depends(get_db),
):
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=422,
            detail="Tipo de arquivo inválido. Apenas JPEG e PNG são aceitos.",
        )

    ext = EXTENSIONS[file.content_type]
    public_id = str(uuid.uuid4())
    attachment_key = str(uuid.uuid4())
    filename = f"{public_id}{ext}"
    file_path = IMAGES_DIR / filename

    contents = await file.read()
    file_path.write_bytes(contents)

    image = Image(
        attachment_key=attachment_key,
        public_id=public_id,
        file_path=f"images/{filename}",
        description=description or None,
        uploaded_on=datetime.now(timezone.utc),
    )
    db.add(image)
    db.commit()
    db.refresh(image)

    return ImageOut(
        attachment_key=image.attachment_key,
        description=image.description,
        uploaded_on=image.uploaded_on,
        url=image.url,
    )
