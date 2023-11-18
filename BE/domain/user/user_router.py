from fastapi import APIRouter, Header
from starlette import status
from domain.user.user_schema import UserRegister, UserLogin#, UserQuit

import domain.user.user_crud as user_crud

router = APIRouter(prefix = '/users')

@router.post("") # POST /users
def register_user(user_register : UserRegister):
    return user_crud.register_user(user_register)

@router.post("/login") # POST /users/login 
def login_user(user_login: UserLogin):
    return user_crud.login_user(user_login)

"""
@router.delete("/{user_id}")  # DELETE /users/{user_id}
def quit_user(user_id: str, user_quit: UserQuit):
    return user_crud.quit_user(user_id, user_quit)
"""

@router.post("/logout/{user_id}")
def logout_user(user_id: str):
    return user_crud.logout_user(user_id)