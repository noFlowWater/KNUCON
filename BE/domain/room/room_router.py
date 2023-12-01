from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer

from domain.room.room_schema import RoomRegister
from util import get_current_user_id
from domain.room.room_crud import register_room
import domain.room.room_crud as room_crud
from db import get_db_connection

router = APIRouter(prefix = '/rooms')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("") # POST /rooms
def register_room_endpoint(room_register: RoomRegister, user_id: str = Depends(get_current_user_id), conn=Depends(get_db_connection)):
    try:
        return room_crud.register_room(user_id, room_register, conn)
    except HTTPException as exc:
        raise exc

@router.get("/list")  # GET /rooms/list
def get_my_rooms(user_id: str = Depends(get_current_user_id), conn=Depends(get_db_connection)):
    return room_crud.get_my_rooms(user_id, conn)