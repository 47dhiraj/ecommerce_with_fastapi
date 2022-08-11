from typing import List
from fastapi import HTTPException, status
from fastapi import BackgroundTasks

from ecommerce.cart.models import Cart, CartItems
from ecommerce.orders.models import Order, OrderDetails
from ecommerce.user.models import User
from .mail import order_email_background


async def place_order(background_tasks: BackgroundTasks, address: str, current_user, database) -> Order:                      

    user_info = database.query(User).filter(User.email == current_user.email).first()   
    cart = database.query(Cart).filter(Cart.user_id == user_info.id).first()

    try:
        cart_items_objects = database.query(CartItems).filter(Cart.id == cart.id)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Items found in Cart !")

    if not cart_items_objects.count():                         
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Items found in Cart !")

    total_amount: float = 0.0                                  

    for item in cart_items_objects:                            
        total_amount += item.products.price * item.quantity

    new_order = Order(order_amount=total_amount,               
                      shipping_address=address,
                      customer_id=user_info.id)

    database.add(new_order)
    database.commit()                                          
    database.refresh(new_order)                                


    bulk_order_details_objects = list()                        

    for item in cart_items_objects:                             
        new_order_details = OrderDetails(order_id=new_order.id, product_id=item.products.id, quantity=item.quantity)   
        bulk_order_details_objects.append(new_order_details)   

    database.bulk_save_objects(bulk_order_details_objects)      
    database.commit()              

    order_email_background(background_tasks, 'Order Successfully Placed !', current_user.email, {"title": "Order Successfully Placed !", "name": current_user.name})

    database.query(CartItems).filter(CartItems.cart_id == cart.id).delete()
  
    database.query(Cart).filter(Cart.user_id == user_info.id).delete()

    database.commit()                                           

    return new_order                                          



async def get_order_listing(current_user, database) -> List[Order]:          
    user_info = database.query(User).filter(User.email == current_user.email).first()
    
    orders = database.query(Order).filter(Order.customer_id == user_info.id).all()
    
    return orders


