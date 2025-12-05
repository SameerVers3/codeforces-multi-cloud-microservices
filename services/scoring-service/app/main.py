from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
import uvicorn

from app.database import init_db
from app.worker import start_worker
from app.config import settings

app = FastAPI(
    title="Scoring Service",
    description="Score calculation service for Codeforces platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

@app.on_event("startup")
async def startup_event():
    init_db()
    # Start background worker (non-blocking)
    import asyncio
    import threading
    
    def run_worker():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(start_worker())
    
    thread = threading.Thread(target=run_worker, daemon=True)
    thread.start()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "scoring-service"}

@app.get("/")
async def root():
    return {"message": "Scoring Service API", "version": "1.0.0"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

