from datetime import datetime
from pydantic import BaseModel, validator 

class Post(BaseModel): 
    post_id : str 
    room_id : str
    uid : str # getting from frontend

    post_status : int
    post_date : datetime
    post_title : str
    post_content : str
    post_view_count : int


class PostInput(BaseModel):
    room_id : str # need to get room_nickname and change into room_id

    post_status : int
    post_title : str
    post_content : str

    @validator('room_id', 'post_status', 'post_title', 'post_content')
    def not_null(cls, v):
        if not v:
            raise ValueError('Empty values are not allowed.')
        return v