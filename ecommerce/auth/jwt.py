from datetime import datetime, timedelta

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from jose import JWTError, jwt

from sqlalchemy.orm import Session

from ecommerce.auth import schema
from ecommerce import db
from ..user import validator


import os
from dotenv import load_dotenv
load_dotenv('./ecommerce/.env')


SECRET_KEY = os.getenv("SECRET_KEY")                                            
ALGORITHM = os.getenv("ALGORITHM")                                         
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))     


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")                          



# function for creating access token
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt



def verify_token(token: str, credentials_exception: dict):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        email: str = payload.get("sub")

        if email is None:                          
            raise credentials_exception

        token_data = schema.TokenData(email=email)

        return token_data                         
    except JWTError:
        raise credentials_exception



async def get_current_user(token: str = Depends(oauth2_scheme), database: Session = Depends(db.get_db)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not verify token, token expired",
        headers={"WWW-AUTHENTICATE": "Bearer", }
    )

    current_user_email = verify_token(token=token, credentials_exception=credentials_exception).email

    current_user = await validator.verify_email_exist(current_user_email, database)

    return current_user

