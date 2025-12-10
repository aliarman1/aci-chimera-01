import os
from PIL import Image
from io import BytesIO
from app.config import settings

def resize_image(image_path: str, max_dimension: int = None) -> None:
    """
    Resize image if it exceeds max_dimension while maintaining aspect ratio
    """
    if max_dimension is None:
        max_dimension = settings.MAX_IMAGE_DIMENSION
    
    try:
        img = Image.open(image_path)
        
        # Check if resizing is needed
        if img.width > max_dimension or img.height > max_dimension:
            # Calculate new dimensions maintaining aspect ratio
            if img.width > img.height:
                new_width = max_dimension
                new_height = int((max_dimension / img.width) * img.height)
            else:
                new_height = max_dimension
                new_width = int((max_dimension / img.height) * img.width)
            
            # Resize image
            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
            
            # Save back to the same path
            img.save(image_path, optimize=True, quality=85)
    except Exception as e:
        print(f"Error resizing image {image_path}: {str(e)}")
        raise

def get_image_info(file_path: str) -> dict:
    """
    Get image information like dimensions and format
    """
    try:
        img = Image.open(file_path)
        return {
            "width": img.width,
            "height": img.height,
            "format": img.format,
            "mode": img.mode
        }
    except Exception as e:
        print(f"Error getting image info: {str(e)}")
        return {}
