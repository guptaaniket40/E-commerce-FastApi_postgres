from fastapi import FastAPI
from .database import Base, engine
from .routers.router import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Ecommerce API")

app.include_router(router)


@app.get("/")
def home():
    return {"message": "API running"}