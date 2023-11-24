from fastapi import APIRouter, Depends
from domain.chatroom.chatroom_schema import ChatRoom
from db import get_db_connection
from typing import Optional
import domain.chatroom.chatroom_crud as chatroom_crud

router = APIRouter(
    prefix = '/chatrooms'
)

# @router.get("")  # GET /posts: GET all posts
# def list_chatroom(user_id: Optional[str] = None, conn=Depends(get_db_connection)):
#     return chatroom_crud.list_chatroom(user_id, conn)