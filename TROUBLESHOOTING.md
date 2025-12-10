# Troubleshooting Guide

## Common Issues and Solutions

### 1. Backend: 500 Internal Server Error when sending messages

**Symptoms:**
- Frontend shows error message
- Backend logs show error in `/api/chat/message` endpoint
- Console shows: `INFO: "POST /api/chat/message HTTP/1.1" 500 Internal Server Error`

**Possible Causes & Solutions:**

#### A. Missing Gemini API Key

**Check:**
```bash
cd backend
cat .env
```

**Solution:**
1. Get your API key from https://makersuite.google.com/app/apikey
2. Edit `backend/.env` file:
   ```
   GEMINI_API_KEY=your_actual_api_key_here
   ```
3. Restart the backend server

#### B. Invalid API Key

**Symptoms:**
- Error message: "Invalid or missing Gemini API key"

**Solution:**
1. Verify your API key is correct (no extra spaces)
2. Check if the key has required permissions
3. Try generating a new key

#### C. Model Not Available

**Symptoms:**
- Error message: "Model not found"

**Solution:**
The code has been updated to use `gemini-1.5-flash`. If you don't have access:
- Try signing up for Gemini API access
- Check your API quota at https://makersuite.google.com

### 2. Backend: ImportError or Module Not Found

**Symptoms:**
```
ImportError: No module named 'fastapi'
ModuleNotFoundError: No module named 'google.generativeai'
```

**Solution:**
```bash
cd backend
# Make sure virtual environment is activated
venv\Scripts\activate    # Windows
source venv/bin/activate # Mac/Linux

# Reinstall dependencies
pip install -r requirements.txt
```

### 3. Backend: Port 8000 Already in Use

**Symptoms:**
```
ERROR: Address already in use
```

**Solution:**
```bash
# Windows - Find and kill process on port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Alternative: Use different port
python -m uvicorn app.main:app --reload --port 8001
```

Then update frontend `.env.local`:
```
NEXT_PUBLIC_API_URL=http://localhost:8001/api
```

### 4. Frontend: Connection Refused / Network Error

**Symptoms:**
- Error: "Failed to send message"
- Console: `ERR_CONNECTION_REFUSED`

**Check:**
1. Is backend running? Check http://localhost:8000/api/health
2. Check frontend `.env.local` has correct API URL
3. Check CORS settings in `backend/app/main.py`

**Solution:**
```bash
# Terminal 1 - Start backend first
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000

# Terminal 2 - Then start frontend
cd frontend
npm run dev
```

### 5. Frontend: npm install errors

**Symptoms:**
```
npm ERR! code ERESOLVE
npm ERR! ERESOLVE unable to resolve dependency tree
```

**Solution:**
```bash
cd frontend
# Delete node_modules and package-lock
rm -rf node_modules package-lock.json

# Clean install
npm install

# If still fails, try force
npm install --legacy-peer-deps
```

### 6. Images Not Displaying

**Symptoms:**
- Images upload successfully but don't show in chat
- 404 error for image URLs

**Check:**
1. Backend `uploads/` directory exists
2. Images are being saved (check `backend/uploads/`)
3. Static file mount is configured

**Solution:**
```bash
# Verify uploads directory
cd backend
mkdir -p uploads

# Check file permissions
ls -la uploads/

# Verify static mount in main.py:
# app.mount("/uploads", StaticFiles(directory=settings.UPLOAD_DIR), name="uploads")
```

### 7. Database Errors

**Symptoms:**
```
sqlalchemy.exc.OperationalError: no such table
```

**Solution:**
```bash
cd backend
# Delete and recreate database
rm chat_history.db

# Restart backend (will auto-create tables)
python -m uvicorn app.main:app --reload --port 8000
```

### 8. CORS Errors

**Symptoms:**
```
Access to fetch at 'http://localhost:8000' from origin 'http://localhost:3000' 
has been blocked by CORS policy
```

**Solution:**
Check `backend/app/main.py` CORS configuration:
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Must match frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### 9. Gemini API Quota Exceeded

**Symptoms:**
- Error: "API quota exceeded"
- Error: "Resource exhausted"

**Solution:**
1. Check your quota at https://makersuite.google.com
2. Wait for quota to reset (usually daily)
3. Upgrade to paid plan if needed
4. Reduce request frequency

### 10. Content Blocked by Safety Filters

**Symptoms:**
- Error: "Content was blocked by safety filters"

**Solution:**
1. Rephrase your message
2. Avoid sensitive or inappropriate content
3. Try a different prompt

## Debugging Tips

### Check Backend Health

```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Expected response:
{
  "status": "ok",
  "gemini_api_key": "configured",
  "database": "connected",
  "uploads_dir": true
}
```

### Check Backend Logs

Look for these messages when backend starts:
```
🚀 Chimera AI Backend Started Successfully!
✅ Gemini API Key: Configured (AIzaSyBxxx...)
```

If you see:
```
❌ Gemini API Key: NOT CONFIGURED!
```
You need to set your API key in `.env`

### Test Frontend API Connection

Open browser console (F12) on http://localhost:3000 and check:
- Network tab for API calls
- Console tab for errors
- Look for failed requests to `http://localhost:8000`

### Verify File Structure

```bash
# Backend
backend/
├── .env                 # Should exist with GEMINI_API_KEY
├── venv/               # Virtual environment
├── uploads/            # Should be created automatically
├── chat_history.db     # Created on first run
└── app/
    └── *.py

# Frontend
frontend/
├── .env.local          # Should exist with NEXT_PUBLIC_API_URL
├── node_modules/       # After npm install
└── (other files)
```

## Still Having Issues?

### Get More Details

1. **Backend errors:**
   ```bash
   cd backend
   venv\Scripts\activate
   python -m uvicorn app.main:app --reload --log-level debug
   ```

2. **Frontend errors:**
   - Open browser DevTools (F12)
   - Check Console tab
   - Check Network tab

3. **Test Gemini API directly:**
   ```python
   # Test in Python
   import google.generativeai as genai
   genai.configure(api_key="YOUR_KEY")
   model = genai.GenerativeModel('gemini-1.5-flash')
   response = model.generate_content("Hello!")
   print(response.text)
   ```

### Check Versions

```bash
# Python version (should be 3.8+)
python --version

# Node version (should be 18+)
node --version

# Pip packages
pip list | grep fastapi
pip list | grep google-generativeai
```

## Quick Reset

If everything is broken, try a fresh start:

```bash
# Backend
cd backend
deactivate  # If venv is active
rm -rf venv chat_history.db uploads/
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
# Set API key in .env
python -m uvicorn app.main:app --reload --port 8000

# Frontend (in new terminal)
cd frontend
rm -rf node_modules .next package-lock.json
npm install
npm run dev
```

---

## Contact & Support

If none of these solutions work:
1. Check the TECHNICAL_DOCUMENTATION.md for architecture details
2. Review the README.md for setup instructions
3. Check for typos in configuration files
4. Verify all dependencies are installed correctly

**Most Common Issue:** 90% of errors are due to missing or incorrect Gemini API key! Always check that first.
