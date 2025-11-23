FROM python:3.13-slim
WORKDIR /usr/local/app
RUN pip install uv
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen
ENTRYPOINT ["uv", "run"]
