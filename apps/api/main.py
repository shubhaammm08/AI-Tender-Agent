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

@app.get("/api/v1/health")
def health_check():
    return {"status": "ok"}
