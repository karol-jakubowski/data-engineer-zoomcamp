FROM python:3.13.11-slim
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /code

# 1. Poprawiona ścieżka do środowiska (z /app na /code)
ENV PATH="/code/.venv/bin:$PATH"

COPY "pyproject.toml" "uv.lock" ".python-version" ./

# 2. Dodana flaga ignorująca brak folderu src/
RUN uv sync --locked --no-install-project

COPY 01_docker_terraform/pipeline/pipeline.py .

ENTRYPOINT ["python", "pipeline.py"]