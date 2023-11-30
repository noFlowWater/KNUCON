from fastapi import APIRouter, Depends, HTTPException
import domain.mypage.mypage_crud as mypage_crud
from db import get_db_connection
from util import get_current_user_id

router = APIRouter(
    prefix = '/mypage'
)

@router.get("/profile")
def read_current_user_profile(conn=Depends(get_db_connection), user_id: str = Depends(get_current_user_id)):
    user_json = mypage_crud.get_user(user_id, conn)
    if user_json == "{}":
        raise HTTPException(status_code=404, detail="No user found")
    return user_json

@router.get("/rooms")
def read_user_rooms(conn=Depends(get_db_connection), user_id: str = Depends(get_current_user_id)):
    rooms_json = mypage_crud.get_user_rooms(user_id, conn)
    if rooms_json == "[]":
        raise HTTPException(status_code=204, detail="No rooms found")
    return rooms_json

@router.get("/posts")
def read_user_posts(conn=Depends(get_db_connection), user_id: str = Depends(get_current_user_id)):
    posts_json = mypage_crud.get_user_posts(user_id, conn)
    if posts_json == "[]":
        raise HTTPException(status_code=204, detail="No posts found")
    return posts_json

@router.get("/wishes")
def read_user_wishes(conn=Depends(get_db_connection), user_id: str = Depends(get_current_user_id)):
    wishes_json = mypage_crud.get_user_wishes(user_id, conn)
    if wishes_json == "[]":
        raise HTTPException(status_code=204, detail="No wishes found")
    return wishes_json