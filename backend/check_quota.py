"""
Quick script to check if your Gemini API quota has reset.
This will attempt a single API call to verify access.
"""

import os
import sys
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

def check_quota_status():
    """Check if API quota is available"""
    
    # Get API key
    api_key = os.getenv("GEMINI_API_KEY")
    
    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY not found in .env file!")
        return False
    
    print("="*60)
    print(f"🔍 Checking Gemini API Quota Status")
    print(f"   Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("="*60)
    print()
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # Try the primary model with a simple request
        print("Testing API access with gemini-2.0-flash-exp...", end=" ")
        model = genai.GenerativeModel('gemini-2.0-flash-exp')
        response = model.generate_content("Hi")
        
        if response and hasattr(response, 'text'):
            print("✅ SUCCESS!")
            print()
            print("="*60)
            print("🎉 Quota Status: AVAILABLE")
            print("="*60)
            print()
            print("Your API quota has been restored!")
            print("You can now use the application normally.")
            print()
            return True
        else:
            print("⚠️  No response received")
            return False
            
    except Exception as e:
        error_str = str(e)
        print("❌ FAILED")
        print()
        
        if "quota" in error_str.lower() or "resource" in error_str.lower():
            print("="*60)
            print("⏳ Quota Status: STILL EXCEEDED")
            print("="*60)
            print()
            print("Your API quota has not reset yet.")
            print()
            print("📋 Quota Limits (Free Tier):")
            print("   • RPM (Requests Per Minute): 15")
            print("   • RPD (Requests Per Day): 1,500")
            print()
            print("⏰ Reset Times:")
            print("   • RPM quota: Resets every 60 seconds")
            print("   • RPD quota: Resets after 24 hours")
            print()
            print("💡 Solutions:")
            print("   1. Wait for quota to reset")
            print("   2. Get a new API key from: https://aistudio.google.com/app/apikey")
            print("   3. Upgrade to paid tier for higher limits")
            print()
            return False
            
        elif "not found" in error_str.lower():
            print("⚠️  Model not found - trying fallback model...")
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content("Hi")
                if response and hasattr(response, 'text'):
                    print("✅ SUCCESS with fallback model!")
                    print()
                    print("Your API is working but gemini-2.0-flash-exp is not available.")
                    print("The app will use gemini-1.5-flash instead.")
                    return True
            except Exception as e2:
                print(f"❌ Fallback also failed: {str(e2)[:100]}")
                return False
        else:
            print(f"❌ Error: {error_str[:200]}")
            return False
    
    except ImportError:
        print("❌ ERROR: google-generativeai package not installed!")
        print("\nRun: pip install google-generativeai")
        return False

if __name__ == "__main__":
    print("\n")
    success = check_quota_status()
    print()
    
    if not success:
        print("🔄 You can run this script again to check if quota has reset.")
        print(f"   Command: python check_quota.py")
    
    sys.exit(0 if success else 1)
