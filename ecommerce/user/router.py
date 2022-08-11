from fastapi import APIRouter, Depends, status, Response, HTTPException
from typing import List
from sqlalchemy.orm import Session

from fastapi import BackgroundTasks

from ecommerce import db

from ecommerce.auth.jwt import get_current_user, create_access_token
from ecommerce.user import hashing

from . import schema
from . import services
from . import validator
from .models import User

from .schema import PasswordResetRequest, PasswordReset
from .send_email import password_reset_request_email_background



router = APIRouter(                
    tags=['Users'],                 
    prefix='/user'                  
)



@router.post('/', status_code=status.HTTP_201_CREATED)
async def create_user_registration(request: schema.User, database: Session = Depends(db.get_db)):   

    """
        ## Register/Create a new user.
        This endpoints requires the following parameter:
        ```
            - name: str
            - email: str
            - password: str
        ```
    """

    user = await validator.verify_email_exist(request.email, database)

    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )

    new_user = await services.new_user_register(request, database)      

    return new_user



@router.get('/', response_model=List[schema.DisplayUser])              
async def get_all_users(database: Session = Depends(db.get_db), current_user: schema.User = Depends(get_current_user)):
    """
        ## List all the users in the system.
    """

    return await services.all_users(database)



@router.get('/{user_id}', response_model=schema.DisplayUser)            
async def get_user_by_id(user_id: int, database: Session = Depends(db.get_db), current_user: schema.User = Depends(get_current_user)):  
    """
        ## Get an user by its ID
        User detail can only be viewed by the same user and this endpoint takes user id as path parameter.
    """
    return await services.get_user_by_id(user_id, database)




@router.delete('/{user_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_user_by_id(user_id: int, database: Session = Depends(db.get_db), current_user: schema.User = Depends(get_current_user)):
    """
        ## Delete User
        This endpoints deletes the user if user id is provided as path paramter.
    """

    return await services.delete_user_by_id(user_id, database)



@router.post("/password_rest/request/", response_description="Password reset request")
async def password_reset_request(background_tasks: BackgroundTasks, request: PasswordResetRequest, database: Session = Depends(db.get_db)):
    
    user = await validator.verify_email_exist(request.email, database)

    if user is not None:
        token = create_access_token(data={"sub": user.email})

        reset_link = f"http://http://127.0.0.1:8000/user/reset?token={token}"

        password_reset_request_email_background(background_tasks, 'Reset your Password', user.email,
            {
                "title": "Password Reset",
                "name": user.name,
                "reset_link": reset_link
            }
        )

        return {"msg": "Email has been sent with instructions to reset your password."}

    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Your details not found, invalid email address"
        )


@router.put("/reset/", response_description="Password reset")
async def reset(token: str, request: PasswordReset, database: Session = Depends(db.get_db)):

    if len(request.password) >= 6:
        current_user = await get_current_user(token, database)

        user = await validator.verify_email_exist(current_user.email, database)
        if not user:
            raise HTTPException(status_code=404, detail=f"User not found")

        hashed_password = hashing.get_password_hash(request.password)
        result = await services.update_password(user, hashed_password, database)

        return result

    else:
        raise HTTPException(status_code=404, detail=f"Password cannot be less than 6 characters")


