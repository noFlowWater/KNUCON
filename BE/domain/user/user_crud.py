from domain.user.user_schema import UserRegister, UserLogin, UserQuit, LoginIdUniqueCheck
from datetime import datetime, timedelta
from util import generate_unique_id
from jose import jwt


# JWT 설정
SECRET_KEY = "10d51693e4a88a9d01f0817eda9aabd6d2a7f50d5afa823ffff133c8e2ada3eb"  # 시크릿 키 설정
ALGORITHM = "HS256"  # 사용할 알고리즘 설정

def check_login_id(login_id :LoginIdUniqueCheck , conn) -> str:
    try:
        # Prepare the SQL query to check if the login_id exists in the database
        query = "SELECT COUNT(*) FROM \"USER\" WHERE login_id = :login_id"
        
        # Execute the query
        cursor = conn.cursor()
        params = {'login_id': login_id.login_id}
        cursor.execute(query, params)
        result = cursor.fetchone()

        # Check the result
        if result[0] > 0:
            # If the count is greater than 0, the login_id is not unique
            return {"is_unique": False}
        else:
            # If the count is 0, the login_id is unique
            return {"is_unique": True}
    except Exception as e:
        # Log exception details here
        return {"error": str(e)}
    
def register_user(user_register: UserRegister, conn) -> str:
    try:
        cursor = conn.cursor()
        # 고유한 user_id 생성
        user_id = generate_unique_id(conn, 'U', 'USER', 'user_id') # create unique user_id 

        # 사용자 등록 쿼리 실행
        cursor.execute("INSERT INTO \"USER\" VALUES (:1, :2, :3, :4, :5)", (user_id, user_register.name, user_register.login_id, user_register.login_password, user_register.phone_number))
        conn.commit()
        msg = f'<<< User registration complete! user_id : {user_id}'
    except Exception as e:
        msg = f'Register failed:{e}'

    finally:
        print(f"\n {msg} \n")
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        return {"message": msg}

def login_user(user_login: UserLogin, conn) -> str:

    cursor = conn.cursor()
    try:
        print("\n >>> Trying Log-in\n")
        cursor.execute("SELECT user_id, name FROM \"USER\" WHERE login_id = :1 AND login_password = :2", (user_login.login_id, user_login.login_password))
        result = cursor.fetchone()
        print(f"result : {result}")
        if result:
            user_id, user_name = result
            print("\n <<< Login successful \n")

            # JWT 토큰 생성
            expiration = datetime.utcnow() + timedelta(hours=24)  # 예: 토큰 만료 시간을 24시간으로 설정
            token_data = {
                "sub": user_id,  # 'sub'에 사용자 ID 포함
                "exp": expiration
            }
            token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
            print(token)
            
            return {"user_name": user_name, "token": token}  # 사용자 이름과 토큰 반환

        else:
            print("\n <<< Login failed: Invalid credentials \n")
            return "Login failed"  # 로그인 실패 메시지 반환
        
    except Exception as e:
        print('Error during login:', e)
        return "Error in login process"  # 오류 메시지 반환
    
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def logout_user(user_id: str) -> str:
    print(f"{user_id} logged out")
    return f"{user_id} logged out"


def quit_user(user_id: str, user_quit: UserQuit, conn) -> str:
    cursor = conn.cursor()

    try:
        # 사용자 비밀번호 확인
        cursor.execute("SELECT COUNT(*) FROM \"USER\" WHERE user_id = :1 AND login_password = :2", (user_id, user_quit.login_password))
        (password_match_count,) = cursor.fetchone()

        if password_match_count == 0:
            return "Quit failed: Incorrect password"

        if user_quit.quit_confirm:
            # 사용자의 이름을 '(알 수 없음)'으로 업데이트
            cursor.execute("UPDATE \"USER\" SET name = '(알 수 없음)' WHERE user_id = :1", (user_id,))
            conn.commit()
            return "User successfully quit"
        else:
            return "Quit cancelled by user"

    except Exception as e:
        print('Error during quit process:', e)
        return "Error in quit process"

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

