from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG = False

    database_host = ""
    database_name = ""
    database_user = ""
    database_pwd = ""
    database_port = ""

    pipe_host = ""
    pipe_port = ""

    rabbit_user = "guest"
    rabbit_pwd = "guest"
    rabbit_host = "localhost"


settings = Settings(
    _env_file='.env',
    _env_file_encoding='utf-8'
)
