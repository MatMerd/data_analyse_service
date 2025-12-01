FROM python:3.11

ENV UV_VERSION=0.8.17 \
    UV_LINK_MODE=copy \
    UV_COMPILE_BYTECODE=1 \
    UV_PYTHON_DOWNLOADS=never \
    UV_PROJECT_ENVIRONMENT=/opt/venv


WORKDIR /app

RUN pip3 install uv==$UV_VERSION && \
    python3 -m venv /venv

COPY pyproject.toml uv.lock ./

RUN uv venv --relocatable
RUN uv sync --no-dev

ENV PATH="/opt/venv/bin:$PATH"

COPY data_analyse_project/ data_analyse_project/
COPY docker-entrypoint/ /docker-entrypoint/


ENTRYPOINT ["/docker-entrypoint/entrypoint" ]
