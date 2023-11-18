import os
os.chdir('C:\oracle2\instantclient_19_21')
os.putenv('NLS_LANG','AMERICAN_AMERICA.UTF8')

import oracledb
import requests
import json
import random  # Import random module
import sys
from domain.user.user_schema import UserRegister, UserLogin#, UserQuit


print("---- Start of Oracle-Python Test ---\n")
USER_ID = "dacsternary"
USER_PW = "pass"
CONN_STR = "localhost:1521/orcl2"

lib_dir = "C:\oracle2\instantclient_19_21"
try:
    print("\n >>> Oracle client initialization starts ...\n")
    oracledb.init_oracle_client(lib_dir=lib_dir)
except Exception as err:
    print("Error connecting: cx_Oracle.init_oracle_client()")
    print(err)
    sys.exit(1)

print("\n <<< Oracle client initialization ended ...\n")

try:
    conn = oracledb.connect(user=USER_ID, password=USER_PW, dsn=CONN_STR)
except:
    print('Cannot get a connection.')

# 데이터베이스 연결 및 커서 생성
cursor = conn.cursor()

def register_user(user_register: UserRegister) -> str:
    
    try:
        # login_id 존재 여부 확인
        cursor.execute("SELECT COUNT(*) FROM \"USER\" WHERE login_id = :1", (user_register.login_id,))
        (login_id_count,) = cursor.fetchone()

        if login_id_count > 0:
            print("\n <<< Register failed: login_id already exists \n")
            return "Register failed: login_id already exists"

        # 랜덤 user_id 생성
        user_id = 'U' + ''.join([str(random.randint(0, 9)) for _ in range(7)])

        # 사용자 등록 쿼리 실행
        cursor.execute("INSERT INTO \"USER\" VALUES (:1, :2, :3, :4, :5)", (user_id, user_register.name, user_register.login_id, user_register.login_password, user_register.phone_number))
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
    try:
        print("\n >>> Trying Log-in\n")
        cursor.execute("SELECT name FROM \"USER\" WHERE login_id = :1 AND login_password = :2", (user_login.login_id, user_login.login_password))
        result = cursor.fetchone()
        print(f"result : {result}")
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

"""
def quit_user(user_id: str, user_quit: UserQuit) -> str:
    conn = None
    cursor = None
    try:
        # 비밀번호 확인을 위한 쿼리
        cursor.execute("SELECT user_id FROM USER WHERE user_id = :1 AND login_password = :2", (user_id, user_quit.login_password))
        result = cursor.fetchone()

        if result and user_quit.quit_check:
            cursor.execute("DELETE FROM USER WHERE user_id = :1", [user_id])
            conn.commit()
            return "User quit successful"
        else:
            return "User quit failed: Invalid credentials or cancellation"

    except Exception as e:
        return f"Error in quit process: {e}"

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
"""

def logout_user(user_id: str) -> str:
    print(f"{user_id} logged out")
    return f"{user_id} logged out"
