from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from app.database import get_db
from app.models import Conversation, Message, Image as ImageModel
from app.schemas import (
    ConversationResponse, 
    MessageResponse, 
    ConversationListItem,
    ChatResponse
)
from app.services.gemini import send_to_gemini
from app.services.storage import save_multiple_files, delete_file

router = APIRouter()

@router.post("/message", response_model=ChatResponse)
async def send_message(
    message: str = Form(...),
    conversation_id: Optional[int] = Form(None),
    images: Optional[List[UploadFile]] = File(None),
    db: Session = Depends(get_db)
):
    """
    Send a message to the chatbot with optional images
    """
    try:
        # Create or get conversation
        if conversation_id:
            conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            # Create new conversation with title from first message
            title = message[:50] + "..." if len(message) > 50 else message
            conversation = Conversation(title=title)
            db.add(conversation)
            db.commit()
            db.refresh(conversation)
        
        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=message
        )
        db.add(user_message)
        db.commit()
        db.refresh(user_message)
        
        # Save uploaded images
        image_paths = []
        if images:
            saved_files = await save_multiple_files(images)
            for file_info in saved_files:
                image_record = ImageModel(
                    message_id=user_message.id,
                    file_path=file_info["file_path"],
                    file_name=file_info["file_name"],
                    mime_type=file_info["mime_type"],
                    file_size=file_info["file_size"]
                )
                db.add(image_record)
                image_paths.append(file_info["file_path"])
            db.commit()
        
        # Get response from Gemini
        try:
            assistant_response = await send_to_gemini(message, image_paths if image_paths else None)
        except Exception as e:
            # If Gemini fails, still save the user message but return error
            raise HTTPException(status_code=500, detail=str(e))
        
        # Save assistant message
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=assistant_response
        )
        db.add(assistant_message)
        
        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(assistant_message)
        db.refresh(user_message)
        
        return ChatResponse(
            user_message=MessageResponse.from_orm(user_message),
            assistant_message=MessageResponse.from_orm(assistant_message),
            conversation_id=conversation.id
        )
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error processing message: {str(e)}")

@router.get("/conversations", response_model=List[ConversationListItem])
async def get_conversations(db: Session = Depends(get_db)):
    """
    Get all conversations with basic info
    """
    conversations = db.query(Conversation).order_by(Conversation.updated_at.desc()).all()
    
    result = []
    for conv in conversations:
        result.append(ConversationListItem(
            id=conv.id,
            title=conv.title,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=len(conv.messages)
        ))
    
    return result

@router.get("/conversations/{conversation_id}", response_model=ConversationResponse)
async def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """
    Get a specific conversation with all messages
    """
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return ConversationResponse.from_orm(conversation)

@router.delete("/conversations/{conversation_id}")
async def delete_conversation(conversation_id: int, db: Session = Depends(get_db)):
    """
    Delete a conversation and all its messages
    """
    conversation = db.query(Conversation).filter(Conversation.id == conversation_id).first()
    
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Delete associated image files
    for message in conversation.messages:
        for image in message.images:
            delete_file(image.file_path)
    
    db.delete(conversation)
    db.commit()
    
    return {"success": True, "message": "Conversation deleted"}

@router.post("/conversations")
async def create_conversation(db: Session = Depends(get_db)):
    """
    Create a new empty conversation
    """
    conversation = Conversation(title="New Conversation")
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    
    return ConversationResponse.from_orm(conversation)
