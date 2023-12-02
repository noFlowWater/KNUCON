from domain.wishes.wishes_schema import WishCreate
import json

def create_wish(wish_create: WishCreate, conn, user_id) -> dict:
    cursor = conn.cursor()
    sql_check_author = "SELECT \"UID\" FROM POST WHERE \"POST_ID\" = :1"
    
    # Check if the author of the post is the same as the current user
    cursor.execute(sql_check_author, (wish_create.pid,))
    post_author = cursor.fetchone()
    
    if post_author and post_author[0] == user_id:
        # If the post author is the same as the current user, return an error
        result = {"error": "You cannot like your own post."}
    else:
        # Check if the user has already liked the post
        sql_check_wish = "SELECT COUNT(*) FROM WISHES WHERE \"UID\" = :1 AND PID = :2"
        cursor.execute(sql_check_wish, (user_id, wish_create.pid))
        existing_wish_count = cursor.fetchone()[0]

        if existing_wish_count > 0:
            result = {"error": "You have already liked this post."}
        else:
            sql = "INSERT INTO WISHES VALUES (:1, :2)"
            try:
                cursor.execute(sql, (user_id, wish_create.pid))
                conn.commit()
                result = {"message": "Wish added successfully."}
            except Exception as e:
                result = {"error": "Error in adding wish: " + str(e)}
    
    cursor.close()
    conn.close()
    return result


def list_wishes(user_id, conn) -> list:
    wishes_list = []
    cursor = conn.cursor()
    sql = "SELECT * FROM WISHES WHERE \"UID\" = :1"
    cursor.execute(sql, (user_id,))
    for row in cursor:
        wishes_list.append({"pid": row[1]})
    cursor.close()
    conn.close()
    return json.dumps(wishes_list)


def delete_wish(user_id, pid, conn) -> dict:
    cursor = conn.cursor()
    sql = "DELETE FROM WISHES WHERE \"UID\" = :1 AND PID = :2"
    try:
        cursor.execute(sql, (user_id, pid))
        conn.commit()
        result = {"message": "Wish deleted successfully."}
    except Exception as e:
        result = {"error": "Error in deleting wish: " + str(e)}
    cursor.close()
    conn.close()
    return result


def check_wish(user_id, pid, conn) -> bool:
    cursor = conn.cursor()
    sql = "SELECT COUNT(*) FROM WISHES WHERE \"UID\" = :1 AND PID = :2"
    cursor.execute(sql, (user_id, pid))
    result = cursor.fetchone()
    cursor.close()
    return result[0] > 0  # 포스트가 위시리스트에 있으면 True, 없으면 False 반환
