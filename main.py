from fastapi import FastAPI

from ecommerce import config

from ecommerce.auth import router as auth_router
from ecommerce.user import router as user_router
from ecommerce.products import router as product_router
from ecommerce.cart import router as cart_router
from ecommerce.orders import router as order_router


description = """
        *** FastAPI Ecommerce Application ***
"""


app = FastAPI(
    title="EcommerceApp",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Agent47",
        "url": "http://x-force.example.com/contact/",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
    },
    # docs_url='/private_docs',                 
)



app.include_router(auth_router.router)
app.include_router(user_router.router)
app.include_router(product_router.router)
app.include_router(cart_router.router)
app.include_router(order_router.router)


@app.get("/")
async def root():
    """
        ## Hi, this is ecommerce app.
    """
    return {"message": "Welcome To FastAPI Ecommerce Site"}
