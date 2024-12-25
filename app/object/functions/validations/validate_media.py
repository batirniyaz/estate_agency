from fastapi import HTTPException, status

from app.config import MAX_VIDEO_SIZE, MAX_IMAGE_SIZE


async def validate_media(media):
    for file in media:
        media_type = "image" if file.content_type.startswith("image") else "video"
        file_size = await file.read()
        if media_type == "video":
            if len(file_size) > MAX_VIDEO_SIZE:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Размер видеофайла слишком большой")
        elif media_type == "image":
            if len(file_size) > MAX_IMAGE_SIZE:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Размер изображения слишком большой")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Неверный формат файла")
        await file.seek(0)
