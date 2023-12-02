from domain.room.room_schema import RoomRegister, RoomInfo, MyRoomList
from datetime import datetime
from util import generate_unique_id
from jose import jwt
from fastapi import HTTPException

def check_existing_room(user_id: str, conn) -> bool:
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM ROOM WHERE \"UID\" = :1 AND ROOM_STATUS = 0", (user_id,))
    (count,) = cursor.fetchone()
    return count > 0

# 새로운 함수: 방 등록
def register_room(user_id: str, room_register : RoomRegister, conn):
    cursor = conn.cursor()

    try:
        # Check if the user already has a room
        if check_existing_room(user_id, conn):
            raise HTTPException(status_code=400, detail="User already has a room")

        # Check if the user already has a room with room_status = 0
        if check_existing_room(user_id, conn):
            return "User already has a room"
        
        # 고유한 room_id 생성
        room_id = generate_unique_id(conn, 'R', 'ROOM', 'room_id')

        # 현재 시간을 room_date로 설정
        room_date = datetime.now()

        # room_status 기본값 설정
        room_status = 0

        # 방 등록 쿼리 실행
        cursor.execute("INSERT INTO ROOM (ROOM_ID, \"UID\", ROOM_DATE, ROOM_STATUS, ROOM_NICKNAME, ADDRESS, AREA, DEPOSIT, PRICE, ROOM_TYPE, DIRECTION, FLOOR, GATE, IS_CONTRACT, RENT_AID, PREVIEW, EXTENSION, ELEC_BILL, WATER_BILL, GAS_BILL, KIT_SEP, STOVE_TYPE, FRIDGE, AC, MW, BALCONY, DRYER) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15, :16, :17, :18, :19, :20, :21, :22, :23, :24, :25, :26, :27)", (room_id, user_id, room_date, room_status, room_register.room_nickname, room_register.address, room_register.area, room_register.deposit, room_register.price, room_register.room_type, room_register.direction, room_register.floor, room_register.gate, room_register.is_contract, room_register.rent_aid, room_register.preview, room_register.extension, room_register.elec_bill, room_register.water_bill, room_register.gas_bill, room_register.kit_sep, room_register.stove_type, room_register.fridge, room_register.ac, room_register.mw, room_register.balcony, room_register.dryer))
        
        conn.commit()
        print("\n <<< Room registration complete \n")
        return room_id

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        # 다른 예외 처리
        raise HTTPException(status_code=500, detail=str(e))

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def get_my_rooms(user_id: str, conn) -> MyRoomList:
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM ROOM WHERE \"UID\" = :1", (user_id,))
        rows = cursor.fetchall()

        rooms = [RoomInfo(
            room_id=row[0],
            uid=row[1],
            room_date=row[2],
            room_status=row[3],
            room_nickname=row[4],
            address=row[5],
            area=row[6],
            deposit=row[7],
            price=row[8],
            room_type=row[9],
            direction=row[10],
            floor=row[11],
            gate=row[12],
            is_contract=row[13],
            rent_aid=row[14],
            preview=row[15],
            extension=row[16],
            elec_bill=row[17],
            water_bill=row[18],
            gas_bill=row[19],
            kit_sep=row[20],
            stove_type=row[21],
            fridge=row[22],
            ac=row[23],
            mw=row[24],
            balcony=row[25],
            dryer=row[26],
            picture=row[27]  # Assuming the picture is stored as a BLOB and is the last column
        ) for row in rows]

        return MyRoomList(rooms=rooms)

    except Exception as e:
        print(f"Error fetching rooms: {str(e)}")
        return MyRoomList(rooms=[])

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()