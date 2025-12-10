import google.generativeai as genai
from PIL import Image as PILImage
from typing import List, Optional
from app.config import settings
from app.utils.rate_limiter import rate_limiter

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

async def send_to_gemini(text: str, image_paths: Optional[List[str]] = None) -> str:
    """
    Send a message with optional images to Gemini 2.5 Pro
    Returns the response text
    """
    try:
        # Apply rate limiting before API call
        rate_limiter.wait_if_needed()
        
        # Use Gemini 2.5 Pro as primary model
        model = genai.GenerativeModel('gemini-2.5-pro')
        
        if image_paths and len(image_paths) > 0:
            # Prepare content parts - text first, then images for better results
            parts = [text]
            
            # Add images
            for img_path in image_paths:
                img = PILImage.open(img_path)
                parts.append(img)
            
            response = model.generate_content(parts)
        else:
            # Text only
            response = model.generate_content(text)
        
        # Handle response
        if response and hasattr(response, 'text'):
            print(f"✅ Successfully used model: gemini-2.5-pro")
            return response.text
        else:
            raise Exception("Response was blocked or empty. Try rephrasing your message.")
    
    except AttributeError as e:
        # Handle cases where response.text is not available
        raise Exception("Response was blocked by safety filters or content policy.")
    
    except Exception as e:
        import traceback
        error_message = str(e)
        print(f"Gemini API Error: {error_message}")
        print(traceback.format_exc())
        
        # Handle common errors with helpful messages
        if "API key" in error_message or "api_key" in error_message.lower():
            raise Exception("Invalid or missing Gemini API key. Please check your configuration in backend/.env file.")
        elif "quota" in error_message.lower() or "resource" in error_message.lower():
            raise Exception("API quota exceeded. Please try again later or upgrade your plan.")
        elif "safety" in error_message.lower() or "block" in error_message.lower():
            raise Exception("Content was blocked by safety filters. Try rephrasing your message.")
        elif "not found" in error_message.lower() or "models/" in error_message.lower():
            raise Exception("Model 'gemini-2.5-pro' not found. Please check your API key has access to Gemini 2.5 Pro at https://aistudio.google.com/")
        else:
            raise Exception(f"Failed to get response from Gemini: {error_message}")
