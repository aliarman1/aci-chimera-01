import google.generativeai as genai
from PIL import Image as PILImage
from typing import List, Optional
from app.config import settings

# Configure Gemini API
genai.configure(api_key=settings.GEMINI_API_KEY)

async def send_to_gemini(text: str, image_paths: Optional[List[str]] = None) -> str:
    """
    Send a message with optional images to Gemini 2.0 Flash
    Returns the response text
    """
    # Try models in order of preference (newest to fallback)
    models_to_try = [
        'gemini-2.0-flash-exp',      # Latest experimental with vision
        'gemini-1.5-flash',           # Stable fallback
        'gemini-1.5-pro',             # Pro fallback
    ]
    
    last_error = None
    
    for model_name in models_to_try:
        try:
            if image_paths and len(image_paths) > 0:
                model = genai.GenerativeModel(model_name)
                
                # Prepare content parts - text first, then images for better results
                parts = [text]
                
                # Add images
                for img_path in image_paths:
                    img = PILImage.open(img_path)
                    parts.append(img)
                
                response = model.generate_content(parts)
            else:
                # Text only
                model = genai.GenerativeModel(model_name)
                response = model.generate_content(text)
            
            # Handle response
            if response and hasattr(response, 'text'):
                # Success! Print which model worked
                print(f"✅ Successfully used model: {model_name}")
                return response.text
            else:
                # Handle blocked responses
                raise Exception("Response was blocked or empty. Try rephrasing your message.")
        
        except AttributeError as e:
            # Handle cases where response.text is not available
            raise Exception("Response was blocked by safety filters or content policy.")
        
        except Exception as e:
            error_message = str(e)
            last_error = error_message
            
            # Handle common errors with helpful messages
            if "API key" in error_message or "api_key" in error_message.lower():
                raise Exception("Invalid or missing Gemini API key. Please check your configuration in backend/.env file.")
            elif "quota" in error_message.lower() or "resource" in error_message.lower():
                raise Exception("API quota exceeded. Please try again later or upgrade your plan.")
            elif "safety" in error_message.lower() or "block" in error_message.lower():
                raise Exception("Content was blocked by safety filters. Try rephrasing your message.")
            elif "not found" in error_message.lower() or "models/" in error_message.lower():
                # Model not found, try next one
                print(f"⚠️  Model '{model_name}' not available, trying next...")
                continue
            else:
                # Unknown error, try next model
                print(f"⚠️  Error with '{model_name}': {error_message}")
                continue
    
    # If we get here, all models failed
    raise Exception(f"All Gemini models failed. Last error: {last_error}. Please check your API key has access to Gemini models at https://aistudio.google.com/")
