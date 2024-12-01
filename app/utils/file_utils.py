from fastapi import UploadFile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if not (BASE_DIR / "storage").exists():
    (BASE_DIR / "storage").mkdir()
    (BASE_DIR / "storage" / "images").mkdir()
    (BASE_DIR / "storage" / "videos").mkdir()

MEDIA_DIR = BASE_DIR / "storage"


def save_upload_file(upload_file: [UploadFile]) -> [str]:
    urls = []
    for file in upload_file:
        if file.content_type.startswith("image"):
            file_location = f"{MEDIA_DIR}/images/{file.filename}"
            url = f"storage/images/{file.filename}"
        else:
            file_location = f"{MEDIA_DIR}/videos/{file.filename}"
            url = f"storage/videos/{file.filename}"

        with open(file_location, "wb") as buffer:
            buffer.write(file.file.read())

        urls.append(url)

    return urls
