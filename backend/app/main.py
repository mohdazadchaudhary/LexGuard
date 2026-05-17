from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.endpoints import analysis

app = FastAPI(
    title="LexGuard API",
    description="Backend API for LexGuard - AI Rights & Contract Intelligence System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analysis.router, prefix="/api/v1/analysis", tags=["analysis"])

@app.get("/")
def read_root():
    return {"message": "Welcome to LexGuard API. The system is running."}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
