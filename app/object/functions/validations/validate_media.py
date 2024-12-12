from fastapi import HTTPException, status

from app.config import MAX_VIDEO_SIZE, MAX_IMAGE_SIZE


async def validate_media(media):
    for file in media:
        media_type = "image" if file.content_type.startswith("image") else "video"
        file_size = await file.read()
        if media_type == "video":
            if len(file_size) > MAX_VIDEO_SIZE:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Video size is too large")
        elif media_type == "image":
            if len(file_size) > MAX_IMAGE_SIZE:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                    detail="Image size is too large")
        else:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid media type")
