from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional

from ecommerce import db

from ecommerce.auth.jwt import get_current_user
from ecommerce.user.schema import User

from .schema import ShowCart

from .services import add_to_cart, get_all_items, remove_cart_item, remove_cart


router = APIRouter(
    tags=['Carts'],
    prefix='/cart'
)



@router.get('/', response_model=ShowCart)           
async def get_all_cart_items(current_user: User = Depends(get_current_user), database: Session = Depends(db.get_db)):
    """
        ## This endpoint list all the cart items
    """
    result = await get_all_items(current_user, database)
    return result



@router.get('/add', status_code=status.HTTP_201_CREATED)
async def add_product_to_cart(product_id: int, quantity: Optional[int] = 1, current_user: User = Depends(get_current_user), database: Session = Depends(db.get_db)):
    """
        ## Add product/item to cart
        This endpoint requires the following url/path parameter :
        ```
            - product_id: str
            - quantity: Optional[str]
        ```
    """
    result = await add_to_cart(product_id, quantity, current_user, database)
    return result



@router.delete('/cart_item/{cart_item_id}', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def remove_cart_item_by_id(cart_item_id: int, current_user: User = Depends(get_current_user), database: Session = Depends(db.get_db)):
    """
        ## Remove/Delete single Cart Item
        This endpoint requires the cart item id as url/path parameter.
    """
    await remove_cart_item(cart_item_id, current_user, database)



@router.delete('/remove_cart', status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def remove_user_cart(current_user: User = Depends(get_current_user), database: Session = Depends(db.get_db)):
    """
        ## Remove/Delete the cart of User
    """
    await remove_cart(current_user, database)


