from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import jwt, JWTError
from configs.db import db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

SECRET_KEY_P1 = "f027f67fabade699bfed696516c"
SECRET_KEY_P2 = "f51c4d3bfb26da70bf6bb06395ed0dba18b5b"  # openssl rand -hex 32
SECRET_KEY = "".join([SECRET_KEY_P1, SECRET_KEY_P2])
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_jwt_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_user_data_by_username(user_username: str):
    user_data = db.select('''select user_id, user_username, user_password from rbac_fastapi.users where user_username='{0}' '''.format("".join(user_username)))
    return user_data


def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
                                status_code=status.HTTP_401_UNAUTHORIZED,
                                detail="Could not validate credentials",
                                headers={"WWW-Authenticate": "Bearer"})
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_username: str = payload.get("sub")
        if user_username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user_data = get_user_data_by_username(user_username)
    if user_data is None:
        raise credentials_exception
    return user_data
