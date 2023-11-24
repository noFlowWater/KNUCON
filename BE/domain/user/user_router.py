from fastapi import Depends, HTTPException, APIRouter
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError

from domain.user.user_schema import UserRegister, UserLogin, UserQuit
import domain.user.user_crud as user_crud

router = APIRouter(prefix = '/users')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

SECRET_KEY = "appleisgreat1234"  # Make sure to keep it consistent
ALGORITHM = "HS256"

@router.post("") # POST /users
def register_user(user_register : UserRegister):
    return user_crud.register_user(user_register)

@router.post("/login") # POST /users/login 
def login_user(user_login: UserLogin):
    return user_crud.login_user(user_login)

@router.post("/logout/{user_id}")
def logout_user(user_id: str):
    return user_crud.logout_user(user_id)

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.delete("/quit")
def quit_user(user_quit: UserQuit, user_id: str = Depends(get_current_user_id)):
    return user_crud.quit_user(user_id, user_quit)
