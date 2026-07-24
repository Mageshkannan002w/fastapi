from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.ticket import router as ticket_router
from app.api.ai import router as ai_router
from app.middleware.response_time import ResponseTimeMiddleware
from app.core.database import get_db, engine, Base

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application starting up...")
    try:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        logger.info("Database tables initialized successfully.")
    except Exception as e:
        logger.warning(f"Database initialization skipped or failed: {e}")

    yield

    logger.info("Application shutting down...")
    try:
        await engine.dispose()
        logger.info("Database engine connection pool disposed.")
    except Exception as e:
        logger.warning(f"Error during shutdown: {e}")


app = FastAPI(lifespan=lifespan)

app.add_middleware(ResponseTimeMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(ticket_router)
app.include_router(ai_router)


@app.get("/ready")
def ready_check():
    return {"message": "Yeah Application works fine"}


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    return {
        "session_exists": db is not None
    }
