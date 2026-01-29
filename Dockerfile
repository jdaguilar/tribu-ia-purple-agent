FROM ghcr.io/astral-sh/uv:python3.13-bookworm

ENV UV_HTTP_TIMEOUT=300

RUN adduser agentbeats
USER agentbeats
RUN mkdir -p /home/agentbeats/.cache/uv
WORKDIR /home/agentbeats/tutorial

COPY pyproject.toml uv.lock README.md ./
COPY src src

RUN \
    --mount=type=cache,target=/home/agentbeats/.cache/uv,uid=1000 \
    uv sync --locked --no-dev --no-install-project

ENTRYPOINT ["uv", "run", "src/server.py"]
CMD ["--host", "0.0.0.0"]
EXPOSE 9019
