"""
Test Gemini API models to see which ones your API key has access to.
Run this script to verify your setup before starting the application.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gemini_models():
    """Test which Gemini models are available with your API key"""
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in .env file!")
        print("\nPlease:")
        print("1. Edit backend/.env")
        print("2. Add: GEMINI_API_KEY=your_api_key_here")
        print("3. Get your key from: https://makersuite.google.com/app/apikey")
        return False
    
    print("="*60)
    print("🔍 Testing Gemini API Models")
    print("="*60)
    print(f"API Key: {api_key[:10]}...{api_key[-5:]}")
    print()
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # List of models to test (in order of preference)
        models_to_test = [
            ('gemini-2.5-flash', 'Gemini 2.5 Flash (Primary Model)'),
            ('gemini-2.0-flash-exp', 'Gemini 2.0 Flash (Experimental - Fallback)'),
            ('gemini-1.5-flash', 'Gemini 1.5 Flash (Stable Fallback)'),
            ('gemini-1.5-pro', 'Gemini 1.5 Pro (Stable Fallback)'),
        ]
        
        available_models = []
        
        for model_name, description in models_to_test:
            try:
                print(f"Testing {model_name}...", end=" ")
                model = genai.GenerativeModel(model_name)
                response = model.generate_content("Say 'Hello!'")
                
                if response and hasattr(response, 'text'):
                    print(f"✅ AVAILABLE")
                    print(f"   Description: {description}")
                    print(f"   Response: {response.text[:50]}...")
                    available_models.append(model_name)
                else:
                    print(f"⚠️  NO RESPONSE")
                    
            except Exception as e:
                error_str = str(e)
                if "not found" in error_str.lower() or "models/" in error_str:
                    print(f"❌ NOT AVAILABLE")
                elif "quota" in error_str.lower():
                    print(f"⚠️  QUOTA EXCEEDED")
                elif "API key" in error_str:
                    print(f"❌ INVALID API KEY")
                    print(f"   Error: {error_str}")
                    return False
                else:
                    print(f"❌ ERROR: {error_str[:50]}...")
            
            print()
        
        print("="*60)
        print("📊 Summary")
        print("="*60)
        
        if available_models:
            print(f"✅ Available Models: {len(available_models)}")
            for model in available_models:
                print(f"   - {model}")
            print()
            print(f"🎉 SUCCESS! The app will use: {available_models[0]}")
            return True
        else:
            print("❌ No models available!")
            print("\nPossible issues:")
            print("1. API key may not have access to Gemini models")
            print("2. You may need to enable Gemini API in Google Cloud Console")
            print("3. Check your API quota at https://aistudio.google.com/")
            return False
            
    except ImportError:
        print("❌ ERROR: google-generativeai package not installed!")
        print("\nRun: pip install google-generativeai")
        return False
    except Exception as e:
        print(f"❌ UNEXPECTED ERROR: {str(e)}")
        return False

if __name__ == "__main__":
    print("\n")
    success = test_gemini_models()
    print("\n")
    
    if success:
        print("✅ You're ready to start the application!")
        print("\nRun:")
        print("   python -m uvicorn app.main:app --reload --port 8000")
        sys.exit(0)
    else:
        print("❌ Please fix the issues above before starting the application.")
        sys.exit(1)
