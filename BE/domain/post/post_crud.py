from datetime import datetime
import json
import oracledb
from domain.post.post_schema import PostInput
from util import generate_unique_id

def create_post(create_post: PostInput, user_id, conn) -> str:
    cursor = conn.cursor()
    data = []
    post_id = generate_unique_id(conn, 'P', 'POST', 'post_id') # create unique post_id 
    post_date = datetime.now()
    print(post_id)
    sql = "INSERT INTO post (post_id, rid, \"UID\", post_status, post_date, post_title, post_content) VALUES \
        (:1, :2, :3, :4, :5, :6, :7)"
    data = [(post_id, create_post.room_id, user_id, create_post.post_status, post_date,\
              create_post.post_title, create_post.post_content)]
    try:
        cursor.executemany(sql, data)
        result = "게시물이 정상적으로 등록되었습니다."
        conn.commit()
    except:
        result = "게시물 삽입 중 에러가 발생하였습니다."
    cursor.close()
    conn.close()
    return result

def list_post(conn) -> list[str]:
    post_list = []
    cursor = conn.cursor()
    sql = "SELECT * FROM post"
    cursor.execute(sql)

    # post format:
    # ('P0000337', 'R1000037', 'U0000037', 0, datetime.datetime(2021, 1, 14, 17, 45), 
    # 53, 'Post-title-3mlmV', '간단한 포스트 내용을 입력합니다.')
    for row in cursor:
        post = f"post_id = {row[0]}, room_id = {row[1]}, user_id = {row[2]}, post_status = {row[3]},\
          post_date = {row[4]}, post_view_count = {row[5]}, post_title = {row[6]}, post_content = {row[7]}"
        post_list.append(post)
    cursor.close()
    conn.close()
    return post_list

def get_post_details(post_id: str, conn) -> str:
    cursor = conn.cursor()
    try:
        # POST와 ROOM 테이블을 JOIN하는 SQL 쿼리
        sql = """
        SELECT P.*, (SELECT COUNT(W.PID) FROM WISHES W WHERE W.PID = P.POST_ID) AS WISH_COUNT, R.*
        FROM POST P
        LEFT JOIN ROOM R ON P.RID = R.ROOM_ID
        WHERE P.POST_ID = :1
        """
        cursor.execute(sql, [post_id])
        row = cursor.fetchone()
        if row:
            # row[4]는 POST_DATE (datetime), row[13]는 ROOM_DATE (datetime)
            post_data = {
                "POST_ID": row[0], 
                "RID": row[1] if row[1] is not None else None,
                "UID": row[2],
                "POST_STATUS": row[3], 
                "POST_DATE": row[4].isoformat() if row[4] else None,
                "POST_VIEW_COUNT": row[5], 
                "POST_TITLE": row[6], 
                "POST_CONTENT": row[7], 
                "WISH_COUNT": row[8],
            }

            # ROOM 데이터를 추가할 때 RID의 null 체크를 고려합니다.
            if post_data["RID"] is not None:
                post_data.update({
                    "ROOM_DATE": row[11].isoformat() if row[11] else None,
                    "ROOM_STATUS": row[12],
                    "ROOM_NICKNAME": row[13],
                    "ADDRESS": row[14],
                    "AREA": row[15],
                    "DEPOSIT": row[16],
                    "PRICE": row[17],
                    "ROOM_TYPE": row[18],
                    "DIRECTION": row[19],
                    "FLOOR": row[20],
                    "GATE": row[21],
                    "IS_CONTRACT": row[22],
                    "RENT_AID": row[23],
                    "PREVIEW": row[24],
                    "EXTENSION": row[25],
                    "ELEC_BILL": row[26],
                    "WATER_BILL": row[27],
                    "GAS_BILL": row[28],
                    "KIT_SEP": row[29],
                    "STOVE_TYPE": row[30],
                    "FRIDGE": row[31],
                    "AC": row[32],
                    "MW": row[33],
                    "BALCONY": row[34],
                    "DRYER": row[35],
                    # "PICTURE": row[36], # BLOB 데이터는 별도 처리가 필요할 수 있음
                })
            return json.dumps(post_data)
        else:
            return json.dumps({})
    except oracledb.DatabaseError as e:
        return json.dumps({"error": str(e)})
    finally:
        cursor.close()
        conn.close()

def delete_post(post_id: str, conn) -> str:
    cursor = conn.cursor()
    sql = f"DELETE FROM post WHERE post.post_id = '{post_id}'"
    try:
        cursor.execute(sql)
        conn.commit()
        result = f"게시물 {post_id}를 성공적으로 삭제하였습니다."
    except: # too many error types -> only return error when error occurs
        result = "게시물 삭제 중 에러가 발생하였습니다."
    cursor.close()
    conn.close()
    return result
