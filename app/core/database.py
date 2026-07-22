from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine,async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from app.core.config import settings

engine=create_async_engine(settings.DATABASE_URL,pool_size=10, max_overflow=20)
async_session_maker=async_sessionmaker(engine, 
                                        autocommit=False, autoflush=False)
class Base(DeclarativeBase):
    pass
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
       try:
           yield session
           await session.commit()
       except Exception as e:
           await session.rollback()
           raise e
       finally:
           await session.close()