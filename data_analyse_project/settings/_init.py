import os
from functools import cache
from typing import Type

from data_analyse_project.settings._app import AppEnvEnum, AppSettings
from data_analyse_project.settings._dev import DevAppSettings
from data_analyse_project.settings._prod import ProdAppSettings


@cache
def load_settings() -> AppSettings:
    env = os.environ.get("APP_ENV", AppEnvEnum.prod.value)
    app_env = AppEnvEnum(env)

    if app_env in (AppEnvEnum.dev,):
        try:
            from icecream import ic, install  # type: ignore[attr-defined]  # noqa: PLC0415

            ic.configureOutput(includeContext=True, prefix="~~> ")
            install()
        except ModuleNotFoundError:
            ...

    _settings: Type[ProdAppSettings] | Type[DevAppSettings] = {  # type: ignore[assignment]
        AppEnvEnum.prod: ProdAppSettings,
        AppEnvEnum.dev: DevAppSettings,
    }[app_env]

    return _settings()
