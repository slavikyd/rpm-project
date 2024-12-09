import mimetypes
import os

from aiobotocore.session import get_session

MINIO_ENDPOINT = "http://localhost:9000"
ACCESS_KEY = "admin"
SECRET_KEY = "admin123"
BUCKET_NAME = "photos"

async def get_minio_client():
    session = get_session()
    return session.create_client(
        's3',
        endpoint_url=MINIO_ENDPOINT,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
    )



ALLOWED_TYPES = {"image/jpeg", "image/png"}
MAX_SIZE_MB = 5

async def validate_file(file_path):
    file_type = mimetypes.guess_type(file_path)[0]
    file_size = os.path.getsize(file_path)

    if file_type not in ALLOWED_TYPES:
        raise ValueError("Invalid file type. Allowed types: JPEG, PNG")
    if file_size > MAX_SIZE_MB * 1024 * 1024:
        raise ValueError("File size exceeds 5MB limit.")

async def upload_photo(file_path, file_name):
    await validate_file(file_path)

    async with get_minio_client() as client:
        try:
            with open(file_path, 'rb') as file_data:
                await client.put_object(
                    Bucket=BUCKET_NAME,
                    Key=file_name,
                    Body=file_data,
                    ContentType=mimetypes.guess_type(file_path)[0],
                )
            print(f"Photo {file_name} uploaded successfully.")
        except Exception as e:
            print(f"Error uploading photo: {e}")
            raise


async def get_photo(username):
    """_summary_

    Args:
        uaername (_type_): _description_

    Returns:
        _type_: _description_
    """
    async with get_minio_client() as client:
        file_name = f'user_{username}.jpg'
        try:
            response = await client.get_object(Bucket=BUCKET_NAME, Key=file_name)
            return response['Body']
        except Exception as e:
            print(f"Error retrieving photo: {e}")
            raise
