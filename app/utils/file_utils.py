from typing import Optional

from fastapi import UploadFile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if not (BASE_DIR / "storage").exists():
    (BASE_DIR / "storage").mkdir()
    (BASE_DIR / "storage" / "apartment").mkdir()
    (BASE_DIR / "storage" / "land").mkdir()
    (BASE_DIR / "storage" / "commercial").mkdir()

MEDIA_DIR = BASE_DIR / "storage"


def save_upload_file(upload_file: [UploadFile], object_id, category,
                     last_media: Optional[int] = None) -> [dict]:
    urls = []
    counter = int(last_media)+1 if last_media else 1
    for file in upload_file:
        media_type = "image" if file.content_type.startswith("image") else "video"
        if " " in file.filename:
            file.filename = file.filename.replace(" ", "_")

        filename, file_extension = file.filename.split(".")

        file_location = f"{MEDIA_DIR}/{category}/{filename}_{object_id}_{counter}.{file_extension}"
        url = f"storage/{category}/{filename}_{object_id}_{counter}.{file_extension}"

        with open(file_location, "wb") as buffer:
            buffer.write(file.file.read())

        urls.append({"url": url, "media_type": media_type})
        counter += 1

    return urls
