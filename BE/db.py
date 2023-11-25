import os
import platform

import oracledb

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
try: # init_oracle client
        oracledb.init_oracle_client(lib_dir = lib_dir)
except oracledb.Error as e:
    pass    # arch warning occurs, but ignore for now

USER_ID = "dacsternary"
USER_PW = "pass"

def get_db_connection(): # get db connection, will be used in DI
    try:
        conn = oracledb.connect(user = USER_ID, password = USER_PW, dsn = CONN_STR) # connect oracledb
        return conn
    except oracledb.DatabaseError as e:
        error, = e.args
        print("failed to connect oracledb: {error.message}")
        return None