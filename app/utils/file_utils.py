from fastapi import UploadFile
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

if not (BASE_DIR / "storage").exists():
    (BASE_DIR / "storage").mkdir()
    (BASE_DIR / "storage" / "images").mkdir()
    (BASE_DIR / "storage" / "videos").mkdir()

MEDIA_DIR = BASE_DIR / "storage"


def save_upload_file(upload_file: [UploadFile], land_id) -> [dict]:
    urls = []
    counter = 0
    for file in upload_file:
        media_type = "image" if file.content_type.startswith("image") else "video"
        if " " in file.filename:
            file.filename = file.filename.replace(" ", "_")

        filename, file_extension = file.filename.split(".")

        if file.content_type.startswith("image"):
            file_location = f"{MEDIA_DIR}/images/{filename}_{land_id}_{counter}.{file_extension}"
            url = f"storage/images/{filename}_{land_id}_{counter}.{file_extension}"
        else:
            file_location = f"{MEDIA_DIR}/videos/{filename}_{land_id}_{counter}.{file_extension}"
            url = f"storage/videos/{filename}_{land_id}_{counter}.{file_extension}"

        with open(file_location, "wb") as buffer:
            buffer.write(file.file.read())

        urls.append({"url": url, "media_type": media_type})
        counter += 1

    return urls
