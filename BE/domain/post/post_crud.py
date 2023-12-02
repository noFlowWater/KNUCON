from datetime import datetime

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


def get_post(post_id:str, conn):
    cursor = conn.cursor()
    sql = f"SELECT * FROM post WHERE post.post_id = '{post_id}'"
    cursor.execute(sql)

    for row in cursor: # cannot directly get data from cursor
        post = f"post_id = {row[0]}, room_id = {row[1]}, user_id = {row[2]}, post_status = {row[3]},\
          post_date = {row[4]}, post_view_count = {row[5]}, post_title = {row[6]}, post_content = {row[7]}"
    cursor.close()
    conn.close()
    return post

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
