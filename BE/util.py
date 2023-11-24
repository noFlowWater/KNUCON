import oracledb
import getpass
import random

server_prefix = "[Server]"

def generate_unique_id(conn, prefix, table_name, column_name):
    unique_id = ""
    check_id_sql = f"SELECT {column_name} FROM \"{table_name}\" WHERE {column_name} = :id"
    while True:
        # Generate a random ID with the specified prefix
        unique_id = prefix + "{:07d}".format(random.randint(0, 9999999))
        # Prepare and execute the SQL statement to check if the ID already exists
        with conn.cursor() as cursor:
            cursor.execute(check_id_sql, [unique_id])
            if not cursor.fetchone():
                # If the ID does not exist, break the loop
                break
    return unique_id

def server_print(*args, sep=' ', end='\n'):             # server_print is print function with prefix([Client])
    message = server_prefix + ' ' + sep.join(map(str, args)) + end
    print(message, end='')