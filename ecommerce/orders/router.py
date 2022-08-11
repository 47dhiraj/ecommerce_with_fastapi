from typing import List

from fastapi import APIRouter, Depends, status
from fastapi import BackgroundTasks

from sqlalchemy.orm import Session
from ecommerce import db

from ecommerce.orders.services import place_order, get_order_listing

from ecommerce.auth.jwt import get_current_user
from ecommerce.user.schema import User

from .schema import ShowOrder


router = APIRouter(
    tags=['Orders'],
    prefix='/orders'
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=ShowOrder)    
async def place_order_processing(background_tasks: BackgroundTasks, address: str, current_user: User = Depends(get_current_user), database: Session = Depends(db.get_db)):
    result = await place_order(background_tasks, address, current_user, database)
    return result                        


@router.get('/', status_code=status.HTTP_200_OK, response_model=List[ShowOrder])
async def orders_list(current_user: User = Depends(get_current_user), database: Session = Depends(db.get_db)):
    result = await get_order_listing(current_user, database)
    return result

