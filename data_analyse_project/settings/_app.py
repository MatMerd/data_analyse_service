# mypy: disable-error-code="assignment"
import enum
import logging
from typing import Annotated, Self
from urllib.parse import quote, quote_plus

from pydantic import BaseModel, Field, SecretStr, field_validator
from pydantic_core import Url
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict

from data_analyse_project.shared import lib


class AppEnvEnum(enum.StrEnum):
    prod = "PROD"
    dev = "DEV"


class LogLevelEnum(enum.StrEnum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"


class URL(BaseModel):
    drivername: str
    host: str
    port: int
    database: str
    username: str | None = None
    password: str | None = None
    query: dict[str, tuple[str] | str] | None = None

    def render_as_string(self, *, hide_password: bool = True) -> str:
        s = self.drivername + "://"
        if self.username is not None:
            s += quote(self.username, safe=" +")
            if self.password is not None:
                s += ":" + ("***" if hide_password else quote(str(self.password), safe=" +"))
            s += "@"
        if ":" in self.host:
            s += f"[{self.host}]"
        else:
            s += self.host
        s += ":" + str(self.port)
        s += "/" + quote(self.database, safe=" +/")
        if self.query:
            keys = list(self.query)
            keys.sort()
            s += "?" + "&".join(
                f"{quote_plus(k)}={quote_plus(element)}" for k in keys for element in lib.to_list(self.query[k])
            )
        return s


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        alias_generator=str.upper, env_ignore_empty=True, case_sensitive=True, extra="allow", env_file=".env"
    )

    asgi_host: str = "0.0.0.0"  # noqa: S104
    asgi_port: int = 8000

    admin_host: str = "0.0.0.0"  # noqa: S104
    admin_port: int = 8001

    log_level_name: LogLevelEnum = Field(alias="LOG_LEVEL", default=LogLevelEnum.INFO)
    app_log_level_name: LogLevelEnum = Field(alias="APP_LOG_LEVEL", default=LogLevelEnum.INFO)

    secret_key: SecretStr

    postgres_username: str
    postgres_database: str
    postgres_password: SecretStr
    postgres_host: str
    postgres_port: int = 5432
    postgres_pool_min_connection_count: int = 3
    postgres_pool_max_connection_count: int = 50

    http_use_only_http_1: bool = True
    http_pool_size: int = 10
    http_retries: int = 3
    http_timeout: float = 0.5
    http_verify_request: bool = False

    @property
    def app_log_level(self: Self) -> int:
        return logging.getLevelNamesMapping()[self.app_log_level_name]

    @property
    def log_level(self: Self) -> int:
        return logging.getLevelNamesMapping()[self.log_level_name]

    @property
    def postgres_dsn(self) -> URL:
        return URL(
            drivername="postgresql",
            database=self.postgres_database,
            username=self.postgres_username,
            password=self.postgres_password.get_secret_value(),
            host=self.postgres_host,
            port=self.postgres_port,
        )
