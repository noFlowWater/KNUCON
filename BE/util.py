import random
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
SECRET_KEY = "10d51693e4a88a9d01f0817eda9aabd6d2a7f50d5afa823ffff133c8e2ada3eb"  # Make sure to keep it consistent
ALGORITHM = "HS256"

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

def get_current_user_id(token: str = Depends(oauth2_scheme)) -> str:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
