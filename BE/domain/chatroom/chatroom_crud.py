# Pseudo-code for chat_crud.py
import oracledb
import json

def check_existing_chatroom(post_id, creator_uid, conn):
    try:
        cursor = conn.cursor()
        
        query = """
        SELECT CHATROOM_ID 
        FROM CHATROOM 
        WHERE PID = :1 AND CREATOR_UID = :2
        """
        cursor.execute(query, (post_id, creator_uid))

        row = cursor.fetchone()
        if row:
            return {"exists": True, "CHATROOM_ID": row[0]}
        else:
            return {"exists": False}

    except Exception as e:
        print("An error occurred while check_existing_chatroom:", e)
        raise
    finally:
        cursor.close()
        
def create_new_chatroom(post_id, creator_uid, conn):
    try:
        print(">>>>>>>>>"+post_id)
        cursor = conn.cursor()

        new_chatroom_id = generate_chatroom_id(post_id, conn)

        query = "INSERT INTO CHATROOM (PID, CHATROOM_ID, CREATOR_UID) VALUES (:1, :2, :3)"
        cursor.execute(query, (post_id, new_chatroom_id, creator_uid))
        conn.commit()

        return new_chatroom_id

    except Exception as e:
        print("An error occurred while creating a new chatroom:", e)
        raise
    
    finally:
        if cursor:
            cursor.close()

def generate_chatroom_id(post_id, conn):
    try:
        cursor = conn.cursor()

        # Find the highest chatroom_id for the given post_id
        query = "SELECT MAX(CHATROOM_ID) as max_id FROM CHATROOM WHERE PID = :1"
        cursor.execute(query, [post_id])
        result = cursor.fetchone()

        # Check if a result was found and process it
        if result and result[0]:
            # Increment the last chatroom_id by 1
            last_id = int(result[0][1:])  # Extracting the numeric part from the ID
            if last_id == 9999999:
                # Handle the case where the ID can no longer be incremented
                raise Exception("Maximum number of chatrooms reached for this post.")
            new_id = last_id + 1
            new_chatroom_id = f"C{new_id:07}"  # Format to keep the leading zeros
        else:
            # If no chatroom exists for this post, start with C0000001
            new_chatroom_id = "C0000001"

        return new_chatroom_id

    except Exception as e:
        print("An error occurred:", e)
        # Optionally, re-raise the exception if you want it to be handled at a higher level
        raise
    finally:
        if cursor:
            cursor.close()



            
def get_chatroom_messages(post_id, chatroom_id, conn):
    try:
        cursor = conn.cursor()

        messages = []
        query = "SELECT * FROM MESSAGE WHERE PID = :1 AND CID = :2"
        cursor.execute(query, [post_id, chatroom_id])

        for row in cursor.fetchall():
            messages.append({
                "PID": row[0],
                "CID": row[1],
                "TIME": row[2].isoformat() if row[2] else None,
                "IS_CREATOR": row[3],
                "MSG_CONTENT": row[4]
            })

        return json.dumps(messages)

    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        if cursor:
            cursor.close()
            
def create_or_verify_chatroom(post_id, creator_uid, conn):
    try:
        cursor = conn.cursor()

        # 게시물의 작성자를 확인
        cursor.execute("SELECT \"UID\" FROM POST WHERE POST_ID = :1", [post_id])
        result = cursor.fetchone()

        # 자신의 게시물인 경우 채팅방을 열 수 없음
        if result and result[0] == creator_uid:
            return {"error": "Cannot open a chatroom for your own post."}

        chatroom_data = check_existing_chatroom(post_id, creator_uid, conn)

        # Existing chatroom found or new one created
        if chatroom_data["exists"]:
            return json.dumps({"chatroom_id": chatroom_data["CHATROOM_ID"]})
        else:
            chatroom_id = create_new_chatroom(post_id, creator_uid, conn)
            return json.dumps({"chatroom_id": chatroom_id})

    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        if cursor:
            cursor.close()
            
            
def get_chatroom_creator(post_id, chatroom_id, conn):
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT CREATOR_UID FROM CHATROOM WHERE PID = :1 AND CHATROOM_ID = :2", (post_id, chatroom_id))
        result = cursor.fetchone()
        return json.dumps({"CREATOR_UID": result[0]}) if result else json.dumps({"error": "Chatroom not found"})

    except Exception as e:
        return json.dumps({"error": str(e)})
    finally:
        cursor.close()
        
        
async def save_message(pid: str, chatroom_id: str, data: str, conn):
    cursor = None  # cursor 초기화
    try:
        cursor = conn.cursor()

        # JSON 데이터 파싱
        message_data = json.loads(data)
        
        pid = message_data.get("PID")  # Post ID
        chatroom_id = message_data.get("CID")  # Chatroom ID
        time = message_data.get("TIME")  # 메시지 시간
        is_creator = message_data.get("IS_CREATOR")  # 채팅방 생성자 여부
        msg_content = message_data.get("MSG_CONTENT")  # 메시지 내용

        # 메시지 데이터베이스에 저장
        query = """
            INSERT INTO MESSAGE (PID, CID, TIME, IS_CREATOR, MSG_CONTENT)
            VALUES (:1, :2, TO_TIMESTAMP(:3, 'YYYY-MM-DD HH24:MI:SS.FF'), :4, :5)
        """
        cursor.execute(query, (pid, chatroom_id, time, is_creator, msg_content))
        conn.commit()

    except oracledb.DatabaseError as e:
        print(f"Database error: {e}")
        raise

    finally:
        if cursor:
            cursor.close()