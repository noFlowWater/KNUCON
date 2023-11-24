from pydantic import BaseModel, validator 

class ChatRoom(BaseModel): 
    pid : str 
    chatroom_id : str
    creator_uid : str
    
    @validator('pid', 'chatroom_id', 'creator_uid')
    def not_null(cls, v):
        if not v:
            raise ValueError('Empty values are not allowed.')
        return v

"""
<< 채팅룸 DB 스키마 >> 
CREATE TABLE "CHATROOM"
(
"PID" CHAR(8) NOT NULL,
"CHATROOM_ID" CHAR(8) NOT NULL,
"CREATOR_UID" CHAR(8) NOT NULL,
CONSTRAINT "CHATROOM_PK" PRIMARY KEY ("PID", "CHATROOM_ID"),
CONSTRAINT "CHATROOM_FK2" FOREIGN KEY ("CREATOR_UID") REFERENCES "USER" ("USER_ID"),
CONSTRAINT "CHATROOM_FK1" FOREIGN KEY ("PID") REFERENCES "POST" ("POST_ID")
);
"""