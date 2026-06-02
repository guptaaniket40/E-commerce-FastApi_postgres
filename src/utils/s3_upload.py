import base64
import uuid

import aioboto3

from fastapi import HTTPException, status

from src.database.config import Config


def get_cloudfront_url(file_key: str):
    return f"{Config.AWS_CLOUDFRONT_DOMAIN}/{file_key}"


def get_file_key_from_url(image_url: str):
    return image_url.replace(
        f"{Config.AWS_CLOUDFRONT_DOMAIN}/",
        ""
    )


async def upload_base64_image_to_s3(
    image_base64: str,
    image_name: str
):
    try:
        if "," in image_base64:
            image_base64 = image_base64.split(",")[1]

        image_bytes = base64.b64decode(image_base64)

        file_extension = image_name.split(".")[-1].lower()

        if file_extension in ["jpg", "jpeg"]:
            content_type = "image/jpeg"
        elif file_extension == "png":
            content_type = "image/png"
        elif file_extension == "webp":
            content_type = "image/webp"
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Only jpg, jpeg, png, webp images are allowed"
            )

        safe_image_name = image_name.replace(" ", "-")

        file_key = f"products/{uuid.uuid4()}-{safe_image_name}"

        session = aioboto3.Session()

        async with session.client(
            "s3",
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_REGION
        ) as s3:
            await s3.put_object(
                Bucket=Config.AWS_BUCKET_NAME,
                Key=file_key,
                Body=image_bytes,
                ContentType=content_type
            )

        return get_cloudfront_url(file_key)

    except HTTPException:
        raise

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Image upload failed"
        )


async def delete_image_from_s3(image_url: str):
    if not image_url:
        return

    try:
        file_key = get_file_key_from_url(image_url)

        session = aioboto3.Session()

        async with session.client(
            "s3",
            aws_access_key_id=Config.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=Config.AWS_SECRET_ACCESS_KEY,
            region_name=Config.AWS_REGION
        ) as s3:
            await s3.delete_object(
                Bucket=Config.AWS_BUCKET_NAME,
                Key=file_key
            )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Image delete failed from S3"
        )