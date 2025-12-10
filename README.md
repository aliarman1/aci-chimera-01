# Chimera AI - Multimodal Chat Application

A modern, full-stack multimodal chat application powered by Google's Gemini 2.5 Flash AI. Built with Next.js (frontend) and FastAPI (backend), featuring a sleek techy UI, image upload support, and persistent chat history.

## Features

- **Multimodal Chat**: Send text and images to Gemini 2.5 Flash AI
- **Multiple Conversations**: Create and manage multiple chat conversations
- **Image Upload**: Upload any number of images per message (automatically resized)
- **Chat History**: Persistent storage of all conversations in SQLite
- **Modern UI**: Sleek, techy design with gradient effects and smooth animations
- **Real-time Updates**: Instant message delivery and conversation updates
- **Error Handling**: Comprehensive error messages for API failures

## Tech Stack

### Backend
- **FastAPI**: Modern Python web framework
- **SQLAlchemy**: ORM for database operations
- **SQLite**: Lightweight database for chat history
- **Google Gemini 2.5 Flash**: AI model for multimodal chat
- **Pillow**: Image processing and resizing
- **Rate Limiting**: Automatic request throttling to prevent quota issues

### Frontend
- **Next.js 14**: React framework with App Router
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework
- **Axios**: HTTP client for API requests

## Project Structure

```
chimera/
├── backend/
│   ├── app/
│   │   ├── routes/
│   │   │   └── chat.py          # Chat API endpoints
│   │   ├── services/
│   │   │   ├── gemini.py        # Gemini 2.5 Flash integration
│   │   │   └── storage.py       # File storage handling
│   │   ├── utils/
│   │   │   ├── image_utils.py   # Image processing utilities
│   │   │   └── rate_limiter.py  # API rate limiting
│   │   ├── config.py            # Configuration settings
│   │   ├── database.py          # Database setup
│   │   ├── models.py            # SQLAlchemy models
│   │   ├── schemas.py           # Pydantic schemas
│   │   └── main.py              # FastAPI app entry point
│   ├── uploads/                 # Uploaded images storage
│   ├── requirements.txt         # Python dependencies
│   ├── test_models.py           # API key testing utility
│   ├── check_quota.py           # Quota status checker
│   ├── test_api.bat             # Quick test script (Windows)
│   ├── check_quota.bat          # Quick quota check (Windows)
│   ├── start_backend.bat        # Backend startup script (Windows)
│   └── .env                     # Environment variables
│
└── frontend/
    ├── app/
    │   ├── page.tsx             # Main page
    │   ├── layout.tsx           # Root layout
    │   └── globals.css          # Global styles
    ├── components/
    │   ├── ChatInterface.tsx    # Main chat container
    │   ├── MessageList.tsx      # Message display
    │   ├── Message.tsx          # Single message
    │   ├── MessageInput.tsx     # Input with image upload
    │   └── ImagePreview.tsx     # Image preview component
    ├── services/
    │   └── api.ts               # API client
    ├── types/
    │   └── index.ts             # TypeScript interfaces
    ├── start_frontend.bat       # Frontend startup script (Windows)
    └── package.json             # Node dependencies
```

## Setup Instructions

