from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models

app = FastAPI(title="AI Tender Agent API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from routers import profile, documents

app.include_router(profile.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}
