from domain.wishes.wishes_schema import WishCreate


def create_wish(wish_create : WishCreate, conn, user_id) -> str:
    cursor = conn.cursor()
    sql = "INSERT INTO WISHES VALUES (:1, :2)"
    try:
        cursor.execute(sql, (user_id, wish_create.pid))
        conn.commit()
        result = "Wish added successfully."
    except:
        result = "Error in adding wish."
    cursor.close()
    conn.close()
    return result

def list_wishes(user_id, conn) -> str:
    wishes_list = []
    cursor = conn.cursor()
    sql = "SELECT * FROM WISHES WHERE \"UID\" = :1"
    cursor.execute(sql, (user_id,))
    for row in cursor:
        wishes_list.append({"pid": row[1]})
    cursor.close()
    conn.close()
    return wishes_list