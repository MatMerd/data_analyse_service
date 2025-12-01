from pydantic import Field, SecretStr
from pydantic_settings import SettingsConfigDict

from data_analyse_project.settings._app import AppSettings, LogLevelEnum


# TODO: добавить конфиги для LLM хоста
class DevAppSettings(AppSettings):
    model_config = SettingsConfigDict(alias_generator=str.upper, env_file=".env")

    app_log_level_name: LogLevelEnum = Field(alias="APP_LOG_LEVEL", default=LogLevelEnum.DEBUG)
    asgi_ssl: bool = True

    secret_key: SecretStr = SecretStr("jwt_secret_dev_saZ/fme8FKWVxFVKaj3VV63Z830=")

    postgres_username: str = "data_analyse_dev"
    postgres_database: str = "data_analyse_dev"
    postgres_password: SecretStr = SecretStr("data_analyse_dev_pass")
    postgres_host: str = "localhost"
    postgres_port: int = 5432
