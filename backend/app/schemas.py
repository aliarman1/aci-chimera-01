from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ImageInfo(BaseModel):
    id: int
    file_path: str
    file_name: str
    mime_type: str
    file_size: Optional[int] = None
    created_at: datetime
    
    class Config:
        from_attributes = True

class MessageResponse(BaseModel):
    id: int
    conversation_id: int
    role: str
    content: str
    images: List[ImageInfo] = []
    created_at: datetime
    
    class Config:
        from_attributes = True

class ConversationResponse(BaseModel):
    id: int
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    messages: List[MessageResponse] = []
    
    class Config:
        from_attributes = True

class ConversationListItem(BaseModel):
    id: int
    title: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    message_count: int = 0
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ChatResponse(BaseModel):
    user_message: MessageResponse
    assistant_message: MessageResponse
    conversation_id: int
