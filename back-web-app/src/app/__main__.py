import uvicorn
from .settings import settings
# точка входа и запуск
# запускаем как модуль
uvicorn.run(
    'app.app:app',
    host=settings.server_host,
    port=int(settings.server_port),
    reload=True,
)
