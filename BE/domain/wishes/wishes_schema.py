from pydantic import BaseModel, validator 
from typing import Optional, List

class WishCreate(BaseModel):
    pid: str  # Post ID

    @validator('pid')
    def not_empty(cls, v):
        if not v:
            raise ValueError('Field cannot be empty')
        return v