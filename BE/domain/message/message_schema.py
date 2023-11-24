from datetime import datetime
from pydantic import BaseModel, validator 

class Message(BaseModel): 
    pid : str 
    cid : str
    time : datetime
    is_creator : int
    msg_content : str
    
    @validator('pid', 'cid', 'time', 'is_creator', 'msg_content')
    def not_null(cls, v):
        if not v:
            raise ValueError('Empty values are not allowed.')
        return v
"""
<< 메세지 DB 스키마 >> 
CREATE TABLE "MESSAGE"
(
"PID" CHAR(8) NOT NULL,
"CID" CHAR(8) NOT NULL,
"TIME" TIMESTAMP NOT NULL,
"IS_CREATOR" NUMBER(1, 0) NOT NULL,
"MSG_CONTENT" VARCHAR2(500) NOT NULL,
CONSTRAINT "MESSAGE_PK" PRIMARY KEY ("PID", "CID", "TIME"),
CONSTRAINT "MESSAGE_FK1" FOREIGN KEY ("PID", "CID") REFERENCES "CHATROOM" ("PID", "CHATROOM_ID")
);
"""