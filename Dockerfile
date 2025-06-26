FROM python:latest

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /url_shortener

COPY pyproject.toml .
RUN uv pip install -r pyproject.toml --system
COPY . .
RUN uv pip install -e . --system

CMD ["make", "test_run"]