### Prerequisites
- Python 3.8+ 
- Node.js 18+
- Gemini API key from [Google AI Studio](https://makersuite.google.com/app/apikey)

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   Edit `backend/.env` and add your Gemini API key:
   ```env
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   UPLOAD_DIR=./uploads
   MAX_IMAGE_SIZE=10485760
   MAX_IMAGE_DIMENSION=2048
   ```

5. **Test your API key (RECOMMENDED)**:
   ```bash
   python test_models.py
   # Or on Windows:
   .\test_api.bat
   ```
   This will verify your API key has access to Gemini 2.5 Flash.

6. **Run the backend server**:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

   The backend will be running at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory** (in a new terminal):
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Run the development server**:
   ```bash
   npm run dev
   ```

   The frontend will be running at `http://localhost:3000`

## Usage

1. **Access the application**: Open your browser and go to `http://localhost:3000`

2. **Start chatting**: 
   - Type a message in the input box
   - Click the image icon to upload images (supports multiple images)
   - Press Enter or click the send button to submit

3. **Manage conversations**:
   - Click "New Conversation" to start a fresh chat
   - Click on conversations in the sidebar to switch between them
   - Delete conversations by clicking the trash icon

4. **Multimodal queries**: Upload images and ask questions about them!

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/chat/message` | Send a message with optional images |
| GET | `/api/chat/conversations` | Get all conversations |
| GET | `/api/chat/conversations/{id}` | Get specific conversation |
| DELETE | `/api/chat/conversations/{id}` | Delete a conversation |
| POST | `/api/chat/conversations` | Create new conversation |
| GET | `/api/health` | Health check |
| GET | `/uploads/{filename}` | Serve uploaded images |

## Configuration

### Backend Configuration (backend/.env)

- `GEMINI_API_KEY`: Your Gemini API key (required)
- `UPLOAD_DIR`: Directory for storing uploaded images (default: ./uploads)
- `MAX_IMAGE_SIZE`: Maximum image size in bytes (default: 10MB)
- `MAX_IMAGE_DIMENSION`: Max width/height for image resizing (default: 2048px)

### Frontend Configuration (frontend/.env.local)

- `NEXT_PUBLIC_API_URL`: Backend API URL (default: http://localhost:8000/api)

## Features in Detail

### Image Processing
- Automatically resizes large images to reduce bandwidth
- Maintains aspect ratio during resizing
- Supports JPEG, PNG, WebP, and GIF formats
- No limit on number of images per message

### Chat History
- All conversations stored in SQLite database
- Messages linked to conversations
- Images tracked with file metadata
- Automatic timestamps for all messages

### Error Handling
- User-friendly error messages
- Graceful handling of API failures
- Retry-capable architecture
- Safety filter warnings

### UI/UX Features
- Responsive design
- Dark theme with techy aesthetics
- Smooth animations and transitions
- Auto-scroll to latest messages
- Loading indicators
- Collapsible sidebar
- Image previews with remove functionality

## Development

### Adding New Features

**Backend**:
- Add new routes in `backend/app/routes/`
- Create services in `backend/app/services/`
- Define models in `backend/app/models.py`
- Define schemas in `backend/app/schemas.py`

**Frontend**:
- Create components in `frontend/components/`
- Add API methods in `frontend/services/api.ts`
- Define types in `frontend/types/index.ts`

### Database Schema

**Conversations Table**:
- id (Primary Key)
- title (Conversation name)
- created_at (Timestamp)
- updated_at (Timestamp)

**Messages Table**:
- id (Primary Key)
- conversation_id (Foreign Key)
- role (user/assistant)
- content (Message text)
- created_at (Timestamp)

**Images Table**:
- id (Primary Key)
- message_id (Foreign Key)
- file_path
- file_name
- mime_type
- file_size
- created_at (Timestamp)

## Troubleshooting

### Backend Issues

**Import errors**: Make sure you're in the virtual environment:
```bash
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows
```

**Gemini API errors**: 
- Check your API key in `.env`
- Verify API quota at Google AI Studio
- Check internet connection
- Ensure your API key has access to Gemini 2.5 Flash

**API quota exceeded**: 
- Run `check_quota.bat` (Windows) or `python check_quota.py` to check quota status
- Free tier limits: 15 requests/minute, 1,500 requests/day
- Wait for quota reset (60 seconds for RPM, 24 hours for RPD)
- Get a new API key or upgrade to paid tier
- The app includes automatic rate limiting to prevent quota issues

**Database errors**: Delete `chat_history.db` to reset the database

### Frontend Issues

**Module not found**: Run `npm install` again

**API connection errors**: 
- Verify backend is running on port 8000
- Check CORS settings in backend
- Verify `.env.local` has correct API URL

**Build errors**: Delete `.next` folder and run `npm run dev` again

## License

This project is open source and available for educational and personal use.

## Credits

- Built with [Next.js](https://nextjs.org/)
- Backend powered by [FastAPI](https://fastapi.tiangolo.com/)
- AI by [Google Gemini](https://deepmind.google/technologies/gemini/)
- Styled with [Tailwind CSS](https://tailwindcss.com/)

---

**Enjoy chatting with Chimera AI!** 🤖✨
