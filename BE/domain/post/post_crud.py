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
    sql = "INSERT INTO post (post_id, rid, \"UID\", post_status, post_date, post_view_count, post_title, post_content) VALUES \
        (:1, :2, :3, :4, :5, :6, :7, :8)"
    data = [(post_id, create_post.room_id, user_id, create_post.post_status, post_date, 0,\
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

def get_total_post_count(conn, search_params: dict):
    cursor = conn.cursor()

    # Construct the WHERE clause as done in list_post function
    query_conditions = []
    bind_params = {}
    
    for key, value in search_params.items():
        if value is None :
            continue  # Skip None values

        if key == "latest_desc" or key == "page" or key == "pageSize":
            continue # Skip non-post values

        if isinstance(value, list):
            # Convert list items to strings for SQL IN clause
            value_list = ', '.join(["'" + str(v) + "'" for v in value])
            query_conditions.append(f"{key} IN ({value_list})")

        elif isinstance(value, dict) and 'start' in value and 'end' in value:
            # Handle range values
            query_conditions.append(f"{key} BETWEEN :{key}_start AND :{key}_end")
            bind_params[f"{key}_start"] = value['start']
            bind_params[f"{key}_end"] = value['end']

        elif isinstance(value, bool):
            # Convert boolean to integer and use as bind parameter
            query_conditions.append(f"{key} = :{key}")
            bind_params[key] = int(value)

    query = " AND ".join(query_conditions)

    count_sql = f"""SELECT COUNT(DISTINCT p.post_id)
                    FROM post p
                    LEFT JOIN room r ON p.rid = r.room_id
                    LEFT JOIN wishes w ON p.post_id = w.pid
                    WHERE {query}"""
    
    try:
        cursor.execute(count_sql, bind_params)
        result = cursor.fetchone()
        print(result)
        total_posts = result[0] if result else 0
        return total_posts
    except Exception as e:
        print(f"An error occurred: {e}")
        return 0
    finally:
        cursor.close()

def list_post(conn, search_params: dict, page_number: int = 1, page_size: int = 10):
    total_posts = get_total_post_count(conn, search_params)
    total_pages = (total_posts + page_size - 1) // page_size  # Calculating total number of pages

    post_list = []
    post_details = []
    cursor = conn.cursor()

    query_conditions = []
    bind_params = {}  # Separate dictionary for bind parameters

    for key, value in search_params.items():
        if value is None :
            continue  # Skip None values

        if key == "latest_desc" or key == "page" or key == "pageSize":
            continue # Skip non-post values

        if isinstance(value, list):
            # Convert list items to strings for SQL IN clause
            value_list = ', '.join(["'" + str(v) + "'" for v in value])
            query_conditions.append(f"{key} IN ({value_list})")

        elif isinstance(value, dict) and 'start' in value and 'end' in value:
            # Handle range values
            query_conditions.append(f"{key} BETWEEN :{key}_start AND :{key}_end")
            bind_params[f"{key}_start"] = value['start']
            bind_params[f"{key}_end"] = value['end']

        elif isinstance(value, bool):
            # Convert boolean to integer and use as bind parameter
            query_conditions.append(f"{key} = :{key}")
            bind_params[key] = int(value)

    # to determine order by direction
    if search_params["latest_desc"] is True:
        order_direction = "P.post_date DESC, COUNT(w.pid) DESC"
    else:
        order_direction = "COUNT(w.pid) DESC, P.post_date DESC"

    # Constructing the SQL query with search parameters
    query = " AND ".join(query_conditions)
    
    # handle page_number first
    if page_number < 1:
        page_number = 1
    elif page_number > total_pages:
        page_number = total_pages

    offset = (page_number - 1) * page_size

    sql = f"""SELECT p.post_id, COUNT(w.pid) as wish_count
      FROM post p 
      LEFT JOIN room r ON p.rid = r.room_id 
      LEFT JOIN wishes w ON p.post_id = w.pid 
      WHERE {query} 
      GROUP BY p.post_id, P.post_date
      ORDER BY {order_direction}
      OFFSET :offset ROWS FETCH NEXT :limit ROWS ONLY"""

    bind_params['limit'] = page_size
    bind_params['offset'] = offset

    try:
        cursor.execute(sql, bind_params)
        for row in cursor:
            post_list.append(row[0])  # Assuming row[0] is the post_id
    except Exception as e:
        print(f"An error occurred: {e}")

    try:
        for post_id in post_list:
            cursor.execute("SELECT p.post_id, p.\"UID\", p.post_status, p.post_date, p.post_view_count, p.post_title,\
                            (SELECT COUNT(W.PID) FROM WISHES W WHERE W.PID = P.POST_ID) AS WISH_COUNT  \
                           FROM post p LEFT JOIN wishes w ON p.post_id = w.pid  WHERE post_id = :post_id", {"post_id": post_id})
            post_detail = cursor.fetchone()
            post_details.append(post_detail)
    except Exception as e:
        print(f"An error occurred during post details query execution: {e}")
    
    finally:
        cursor.close()
        conn.close()
    return post_details, total_pages


def get_post_details(post_id: str, conn) -> str:
    cursor = conn.cursor()
    try:
        # POST와 ROOM 테이블을 JOIN하는 SQL 쿼리
        sql = """
        SELECT P.*, 
            (SELECT COUNT(W.PID) FROM WISHES W WHERE W.PID = P.POST_ID) AS WISH_COUNT, 
            R.*, 
            U.NAME
        FROM POST P
        LEFT JOIN ROOM R ON P.RID = R.ROOM_ID
        INNER JOIN "USER" U ON P."UID" = U.USER_ID
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
                "POST_CREATOR": row[37],
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


def get_post_creator(post_id, conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT \"UID\" FROM POST WHERE POST_ID = :1", [post_id])
        result = cursor.fetchone()
        return json.dumps({"UID": result[0]}) if result else json.dumps({"error": "Post not found"})

    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        cursor.close()
        
def check_my_post_status_0(user_id, conn):
    try:
        cursor = conn.cursor()
        sql = """
        SELECT 1
        FROM POST
        WHERE "UID" = :1
        AND POST_STATUS = 0
        """
        cursor.execute(sql, [user_id])
        result = cursor.fetchone()

        # If a result is found, it means there's at least one post with status 0
        if result:
            return json.dumps({"status": "exists"})
        else:
            return json.dumps({"status": "not_exists"})

    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        cursor.close()
        
def check_my_post_status_1(user_id, conn):
    try:
        cursor = conn.cursor()
        sql = """
        SELECT 1
        FROM POST
        WHERE "UID" = :1
        AND POST_STATUS = 1
        """
        cursor.execute(sql, [user_id])
        result = cursor.fetchone()

        # If a result is found, it means there's at least one post with status 0
        if result:
            return json.dumps({"status": "exists"})
        else:
            return json.dumps({"status": "not_exists"})

    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        cursor.close()