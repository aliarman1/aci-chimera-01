from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from app.database import init_db
from app.routes import chat
from app.config import settings

# Initialize database
init_db()

# Create uploads directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

app = FastAPI(
    title="Multimodal Chat API",
    description="FastAPI backend for Gemini Pro multimodal chat",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount uploads directory for serving images
app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")

# Include routers
app.include_router(chat.router, prefix="/api/chat", tags=["chat"])

@app.get("/")
async def root():
    return {
        "message": "Multimodal Chat API",
        "version": "1.0.0",
        "status": "running"
    }

@app.get("/api/health")
async def health_check():
    api_key_status = "configured" if settings.GEMINI_API_KEY else "not_configured"
    return {
        "status": "ok",
        "gemini_api_key": api_key_status,
        "database": "connected",
        "uploads_dir": os.path.exists(settings.UPLOAD_DIR)
    }

@app.on_event("startup")
async def startup_event():
    """Print helpful startup information"""
    print("\n" + "="*60)
    print("🚀 Chimera AI Backend Started Successfully!")
    print("="*60)
    print(f"📍 API URL: http://localhost:8000")
    print(f"📖 Docs: http://localhost:8000/docs")
    print(f"🗄️  Database: {settings.DATABASE_URL}")
    print(f"📁 Uploads: {settings.UPLOAD_DIR}")
    
    if settings.GEMINI_API_KEY:
        print(f"✅ Gemini API Key: Configured ({settings.GEMINI_API_KEY[:10]}...)")
    else:
        print("❌ Gemini API Key: NOT CONFIGURED!")
        print("   Please set GEMINI_API_KEY in backend/.env")
        print("   Get your key from: https://makersuite.google.com/app/apikey")
    
    print("="*60 + "\n")
