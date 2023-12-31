from pydantic import BaseModel, validator, constr 
from datetime import datetime

class UserRegister(BaseModel):
    name : constr(strip_whitespace=True)
    login_id : constr(strip_whitespace=True)
    login_password : constr(strip_whitespace=True)
    phone_number : int

    @validator('name', 'login_id', 'login_password', 'phone_number')
    def not_null(cls, v):
        if not v:
            raise ValueError('Empty values are not allowed.')
        return v
    
class UserLogin(BaseModel):
    login_id: constr(strip_whitespace=True)
    login_password: constr(strip_whitespace=True)

    # constr(strip_whitespace=True)
    @validator('login_id', 'login_password')
    def not_null(cls, v):
        if not v:
            raise ValueError('Empty values are not allowed.')
        return v
    
class UserQuit(BaseModel):
    login_password: constr(strip_whitespace=True)
    quit_confirm: bool

    @validator('login_password')
    def not_null(cls, v):
        if not v:
            raise ValueError('Empty values are not allowed.')
        return v

