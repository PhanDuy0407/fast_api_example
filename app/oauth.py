from fastapi import Depends
from jose import JWTError, jwt
from datetime import datetime, timedelta
from starlette import status
from fastapi.exceptions import HTTPException
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from .config import setting

# SECRET_KEY
# Algorithm
# Expiration time
oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")
SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes


def create_access_token(data: dict):
    data_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    data_encode.update({"exp": expire})

    return jwt.encode(data_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_access_token(token: str, credentials_exception):
    try:
        payload: dict = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        if not user_id:
            raise credentials_exception
        token_data = schemas.TokenData(id=user_id)
    except JWTError:
        raise credentials_exception

    return token_data


def get_current_user(token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                          detail="Could not validate credentials",
                                          headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)
