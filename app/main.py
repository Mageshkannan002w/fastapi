from fastapi import FastAPI
from app.api.ticket import router as ticket_router
from app.api.ai import router as ai_router
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.response_time import ResponseTimeMiddleware
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
app = FastAPI()
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
@app.get("/ready")
async def health_check(db: AsyncSession = Depends(get_db)):
    return {
        "session_exists": db is not None
    }
