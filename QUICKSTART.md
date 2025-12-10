# Quick Start Guide

## You've successfully installed the dependencies! 🎉

## Before Running

### IMPORTANT: Set your Gemini API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey) to get your API key
2. Edit `backend/.env` file
3. Replace `your_gemini_api_key_here` with your actual API key:
   ```
   GEMINI_API_KEY=your_actual_key_here
   ```

### RECOMMENDED: Test Your API Key

Before starting the app, test your API key to see which models you have access to:

```bash
cd backend
venv\Scripts\activate
python test_models.py
```

This will show you:
- ✅ Which Gemini models are available
- ❌ Any issues with your API key
- 🎉 Which model the app will use

**Example output:**
```
Testing gemini-2.0-flash-exp... ✅ AVAILABLE
Testing gemini-1.5-flash... ✅ AVAILABLE

✅ Available Models: 2
   - gemini-2.0-flash-exp
   - gemini-1.5-flash

🎉 SUCCESS! The app will use: gemini-2.0-flash-exp
```

## Running the Application

### Option 1: Using the batch scripts (Windows)

1. **Start Backend** (in PowerShell or Command Prompt):
   ```cmd
   cd backend
   .\start_backend.bat
   ```
   Backend will run on http://localhost:8000

2. **Start Frontend** (in a NEW terminal):
   ```cmd
   cd frontend
   .\start_frontend.bat
   ```
   Frontend will run on http://localhost:3000

### Option 2: Manual start

**Terminal 1 - Backend:**
```bash
cd backend
venv\Scripts\activate
python -m uvicorn app.main:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## Access the Application

Open your browser and go to: **http://localhost:3000**

## Features to Try

1. **Text Chat**: Type a message and press Enter or click Send
2. **Image Upload**: Click the image icon to upload one or more images
3. **Ask about images**: Upload an image and ask "What's in this image?"
4. **Multiple Conversations**: Click "New Conversation" to start fresh chats
5. **Switch Conversations**: Click any conversation in the sidebar to view it
6. **Delete Conversations**: Hover over a conversation and click the trash icon

## Troubleshooting

### Backend won't start
- Make sure you've set the GEMINI_API_KEY in backend/.env
- Check that port 8000 is not already in use

### Frontend shows connection errors
- Make sure the backend is running on port 8000
- Check that backend/.env.local has the correct API URL

### "API key error"
- Double-check your Gemini API key in backend/.env
- Make sure there are no extra spaces or quotes around the key

## Next Steps

- Check out the full README.md for detailed documentation
- Customize the UI colors in frontend/tailwind.config.js
- Add more features as needed!

Enjoy your multimodal AI chat! 🚀
