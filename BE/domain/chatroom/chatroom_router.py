from fastapi import APIRouter, Depends, HTTPException, WebSocket
from typing import List, Dict
from domain.chatroom.chatroom_schema import ChatRoom
from db import get_db_connection
from util import get_current_user_id
from typing import Optional
import domain.chatroom.chatroom_crud as chatroom_crud

router = APIRouter(
    prefix = '/chatrooms'
)

@router.post("/start/{post_id}")
async def start_chatroom(post_id: str, conn=Depends(get_db_connection), creator_uid: str = Depends(get_current_user_id)):
    return chatroom_crud.create_or_verify_chatroom(post_id, creator_uid, conn)

@router.get("/{post_id}/{chatroom_id}/messages")
async def get_messages(post_id: str, chatroom_id: str, conn=Depends(get_db_connection)):
    messages_json = chatroom_crud.get_chatroom_messages(post_id, chatroom_id, conn)
    if messages_json == "[]":
        raise HTTPException(status_code=204, detail="No messages found")
    return messages_json

@router.get("/{post_id}/{chatroom_id}/creator")
async def get_chatroom_creator(post_id: str, chatroom_id: str, conn=Depends(get_db_connection)):
    return chatroom_crud.get_chatroom_creator(post_id, chatroom_id, conn)
        
# 각 채팅방별로 연결된 클라이언트 관리
chatrooms: Dict[str, List[WebSocket]] = {}

@router.websocket("/ws/{pid}/{chatroom_id}")
async def websocket_endpoint(websocket: WebSocket, pid: str, chatroom_id: str, conn=Depends(get_db_connection)):
    chatroom_key = f"{pid}_{chatroom_id}"
    if chatroom_key not in chatrooms:
        chatrooms[chatroom_key] = []

    if len(chatrooms[chatroom_key]) >= 2:
        # 채팅방이 이미 두 명의 사용자로 꽉 찼을 경우
        raise HTTPException(status_code=400, detail="Chatroom is full")

    await websocket.accept()
    chatrooms[chatroom_key].append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # 데이터베이스에 메시지 저장
            await chatroom_crud.save_message(pid, chatroom_id, data, conn)
            # 채팅방의 다른 사용자에게 메시지 전송
            for client in chatrooms[chatroom_key]:
                if client == websocket:
                    await client.send_text(data)
    except Exception as e:
        print("e:"+str(e))
        chatrooms[chatroom_key].remove(websocket)
    finally:
        if not chatrooms[chatroom_key]:
            # 채팅방이 비어있으면 삭제
            del chatrooms[chatroom_key]