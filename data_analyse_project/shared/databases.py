import logging
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager

from asyncpg import Pool, create_pool

from data_analyse_project.settings._app import AppSettings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def pool_maker(settings: AppSettings) -> AsyncGenerator[Pool, None]:
    logger.info("Connecting to PostgreSQL")
    database_url = settings.postgres_dsn.render_as_string()

    pool = await create_pool(
        dsn=str(database_url),
        min_size=settings.postgres_pool_min_connection_count,
        max_size=settings.postgres_pool_max_connection_count,
    )
    yield pool
    await pool.close()
