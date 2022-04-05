import uvicorn
from .settings import settings

uvicorn.run(
    'app.app:app',
    host=settings.server_host,
    port=int(settings.server_port),
    reload=True,
)
