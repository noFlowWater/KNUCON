from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from domain.room.room_schema import RoomRegister
from domain.user.user_router import get_current_user_id
import domain.room.room_crud as room_crud

router = APIRouter(prefix = '/rooms')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("") # POST /rooms
def register_room(room_register : RoomRegister, user_id: str = Depends(get_current_user_id)):
    return room_crud.register_room(user_id, room_register)

@router.get("/list")  # GET /rooms/list
def get_my_rooms(user_id: str = Depends(get_current_user_id)):
    return room_crud.get_my_rooms(user_id)