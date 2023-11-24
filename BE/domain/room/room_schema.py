from pydantic import BaseModel, validator, constr 
from datetime import datetime
from typing import Optional

class RoomRegister(BaseModel):    
    room_nickname : str
    address : constr(max_length = 150)
    area : float
    deposit: int
    price: int
    room_type : int
    direction : int
    floor : int
    gate : int
    is_contract : int
    rent_aid: int
    preview: int
    extension: Optional[int] = None
    elec_bill : int
    water_bill: int
    gas_bill: int
    kit_sep: int
    stove_type: int
    fridge: int
    ac: int
    mw: int
    balcony: int
    dryer: int

    @validator('room_nickname', 'address', 'area', 'deposit', 'price', 'room_type', 
               'direction', 'floor', 'gate', 'is_contract', 'rent_aid', 'preview', 
               'elec_bill', 'water_bill', 'gas_bill', 'kit_sep', 'stove_type', 'fridge', 
               'ac', 'mw', 'balcony', 'dryer', pre=True, each_item=False)
    def not_null(cls, v):
        if v is None:
            raise ValueError('Null values are not allowed for this field.')
        return v
