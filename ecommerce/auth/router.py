from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm          
                                                                
from sqlalchemy.orm import Session


from ecommerce import db
from ecommerce.auth import schema
from ecommerce.user import hashing
from ecommerce.user.models import User

from .jwt import create_access_token
from ..user import validator


router = APIRouter(                     
    tags=['auth']
)



@router.post('/login', response_model=schema.Token, status_code=status.HTTP_200_OK)
async def login(request: OAuth2PasswordRequestForm = Depends(), database: Session = Depends(db.get_db)):

    user = await validator.verify_email_exist(request.username, database)
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Invalid User Credentials')

    if not hashing.verify_password(request.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Invalid User Credentials')

    
    access_token = create_access_token(data={"sub": user.email})   

    return {"access_token": access_token, "token_type": "bearer"}

