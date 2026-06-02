from fastapi import FastAPI

from src.urls.v1 import auth,products,cart,orders


app = FastAPI(
    title="Ecommerce API"
)

app.include_router(auth.router,prefix="/api/v1")
app.include_router(products.router,prefix="/api/v1")
app.include_router(cart.router, prefix="/api/v1")
app.include_router(orders.router,prefix="/api/v1")


@app.get("/")
async def root():
    return {"message": "Ecommerce API is running"}