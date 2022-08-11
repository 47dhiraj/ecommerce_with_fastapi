from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text
from sqlalchemy.orm import relationship

from ecommerce.db import Base


class Category(Base):                                               
    __tablename__ = "category"                    

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    product = relationship("Product", back_populates="category")  

    def __str__(self):
        return f"<Category - {self.name}"



class Product(Base):                                                
    __tablename__ = "products"                      

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    quantity = Column(Integer, default=0, nullable=False)
    description = Column(Text)
    price = Column(Float)

    category_id = Column(Integer, ForeignKey('category.id', ondelete="CASCADE"), )          
    category = relationship("Category", back_populates="product")                          

    cart_items = relationship("CartItems", back_populates="products")                       

    order_details = relationship("OrderDetails", back_populates="product_order_details")  

    def __str__(self):
        return f"<Product - {self.name}"
