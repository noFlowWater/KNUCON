from fastapi import APIRouter, Header
from starlette import status
from domain.user.user_schema import UserRegister, UserLogin, UserQuit, UserLogout

import domain.user.user_crud as user_crud

router = APIRouter(
    prefix = '/users'
)

@router.post("") # POST /users
def register_user(user_register : UserRegister):
    return user_crud.register_user(user_register)

@router.post("/login") # POST /users/login 
def login_user(user_login: UserLogin):
    return user_crud.login_user(user_login)

@router.post("/quit")  # POST /users/quit
def quit_user(user_quit: UserQuit):
    return user_crud.quit_user(user_quit)

@router.post("/logout")
def logout_user(user_logout: UserLogout):
    return user_crud.logout_user(user_logout)