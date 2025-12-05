from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from prometheus_client import make_asgi_app
import uvicorn
import json
import redis
import asyncio

from app.database import get_db
from app.routers import leaderboard
from app.config import settings

app = FastAPI(title="Leaderboard Service", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(leaderboard.router, prefix="/api/v1/leaderboard", tags=["leaderboard"])

metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)

# WebSocket connections manager
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, list[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, contest_id: str):
        await websocket.accept()
        if contest_id not in self.active_connections:
            self.active_connections[contest_id] = []
        self.active_connections[contest_id].append(websocket)
    
    def disconnect(self, websocket: WebSocket, contest_id: str):
        if contest_id in self.active_connections:
            self.active_connections[contest_id].remove(websocket)
    
    async def broadcast(self, contest_id: str, message: dict):
        if contest_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[contest_id]:
                try:
                    await connection.send_json(message)
                except:
                    disconnected.append(connection)
            for conn in disconnected:
                self.active_connections[contest_id].remove(conn)

manager = ConnectionManager()

@app.websocket("/ws/leaderboard/{contest_id}")
async def websocket_endpoint(websocket: WebSocket, contest_id: str):
    await manager.connect(websocket, contest_id)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, contest_id)

@app.on_event("startup")
async def startup_event():
    # Subscribe to Redis pub/sub for leaderboard updates (non-blocking)
    import threading
    
    def run_subscriber():
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(subscribe_to_updates())
        except Exception as e:
            print(f"Warning: Could not start Redis subscription: {e}")
    
    thread = threading.Thread(target=run_subscriber, daemon=True)
    thread.start()

async def subscribe_to_updates():
    try:
        r = redis.from_url(settings.REDIS_URL)
        pubsub = r.pubsub()
        pubsub.subscribe("leaderboard_updates")
        
        for message in pubsub.listen():
            if message["type"] == "message":
                try:
                    data = json.loads(message["data"])
                    await manager.broadcast(data["contest_id"], data["leaderboard"])
                except Exception as e:
                    print(f"Error processing leaderboard update: {e}")
    except Exception as e:
        print(f"Redis subscription error: {e}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "leaderboard-service"}

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

