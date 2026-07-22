from fastapi import FastAPI
from app.api.ticket import router as ticket_router
from fastapi.middleware.cors import CORSMiddleware
from app.middleware.response_time import ResponseTimeMiddleware

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

@app.get("/")
def health_check():
    return {"message": "Hello"}