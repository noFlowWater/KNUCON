import os 
import oracledb

# set environment variables and lib_dir
os.putenv('NLS_LANG', 'AMERICAN_AMERICA.UTF8')
lib_dir = "/opt/oracle/instantclient_19_8"

try: # init_oracle client
        oracledb.init_oracle_client(lib_dir = lib_dir)
except oracledb.Error as e:
    pass    # arch warning occurs, but ignore for now

USER_ID = "dacsternary"
USER_PW = "pass"
CONN_STR = "localhost:1521/xe"

def get_db_connection(): # get db connection, will be used in DI
    try:
        conn = oracledb.connect(user = USER_ID, password = USER_PW, dsn = CONN_STR) # connect oracledb
        return conn
    except oracledb.DatabaseError as e:
        error, = e.args
        print("failed to connect oracledb: {error.message}")
        return None