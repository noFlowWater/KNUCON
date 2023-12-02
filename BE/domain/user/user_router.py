from fastapi import APIRouter, Depends, Form
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

from domain.user.user_schema import UserRegister, UserLogin, UserQuit, LoginIdUniqueCheck
import domain.user.user_crud as user_crud
from util import get_current_user_id
from db import get_db_connection


router = APIRouter(prefix='/users')
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("/check")
def check_login_id_endpoint(login_id :LoginIdUniqueCheck,  conn=Depends(get_db_connection)):
    return user_crud.check_login_id(login_id,conn)

@router.post("/register") # POST /users
def register_user(user_register : UserRegister,  conn=Depends(get_db_connection)):
    return user_crud.register_user(user_register, conn)

@router.post("/login") # POST /users/login 
def login_user(login_id: str = Form(...), login_password: str = Form(...),  conn=Depends(get_db_connection)):
    user_login = UserLogin(login_id=login_id, login_password=login_password)
    # 데이터베이스 연결 객체를 함수에 전달
    return user_crud.login_user(user_login, conn)

@router.post("/logout/{user_id}")
def logout_user(user_id: str):
    return user_crud.logout_user(user_id)

@router.delete("/quit")
def quit_user(user_quit: UserQuit, user_id: str = Depends(get_current_user_id)):
    return user_crud.quit_user(user_id, user_quit)
