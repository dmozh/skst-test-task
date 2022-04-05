from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router, ws_prices


app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:9000",
    "http://localhost:8080",
    "http://192.168.0.106",
    "http://192.168.0.106:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.add_api_websocket_route("/api/prices/{product}/ws", ws_prices)

app.include_router(router)
