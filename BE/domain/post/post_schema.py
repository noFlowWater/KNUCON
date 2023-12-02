from datetime import datetime
from pydantic import BaseModel, validator 
from typing import Optional

class Post(BaseModel): 
    post_id : str 
    room_id : str
    uid : str # getting from frontend

    post_status : int
    post_date : datetime
    post_title : str
    post_content : str
    post_view_count : int

class PostSearchParams(BaseModel):
    room_type: Optional[list] = None
    is_contract: Optional[list] = None
    direction: Optional[list] = None
    floor: Optional[list] = None
    area: Optional[dict] 
    gate: Optional[list] = None
    deposit: Optional[dict] 
    stove_type: Optional[list] = None
    price: Optional[dict]  
    elec_bill: Optional[bool] = None
    water_bill: Optional[bool] = None
    rent_aid: Optional[bool] = None
    gas_bill: Optional[bool] = None
    fridge: Optional[bool] = None
    ac: Optional[bool] = None
    dryer: Optional[bool] = None
    balcony: Optional[bool] = None
    kit_sep: Optional[bool] = None
    preview: Optional[bool] = None
    extension: Optional[bool] = None
    latest_desc: Optional[bool] = None
    page: int = 1
    page_size: int = 10

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
    