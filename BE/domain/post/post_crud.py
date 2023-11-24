from datetime import datetime

from domain.post.post_schema import PostInput
from util import generate_unique_id


def create_post(create_post: PostInput, conn, user_id) -> str:
    cursor = conn.cursor()
    data = []
    post_id = generate_unique_id(conn, 'P', 'POST', 'post_id') # create unique post_id 
    post_date = datetime.now()
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

def list_post(user_id, conn) -> list[str]:
    post_list = []
    cursor = conn.cursor()
    sql = "SELECT * FROM post"
    if user_id is not None: # get post with user_id
        sql = f"{sql} WHERE post.\"UID\" = '{user_id}'" # must use "" for UID and '' for user_id
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
