from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Optional

from util import get_current_user_id
from domain.post.post_schema import PostInput
import domain.post.post_crud as post_crud
from db import get_db_connection

router = APIRouter(
    prefix = '/posts'
)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@router.post("") # POST /posts: create new post
def create_post(create_post: PostInput, conn=Depends(get_db_connection), user_id: str = Depends(get_current_user_id)):
    return post_crud.create_post(create_post, user_id)

@router.get("")  # GET /posts: GET all posts
def list_post(user_id: Optional[str] = None, conn=Depends(get_db_connection)):
    return post_crud.list_post(user_id, conn)

@router.get("/{post_id}")
def get_post(post_id: str, conn=Depends(get_db_connection)): # GET /posts/:post_id: GET single post
    return post_crud.get_post(post_id, conn)

@router.delete("/{post_id}") # DELETE /posts/:post_id : delete single post
def delete_post(post_id: str, conn=Depends(get_db_connection)):
    return post_crud.delete_post(post_id, conn)
