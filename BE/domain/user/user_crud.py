import os
os.chdir('C:\oracle2\instantclient_19_21')
os.putenv('NLS_LANG','AMERICAN_AMERICA.UTF8')

import oracledb

print("---- Start of Oracle-Python Test ---\n")
USER_ID = "dacsternary"
USER_PW = "pass"
CONN_STR = "localhost:1521/orcl2"

import requests
import json
import random  # Import random module
from utils import handle_response
from domain.user.user_schema import UserRegister, UserLogin, UserQuit, UserLogout

with open('./conf.json','r') as conf:
    config = json.load(conf)

def register_user(user_register: UserRegister) -> str:
    conn = None
    cursor = None
    try:
        # 데이터베이스 연결 및 커서 생성
        conn = establish_database_connection()
        cursor = conn.cursor()

        # 랜덤 user_id 생성
        user_id = 'U' + ''.join([str(random.randint(0, 9)) for _ in range(7)])

        # 사용자 데이터 준비
        data = {
            'user_id': user_id,
            'name': user_register.name,
            'login_id': user_register.login_id,
            'login_password': user_register.login_password,
            'phone_number': user_register.phone_number
        }

        # 사용자 등록 쿼리 실행
        cursor.executemany("INSERT INTO USER (user_id, name, login_id, login_password, phone_number) VALUES (:1, :2, :3, :4, :5)", [data])
        conn.commit()
        print("\n <<< User registration complete \n")
        return user_id  # user_id 반환

    except Exception as e:  # 예외 처리
        print('Register failed:', e)
        return "Register failed"  # 실패 메시지 반환

    finally:
        # 커서와 데이터베이스 연결 종료
        if cursor:
            cursor.close()
        if conn:
            conn.close()
   
def login_user(user_login: UserLogin) -> str:
    conn = None
    cursor = None
    data = {
        'login_id': user_login.login_id,
        'login_password': user_login.login_password
    }

    try:
        print("\n >>> Trying Log-in\n")
        cursor.execute("SELECT name FROM USER WHERE login_id = :1 AND login_password = :2", (user_login.login_id, user_login.login_password))
        result = cursor.fetchone()

        if result:
            print("\n <<< Login successful \n")
            return result[0]  # user name 반환
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

def quit_user(user_quit: UserQuit) -> str:
    conn = None
    cursor = None
    try:
        # 데이터베이스 연결 및 커서 생성
        conn = establish_database_connection()
        cursor = conn.cursor()

        # 비밀번호 확인을 위한 쿼리
        cursor.execute("SELECT user_id FROM USER WHERE login_id = :1 AND login_password = :2", [user_quit.login_id, user_quit.login_password])
        result = cursor.fetchone()

        if result:
            # 사용자 삭제 쿼리 실행
            cursor.execute("DELETE FROM USER WHERE user_id = :1", [result[0]])
            conn.commit()
            print("\n <<< User quit successful \n")
            return "User quit successful"  # 탈퇴 성공 메시지 반환
        else:
            print("\n <<< User quit failed: Invalid credentials \n")
            return "User quit failed"  # 탈퇴 실패 메시지 반환

    except Exception as e:
        print('Error during user quit:', e)
        return "Error in quit process"  # 오류 메시지 반환

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()

def logout_user(user_logout: UserLogout) -> str:
    if user_logout.confirm_logout:
        # 여기서 세션 또는 토큰 무효화 로직을 구현 -> 나중에 어플리케이션 단계에서 추가 구현해야함
        print("\n <<< User logged out successfully \n")
        return "User logged out successfully"
    else:
        return "Logout cancelled"