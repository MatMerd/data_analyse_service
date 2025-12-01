from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, cast

from asyncpg import Pool
from fastapi import FastAPI, Request
from niquests import AsyncSession
from rodi import Container

from data_analyse_project.settings._app import AppSettings
from data_analyse_project.settings._init import load_settings
from data_analyse_project.shared.clients import http_session_maker
from data_analyse_project.shared.databases import pool_maker


@asynccontextmanager
async def build_container(app: FastAPI) -> AsyncGenerator[None, Any]:  # noqa: PLR0915
    settings = load_settings()
    async with (
        http_session_maker(settings) as http_session,
        pool_maker(settings) as pool,
    ):
        container = Container()
        container.add_instance(settings, AppSettings)
        container.add_instance(http_session, AsyncSession)
        container.add_instance(pool, Pool)
        app.state.container = container
        yield


async def get_container(request: Request) -> Container:
    return cast(Container, request.app.state.container)
