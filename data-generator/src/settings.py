from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG = False

    tickers_num = 100
    data_parts = 4

    cache_host = "localhost"
    cache_port = 6379

    rabbit_user = "guest"
    rabbit_pwd = "guest"
    rabbit_host = "localhost"


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
