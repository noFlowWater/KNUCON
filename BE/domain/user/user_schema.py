from pydantic import BaseModel, validator, constr 
#constr:공백 자동제거

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

    @validator('login_id', 'login_password')
    def not_null(cls, v):
        if not v:
            raise ValueError('Empty values are not allowed.')
        return v
    
class UserProfile(BaseModel):
    profile_click : 


class UserQuit(BaseModel):
    login_password: constr(strip_whitespace=True)
    quit_check: bool    #사용자가 Yes를 눌렀는 지 확인

    @validator('login_password')
    def not_null(cls, v):
        if not v:
            raise ValueError('Empty values are not allowed.')
        return v

class UserLogout(BaseModel):
    logout_check : bool    #사용자가 Yes를 눌렀는 지 확인
