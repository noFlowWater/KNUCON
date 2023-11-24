import os
import platform
import random  # Import random module
from datetime import datetime, timedelta

import oracledb
from jose import jwt

from domain.user.user_schema import UserRegister, UserLogin, UserQuit

# Handle env related with OS
os_name = platform.system()
if os_name == "Windows":
    os.chdir('C:\\oracle2\\instantclient_19_21')
    lib_dir = 'C:\\oracle2\\instantclient_19_21'
    CONN_STR = "localhost:1521/orcl2"
elif os_name == "Darwin":
    os.chdir('/opt/oracle/instantclient_19_8')
    lib_dir = '/opt/oracle/instantclient_19_8'
    CONN_STR = "localhost:1521/xe"

os.putenv('NLS_LANG','AMERICAN_AMERICA.UTF8')
USER_ID = "dacsternary"
USER_PW = "pass"

try:
    oracledb.init_oracle_client(lib_dir=lib_dir)
except Exception as err:
    print(err)

try:
    conn = oracledb.connect(user=USER_ID, password=USER_PW, dsn=CONN_STR)
except:
    print('Cannot get a connection.')

# 데이터베이스 연결 및 커서 생성
cursor = conn.cursor()

def generate_unique_user_id():
    while True:
        # 랜덤 user_id 생성
        user_id = 'U' + ''.join([str(random.randint(0, 9)) for _ in range(7)])
        
        # 생성한 user_id가 이미 데이터베이스에 존재하는지 확인
        cursor.execute("SELECT COUNT(*) FROM \"USER\" WHERE user_id = :1", (user_id,))
        (user_id_count,) = cursor.fetchone()
        
        if user_id_count == 0:
            return user_id  # 데이터베이스에 존재하지 않는 고유한 user_id 반환

def register_user(user_register: UserRegister) -> str:
    try:
        # login_id 존재 여부 확인
        cursor.execute("SELECT COUNT(*) FROM \"USER\" WHERE login_id = :1", (user_register.login_id,))
        (login_id_count,) = cursor.fetchone()

        if login_id_count > 0:
            print("\n <<< Register failed: login_id already exists \n")
            return "Register failed: login_id already exists"

        # 고유한 user_id 생성
        user_id = generate_unique_user_id()

        # 사용자 등록 쿼리 실행
        cursor.execute("INSERT INTO \"USER\" VALUES (:1, :2, :3, :4, :5)", (user_id, user_register.name, user_register.login_id, user_register.login_password, user_register.phone_number))
        conn.commit()
        print("\n <<< User registration complete \n")
        return user_id  # user_id 반환

    except Exception as e:
        print('Register failed:', e)
        return "Register failed"  # 실패 메시지 반환

    finally:
        # 커서와 데이터베이스 연결 종료
        if cursor:
            cursor.close()
        if conn:
            conn.close()

# JWT 설정
SECRET_KEY = "appleisgreat1234"  # 시크릿 키 설정
ALGORITHM = "HS256"  # 사용할 알고리즘 설정

def login_user(user_login: UserLogin) -> str:
    try:
        print("\n >>> Trying Log-in\n")
        cursor.execute("SELECT user_id, name FROM \"USER\" WHERE login_id = :1 AND login_password = :2", (user_login.login_id, user_login.login_password))
        result = cursor.fetchone()
        print(f"result : {result}")
        if result:
            user_id, user_name = result
            print("\n <<< Login successful \n")

            # JWT 토큰 생성
            expiration = datetime.utcnow() + timedelta(hours=1)  # 예: 토큰 만료 시간을 1시간으로 설정
            token_data = {
                "sub": user_id,  # 'sub'에 사용자 ID 포함
                "exp": expiration
            }
            token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)

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


def quit_user(user_id: str, user_quit: UserQuit) -> str:
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

