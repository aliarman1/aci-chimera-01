import os
import uuid
from typing import List
from fastapi import UploadFile
from app.config import settings
from app.utils.image_utils import resize_image

async def save_upload_file(upload_file: UploadFile) -> dict:
    """
    Save an uploaded file to the uploads directory
    Returns file information
    """
    # Generate unique filename
    file_extension = os.path.splitext(upload_file.filename)[1]
    unique_filename = f"{uuid.uuid4()}{file_extension}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    # Ensure upload directory exists
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    # Save file
    contents = await upload_file.read()
    with open(file_path, "wb") as f:
        f.write(contents)
    
    # Get file size
    file_size = len(contents)
    
    # Resize if needed
    try:
        resize_image(file_path)
    except Exception as e:
        print(f"Warning: Could not resize image: {str(e)}")
    
    return {
        "file_path": file_path,
        "file_name": upload_file.filename,
        "mime_type": upload_file.content_type,
        "file_size": file_size
    }

async def save_multiple_files(files: List[UploadFile]) -> List[dict]:
    """
    Save multiple uploaded files
    Returns list of file information
    """
    saved_files = []
    for file in files:
        file_info = await save_upload_file(file)
        saved_files.append(file_info)
    return saved_files

def delete_file(file_path: str) -> bool:
    """
    Delete a file from the filesystem
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        return False
    except Exception as e:
        print(f"Error deleting file {file_path}: {str(e)}")
        return False
