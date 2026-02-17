from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_
from typing import List
import json

from .. import models, schemas
from ..database import get_db
from ..connection_manager import manager
from .Oauth import get_current_user, verify_access_token

router = APIRouter(
    prefix="/chat",
    tags=["Chat"]
)


async def get_user_from_token(token: str, db: Session) -> models.User:
    """Verify token and return user for WebSocket connections"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    token_data = verify_access_token(token, credentials_exception)
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    if not user:
        raise credentials_exception
    return user


@router.websocket("/ws/{token}")
async def websocket_chat(websocket: WebSocket, token: str):
    """
    WebSocket endpoint for real-time chat.
    Connect with: ws://localhost:8000/chat/ws/{your_jwt_token}
    
    Send messages:
    {"type": "message", "receiver_id": 2, "content": "Hello!"}
    
    Receive messages:
    {"type": "message", "message_id": 1, "sender_id": 1, "content": "Hello!", ...}
    """
    db = next(get_db())
    
    try:
        user = await get_user_from_token(token, db)
        user_id: int = user.id  # type: ignore
    except HTTPException:
        await websocket.close(code=4001)
        return
    
    await manager.connect(websocket, user_id)
    
    await websocket.send_json({
        "type": "connected",
        "user_id": user_id,
        "message": "Connected to chat server"
    })
    
    try:
        while True:
            data = await websocket.receive_text()
            
            try:
                message_data = json.loads(data)
            except json.JSONDecodeError:
                await websocket.send_json({"type": "error", "message": "Invalid JSON"})
                continue
            
            message_type = message_data.get("type", "message")
            
            if message_type == "message":
                receiver_id = message_data.get("receiver_id")
                content = message_data.get("content")
                
                if not receiver_id or not content:
                    await websocket.send_json({"type": "error", "message": "receiver_id and content required"})
                    continue
                
                receiver = db.query(models.User).filter(models.User.id == receiver_id).first()
                if not receiver:
                    await websocket.send_json({"type": "error", "message": "Receiver not found"})
                    continue
                
                # Save to database
                new_message = models.Message(
                    sender_id=user_id,
                    receiver_id=receiver_id,
                    content=content
                )
                db.add(new_message)
                db.commit()
                db.refresh(new_message)
                
                message_response = {
                    "type": "message",
                    "message_id": new_message.id,
                    "sender_id": user_id,
                    "receiver_id": receiver_id,
                    "content": content,
                    "created_at": new_message.created_at.isoformat(),
                    "sender_email": user.email
                }
                
                # Send to receiver if online
                await manager.send_personal_message(message_response, receiver_id)
                
                # Confirm to sender
                await websocket.send_json({
                    "type": "message_sent",
                    "message_id": new_message.id,
                    "receiver_id": receiver_id,
                    "content": content,
                    "created_at": new_message.created_at.isoformat()
                })
            
            elif message_type == "typing":
                receiver_id = message_data.get("receiver_id")
                if receiver_id:
                    await manager.send_personal_message({"type": "typing", "sender_id": user_id}, receiver_id)
            
            elif message_type == "read":
                message_id = message_data.get("message_id")
                if message_id:
                    msg = db.query(models.Message).filter(
                        models.Message.id == message_id,
                        models.Message.receiver_id == user_id
                    ).first()
                    if msg:
                        msg.is_read = True  # type: ignore
                        db.commit()
                        await manager.send_personal_message({
                            "type": "read",
                            "message_id": message_id,
                            "reader_id": user_id
                        }, msg.sender_id)  # type: ignore
            
            elif message_type == "online_status":
                check_user_id = message_data.get("user_id")
                if check_user_id:
                    await websocket.send_json({
                        "type": "online_status",
                        "user_id": check_user_id,
                        "is_online": manager.is_user_online(check_user_id)
                    })
    
    except WebSocketDisconnect:
        manager.disconnect(websocket, user_id)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket, user_id)
    finally:
        db.close()


@router.get("/history/{other_user_id}", response_model=List[schemas.MessageOut])
def get_chat_history(
    other_user_id: int,
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get chat history between current user and another user"""
    messages = db.query(models.Message).filter(
        or_(
            and_(models.Message.sender_id == current_user.id, models.Message.receiver_id == other_user_id),
            and_(models.Message.sender_id == other_user_id, models.Message.receiver_id == current_user.id)
        )
    ).order_by(models.Message.created_at.desc()).offset(skip).limit(limit).all()
    
    return messages[::-1]


@router.get("/conversations", response_model=List[schemas.UserOut])
def get_conversations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get list of users the current user has chatted with"""
    sent_to = db.query(models.Message.receiver_id).filter(models.Message.sender_id == current_user.id).distinct().all()
    received_from = db.query(models.Message.sender_id).filter(models.Message.receiver_id == current_user.id).distinct().all()
    
    user_ids = set([u[0] for u in sent_to] + [u[0] for u in received_from])
    users = db.query(models.User).filter(models.User.id.in_(user_ids)).all()
    return users


@router.get("/unread/count")
def get_unread_count(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    """Get count of unread messages"""
    count = db.query(models.Message).filter(
        models.Message.receiver_id == current_user.id,
        models.Message.is_read == False
    ).count()
    return {"unread_count": count}
