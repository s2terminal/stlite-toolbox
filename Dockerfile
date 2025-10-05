FROM mcr.microsoft.com/devcontainers/typescript-node:1-22-bookworm

# Install uv
COPY --from=ghcr.io/astral-sh/uv:0.8.18 /uv /uvx /bin/
