from pydantic import BaseModel, validator, constr 
from datetime import datetime
from typing import Optional

class RoomRegister(BaseModel):    
    room_type : int
    is_contract : int
    direction : int
    address : constr(max_length = 150)
    floor : int
    area : float
    gate : int
    elec_bill : int
    water_bill: int
    rent_aid: int
    gas_bill: int
    deposit: int
    stove_type: int
    fridge: int
    ac: int
    mw: int
    dryer: int
    balcony: int
    kit_sep: int
    preview: int
    extension: Optional[int] = None
    price: int

    @validator('*')
    def not_null(cls, v):
        if v is None:
            raise ValueError('Null values are not allowed for this field.')
        return v