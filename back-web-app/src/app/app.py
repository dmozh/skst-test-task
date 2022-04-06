from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api import router, ws_prices

# главный объект приложения
app = FastAPI()

# ориджины, поставил звезду потому что это дев
origins = [
    "*"
]

# навешиваем мидлваре
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# В общем история такая, роутер не умеет работать с вебсокетами
# поэтому костылек
app.add_api_websocket_route("/api/ws/prices/{product}/", ws_prices)

app.include_router(router)
