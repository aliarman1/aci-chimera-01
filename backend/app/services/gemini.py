import google.generativeai as genai
from PIL import Image as PILImage
from typing import List, Optional
from app.config import settings

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

async def send_to_gemini(text: str, image_paths: Optional[List[str]] = None) -> str:
    """
    Send a message with optional images to Gemini Pro Vision
    Returns the response text
    """
    try:
        # Use gemini-pro-vision for images, gemini-pro for text only
        if image_paths and len(image_paths) > 0:
            model = genai.GenerativeModel('gemini-pro-vision')
            
            # Prepare content parts
            parts = []
            
            # Add images first
            for img_path in image_paths:
                img = PILImage.open(img_path)
                parts.append(img)
            
            # Add text prompt
            parts.append(text)
            
            response = model.generate_content(parts)
        else:
            # Text only
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(text)
        
        return response.text
    
    except Exception as e:
        error_message = str(e)
        
        # Handle common errors
        if "API key" in error_message:
            raise Exception("Invalid or missing Gemini API key. Please check your configuration.")
        elif "quota" in error_message.lower():
            raise Exception("API quota exceeded. Please try again later.")
        elif "safety" in error_message.lower():
            raise Exception("Content was blocked by safety filters.")
        else:
            raise Exception(f"Gemini API error: {error_message}")
