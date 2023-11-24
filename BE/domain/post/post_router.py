from fastapi import APIRouter, Depends
from domain.post.post_schema import UserPostInput
from db import get_db_connection
from typing import Optional
import domain.post.post_crud as post_crud

router = APIRouter(
    prefix = '/posts'
)

@router.post("") # POST /posts: create new post
def create_post(create_post: UserPostInput, conn=Depends(get_db_connection)):
    return post_crud.create_post(create_post)

@router.get("")  # GET /posts: GET all posts
def list_post(user_id: Optional[str] = None, conn=Depends(get_db_connection)):
    return post_crud.list_post(user_id, conn)

@router.get("/{post_id}")
def get_post(post_id: str, conn=Depends(get_db_connection)): # GET /posts/:post_id: GET single post
    return post_crud.get_post(post_id, conn)

@router.delete("/{post_id}") # DELETE /posts/:post_id : delete single post
def delete_post(post_id: str, conn=Depends(get_db_connection)):
    return post_crud.delete_post(post_id, conn)
