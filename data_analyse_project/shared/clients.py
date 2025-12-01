import logging
import urllib.parse
from collections.abc import AsyncIterator, Sequence
from contextlib import asynccontextmanager
from http import HTTPStatus
from typing import Any, AsyncGenerator

from descanso.client import (
    AsyncClient,
    AsyncResponseWrapper,
)
from descanso.request import HttpRequest, RequestTransformer
from descanso.response import ResponseTransformer
from niquests import AsyncSession, ReadTimeout, Response

from data_analyse_project.settings._app import AppSettings

logger = logging.getLogger(__name__)


class NiquestsResponseWrapper(AsyncResponseWrapper):
    def __init__(self, response: Response) -> None:
        self.status_code = response.status_code or HTTPStatus.INTERNAL_SERVER_ERROR
        self.status_text = response.reason or "Error response"
        self.body = None
        self.headers = response.headers  # type: ignore[assignment]
        self._raw_response = response

    async def aload_body(self) -> None:
        self.body = self._raw_response.content


class NiquestsClient(AsyncClient):
    def __init__(
        self,
        base_url: str,
        session: AsyncSession,
        transformers: Sequence[RequestTransformer | ResponseTransformer] = (),
    ) -> None:
        super().__init__(
            transformers=transformers,
        )
        self._base_url = base_url
        self._session = session

    @asynccontextmanager
    async def asend_request(
        self,
        request: HttpRequest,
    ) -> AsyncIterator[AsyncResponseWrapper]:
        params = [(k, v) for k, v in request.query_params if v is not None]
        try:
            resp = await self._session.request(
                method=request.method,
                url=urllib.parse.urljoin(self._base_url, request.url),
                headers=dict(request.headers),  # type: ignore[arg-type]
                data=request.body,
                params=params,
                files=[
                    (name, (data.filename or "new_file.txt", data.contents or b"", data.content_type or "text/plain"))
                    for name, data in request.files
                ],
            )
        except ReadTimeout as err:
            raise TimeoutError from err
        yield NiquestsResponseWrapper(resp)


@asynccontextmanager
async def http_session_maker(settings: AppSettings) -> AsyncGenerator[AsyncSession, None]:
    params: dict[str, Any] = {
        "retries": settings.http_retries,
        "pool_connections": settings.http_pool_size,
        "timeout": settings.http_timeout,
    }
    if settings.http_use_only_http_1:
        params.update({"disable_http2": True, "disable_http3": True})
    async with AsyncSession(**params) as session:
        session.verify = settings.http_verify_request
        yield session
