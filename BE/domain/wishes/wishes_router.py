from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer

from domain.wishes.wishes_schema import WishCreate
import domain.wishes.wishes_crud as wishes_crud
from util import get_current_user_id
from db import get_db_connection

router = APIRouter(prefix='/wishes')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@router.post("")  # POST /wishes
def create_wish(wish: WishCreate, conn=Depends(get_db_connection), user_id: str = Depends(get_current_user_id)):
    return wishes_crud.create_wish(wish, conn, user_id)

@router.get("")  # GET /wishes
def list_wishes(conn=Depends(get_db_connection), user_id: str = Depends(get_current_user_id)):
    return wishes_crud.list_wishes(user_id, conn)

