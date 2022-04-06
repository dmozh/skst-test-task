from pydantic import BaseSettings


class Settings(BaseSettings):
    DEBUG = False

    server_host = ''
    server_port = ''

    database_host = ""
    database_name = ""
    database_user = ""
    database_pwd = ""
    database_port = ""

    pipe_host = ""
    pipe_port = ""

    cache_host = ""
    cache_port = ""


settings = Settings(
    _env_file='../.env',
    _env_file_encoding='utf-8'
)
