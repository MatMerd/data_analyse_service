from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Self

import structlog
from asyncpg.pool import Pool
from asyncpg.transaction import Transaction

logger = structlog.get_logger(__name__)


class BaseRepository:
    def __init__(self, pool: Pool) -> None:
        self._pool = pool

        self._in_transaction = False
        self._transactional_session: Transaction | None = None

    @asynccontextmanager
    async def transaction(self: Self) -> AsyncGenerator[None, None]:
        # Custom transaction wrapper for `autobegin=True` configuration.
        # In this mode session execute all queries in transaction.
        #  For this reason usage of begin() after any sql query will raise error.
        if self._in_transaction:
            raise RuntimeError("Repository already start transaction")

        async with self.session() as session:
            self._transactional_session = session

            try:
                self._in_transaction = True
                yield
                logger.debug("session commit", extra={"session": session})
                await session.commit()
            except Exception as error:
                logger.debug("session rollback", extra={"session": session, "error": error})
                await session.rollback()
                raise
            finally:
                self._in_transaction = False
                self._transactional_session = None

    @asynccontextmanager
    async def session(self: Self) -> AsyncGenerator[Transaction, None]:
        if self._transactional_session:
            yield self._transactional_session
        else:
            async with self._pool.acquire() as conn:
                yield conn.transaction()
