import mimetypes
import os
import uuid
from pathlib import Path

import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv
from fastapi import HTTPException, UploadFile

load_dotenv()


def configure_cloudinary():
    if os.getenv("CLOUDINARY_URL"):
        cloudinary.config(secure=True)
        return

    CLOUD_NAME = os.getenv("CLOUDINARY_CLOUD_NAME")
    API_KEY = os.getenv("CLOUDINARY_API_KEY")
    API_SECRET = os.getenv("CLOUDINARY_API_SECRET")

    if not CLOUD_NAME or not API_KEY or not API_SECRET:
        raise HTTPException(
            status_code=500,
            detail="Cloudinary is not configured",
        )

    cloudinary.config(
        cloud_name=CLOUD_NAME,
        api_key=API_KEY,
        api_secret=API_SECRET,
        secure=True,
    )


def get_cloudinary_upload_folder(env_name: str) -> str:
    folder = os.getenv(env_name)
    if not folder:
        raise HTTPException(
            status_code=500,
            detail=f"{env_name} is not configured",
        )
    return folder


def is_image_file(upload_file: UploadFile) -> bool:
    content_type = upload_file.content_type or ""
    if content_type.startswith("image/"):
        return True

    guessed_type, _ = mimetypes.guess_type(upload_file.filename or "")
    return bool(guessed_type and guessed_type.startswith("image/"))


def upload_image_to_cloudinary(upload_file: UploadFile) -> str:
    if not is_image_file(upload_file):
        raise HTTPException(status_code=400, detail="Only image files can be uploaded")

    configure_cloudinary()

    filename = Path(upload_file.filename or "image").stem
    public_id = f"{filename}-{uuid.uuid4().hex}"

    try:
        upload_file.file.seek(0)
        result = cloudinary.uploader.upload(
            upload_file.file,
            folder=get_cloudinary_upload_folder("CLOUDINARY_UPLOAD_IMAGE_DIR"),
            public_id=public_id,
            resource_type="image",
            overwrite=False,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Cloudinary upload failed: {str(exc)}",
        )

    secure_url = result.get("secure_url") or result.get("url")
    if not secure_url:
        raise HTTPException(
            status_code=500, detail="Cloudinary did not return an image URL"
        )

    return secure_url


def upload_file_to_cloudinary(upload_file: UploadFile) -> str:
    configure_cloudinary()

    try:
        upload_file.file.seek(0)
        result = cloudinary.uploader.upload(
            upload_file.file,
            folder=get_cloudinary_upload_folder("CLOUDINARY_UPLOAD_FILE_DIR"),
            resource_type="auto",
            use_filename=True,
            unique_filename=True,
            overwrite=False,
        )
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Cloudinary upload failed: {str(exc)}",
        )

    secure_url = result.get("secure_url") or result.get("url")
    if not secure_url:
        raise HTTPException(
            status_code=500, detail="Cloudinary did not return a file URL"
        )

    return secure_url
