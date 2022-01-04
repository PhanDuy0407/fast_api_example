from pydantic import BaseSettings


class Setting(BaseSettings):
    db_username: str
    db_password: str
    db_name: str
    db_host: str
    db_port: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    class Config:
        env_file = ".env"


setting = Setting()
