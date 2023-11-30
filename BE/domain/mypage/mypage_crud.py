from datetime import datetime
import oracledb
import json

def get_user(user_id: str, conn) -> str:
    cursor = conn.cursor()
    try:
        sql = "SELECT user_id, name, login_id, phone_number FROM \"USER\" WHERE user_id = :1"
        
        cursor.execute(sql, [user_id])
        # 데이터베이스에서 정보를 가져옴
        row = cursor.fetchone()
        if row:
            # 조회된 데이터를 사전으로 만들고 JSON 문자열로 변환
            user_data = {
                "user_id": row[0],
                "name": row[1],
                "login_id": row[2],
                "phone_number": row[3]
            }
            return json.dumps(user_data)
        else:
            # 해당 사용자가 없는 경우 빈 JSON 객체 반환
            return json.dumps({})
    except oracledb.DatabaseError as e:
        # 예외 처리
        return json.dumps({"error": str(e)})
    finally:
        cursor.close()
        conn.close()

def get_user_rooms(user_id: str, conn) -> str:
    cursor = conn.cursor()
    try:
        sql = "SELECT * FROM ROOM WHERE \"UID\" = :1"
        cursor.execute(sql, [user_id])

        rows = cursor.fetchall()
        if rows:
            rooms = [{
                "room_id": row[0],
                "uid": row[1],
                "room_date": row[2].isoformat() if row[2] else None,
                "room_status": row[3],
                "room_nickname": row[4],
                "address": row[5],
                "area": float(row[6]),
                "deposit": int(row[7]),
                "price": int(row[8]),
                "room_type": row[9],
                "direction": row[10],
                "floor": int(row[11]),
                "gate": int(row[12]),
                "is_contract": bool(row[13]),
                "rent_aid": bool(row[14]),
                "preview": bool(row[15]),
                "extension": bool(row[16]),
                "elec_bill": bool(row[17]),
                "water_bill": bool(row[18]),
                "gas_bill": bool(row[19]),
                "kit_sep": bool(row[20]),
                "stove_type": bool(row[21]),
                "fridge": bool(row[22]),
                "ac": bool(row[23]),
                "mw": bool(row[24]),
                "balcony": bool(row[25]),
                "dryer": bool(row[26]),
            } for row in rows]
            return json.dumps(rooms)
        else:
            return json.dumps([])
    except oracledb.DatabaseError as e:
        return json.dumps({"error": str(e)})
    finally:
        cursor.close()
        conn.close()
        
def get_user_posts(user_id: str, conn) -> str:
    cursor = conn.cursor()
    try:
        sql = "SELECT * FROM POST WHERE \"UID\" = :1"
        cursor.execute(sql, [user_id])

        rows = cursor.fetchall()
        if rows:
            posts = [{"post_id": row[0], 
                       "room_id": row[1],
                       "uid": row[2],
                       "post_status": row[3], 
                       "post_date": row[4].isoformat() if row[2] else None,
                       "post_view_count": row[5], 
                       "post_title": row[6], 
                       "post_content": row[7], 
                      } for row in rows]
            
            return json.dumps(posts)
        else:
            return json.dumps([])
    except oracledb.DatabaseError as e:
        return json.dumps({"error": str(e)})
    finally:
        cursor.close()
        conn.close()

def get_user_wishes(user_id: str, conn) -> str:
    cursor = conn.cursor()
    try:
        sql = """
        SELECT p.*
        FROM POST p
        JOIN WISHES w ON p.POST_ID = w.PID
        WHERE w.\"UID\" = :1
        """
        cursor.execute(sql, [user_id])

        rows = cursor.fetchall()
        if rows:
            wishes = [{"post_id": row[0], 
                       "room_id": row[1],
                       "uid": row[2],
                       "post_status": row[3], 
                       "post_date": row[4].isoformat() if row[2] else None,
                       "post_view_count": row[5], 
                       "post_title": row[6], 
                       "post_content": row[7], 
                      } for row in rows]
            return json.dumps(wishes)
        else:
            return json.dumps([])
    except oracledb.DatabaseError as e:
        return json.dumps({"error": str(e)})
    finally:
        cursor.close()
        conn.close()