-----------------------------------------
-----------------------------------------
------ DACSTERNARY CREATE  DDL SQL ------
-----------------------------------------
-----------------------------------------


CREATE TABLE "USER"
(
"USER_ID" CHAR(8) NOT NULL,
"NAME" VARCHAR2(20) NOT NULL,
"LOGIN_ID" VARCHAR2(30) NOT NULL UNIQUE,
"LOGIN_PASSWORD" VARCHAR2(50) NOT NULL,
"PHONE_NUMBER" NUMBER(11, 0) NOT NULL,
CONSTRAINT "USER_PK" PRIMARY KEY ("USER_ID")
);

CREATE TABLE "ROOM"
(
"ROOM_ID" CHAR(8) NOT NULL,
"UID" CHAR(8) NOT NULL,
"ROOM_DATE" TIMESTAMP NOT NULL,
"ROOM_STATUS" NUMBER(1, 0) NOT NULL,
"ROOM_NICKNAME" VARCHAR2(100) NOT NULL,
"ADDRESS" VARCHAR2(150) NOT NULL,
"AREA" NUMBER(3, 1) NOT NULL,
"DEPOSIT" NUMBER(4, 0) NOT NULL,
"PRICE" NUMBER(3, 0) NOT NULL,
"ROOM_TYPE" NUMBER(1, 0) NOT NULL,
"DIRECTION" NUMBER(1, 0) NOT NULL,
"FLOOR" NUMBER(2, 0) NOT NULL,
"GATE" NUMBER(2, 0) NOT NULL,
"IS_CONTRACT" NUMBER(1, 0) NOT NULL,
"RENT_AID" NUMBER(1, 0) NOT NULL,
"PREVIEW" NUMBER(1, 0) NOT NULL,
"EXTENSION" NUMBER(1, 0),
"ELEC_BILL" NUMBER(1, 0) NOT NULL,
"WATER_BILL" NUMBER(1, 0) NOT NULL,
"GAS_BILL" NUMBER(1, 0) NOT NULL,
"KIT_SEP" NUMBER(1, 0) NOT NULL,
"STOVE_TYPE" NUMBER(1, 0) NOT NULL,
"FRIDGE" NUMBER(1, 0) NOT NULL,
"AC" NUMBER(1, 0) NOT NULL,
"MW" NUMBER(1, 0) NOT NULL,
"BALCONY" NUMBER(1, 0) NOT NULL,
"DRYER" NUMBER(1, 0) NOT NULL,
"PICTURE" BLOB,
CONSTRAINT "ROOM_PK" PRIMARY KEY ("ROOM_ID"),
CONSTRAINT "ROOM_FK" FOREIGN KEY ("UID") REFERENCES "USER" ("USER_ID")
);

CREATE TABLE "POST"
(
"POST_ID" CHAR(8) NOT NULL,
"RID" CHAR(8),
"UID" CHAR(8) NOT NULL,
"POST_STATUS" NUMBER(1, 0) NOT NULL,
"POST_DATE" TIMESTAMP NOT NULL,
"POST_VIEW_COUNT" NUMBER(8,0),
"POST_TITLE" VARCHAR2(300) NOT NULL,
"POST_CONTENT" VARCHAR2(4000),
CONSTRAINT "POST_PK" PRIMARY KEY ("POST_ID"),
CONSTRAINT "POST_FK1" FOREIGN KEY ("RID") REFERENCES "ROOM" ("ROOM_ID"),
CONSTRAINT "POST_FK2" FOREIGN KEY ("UID") REFERENCES "USER" ("USER_ID")
);

CREATE TABLE "CHATROOM"
(
"PID" CHAR(8) NOT NULL,
"CHATROOM_ID" CHAR(8) NOT NULL,
"CREATOR_UID" CHAR(8) NOT NULL,
CONSTRAINT "CHATROOM_PK" PRIMARY KEY ("PID", "CHATROOM_ID"),
CONSTRAINT "CHATROOM_FK2" FOREIGN KEY ("CREATOR_UID") REFERENCES "USER" ("USER_ID"),
CONSTRAINT "CHATROOM_FK1" FOREIGN KEY ("PID") REFERENCES "POST" ("POST_ID")
);

CREATE TABLE "REPORT"
(
"REPORT_ID" CHAR(8) NOT NULL,
"REASON" NUMBER(1, 0) NOT NULL,
"REPORTED_UID" CHAR(8) NOT NULL,
"REPORTER_UID" CHAR(8) NOT NULL,
CONSTRAINT "REPORT_PK" PRIMARY KEY ("REPORT_ID"),
CONSTRAINT "REPORT_FK1" FOREIGN KEY ("REPORTED_UID") REFERENCES "USER" ("USER_ID"),
CONSTRAINT "REPORT_FK2" FOREIGN KEY ("REPORTER_UID") REFERENCES "USER" ("USER_ID")

);

CREATE TABLE "CONNECTION"
(
"CONNECTION_ID" CHAR(8) NOT NULL,
"CONNECTED_PID" CHAR(8) NOT NULL,
"CONNECTED_CHAT_ID" CHAR(8) NOT NULL,
"COMPLETED_DATE" TIMESTAMP NOT NULL,
CONSTRAINT "CONNECTION_PK" PRIMARY KEY ("CONNECTION_ID"),
CONSTRAINT "CONNECTION_FK1" FOREIGN KEY ("CONNECTED_PID", "CONNECTED_CHAT_ID") REFERENCES "CHATROOM" ("PID", "CHATROOM_ID")
);

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

CREATE TABLE "WISHES"
(
"UID" CHAR(8) NOT NULL,
"PID" CHAR(8) NOT NULL,
CONSTRAINT "WISHES_PK" PRIMARY KEY ("UID", "PID"),
CONSTRAINT "WISHES_FK" FOREIGN KEY ("UID") REFERENCES "USER" ("USER_ID"),
CONSTRAINT "WISHES_FK_2" FOREIGN KEY ("PID") REFERENCES "POST" ("POST_ID")
);