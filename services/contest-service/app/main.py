from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
import uvicorn

from app.database import init_db
from app.routers import contests, problems, registrations
from app.config import settings

app = FastAPI(
    title="Contest Service",
    description="Contest and problem management service for Codeforces platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(contests.router, prefix="/api/v1/contests", tags=["contests"])
app.include_router(problems.router, prefix="/api/v1/problems", tags=["problems"])
app.include_router(registrations.router, prefix="/api/v1/registrations", tags=["registrations"])

# Prometheus metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.on_event("startup")
async def startup_event():
    init_db()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "contest-service"}

@app.get("/")
async def root():
    return {"message": "Contest Service API", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

