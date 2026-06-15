from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from src.database.config import Config

 
Base = declarative_base()

 
engine = create_async_engine(
    Config.DB_CONFIG,
    echo=False
)
 
SessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)
 
async def get_db():
    async with SessionLocal() as session:
        yield session