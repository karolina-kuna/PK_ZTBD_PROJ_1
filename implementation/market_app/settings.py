from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    log_level: str = Field(..., env="LOG_LEVEL")
    app_name: str = "Authors Service APP"

    db_username: str = Field(..., env="DB_USERNAME")
    db_password: str = Field(..., env="DB_PASSWORD")
    db_host: str = Field(..., env="DB_HOST")
    db_port: str = Field(..., env="DB_PORT")
    db_name: str = Field(..., env="DB_NAME")


SETTINGS = Settings()
