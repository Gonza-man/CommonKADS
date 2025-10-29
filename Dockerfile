# Dockerfile from the uv docs: https://github.com/astral-sh/uv-docker-example/blob/main/Dockerfile

# First, build the application in the `/app` directory
FROM ghcr.io/astral-sh/uv:bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Configure the Python directory so it is consistent
ENV UV_PYTHON_INSTALL_DIR=/python

# Only use the managed Python version
ENV UV_PYTHON_PREFERENCE=only-managed

# Install Python before the project for caching
RUN uv python install 3.8

WORKDIR /app
RUN --mount=type=cache,target=/root/.cache/uv \
  --mount=type=bind,source=uv.lock,target=uv.lock \
  --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
  uv sync --locked --no-install-project --no-dev
COPY . /app
RUN --mount=type=cache,target=/root/.cache/uv \
  uv sync --locked --no-dev

# Then, use a final image without uv
FROM debian:bookworm-slim

# Copy the Python version
COPY --from=builder --chown=python:python /python /python

# Copy the application from the builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Setup non-root user (as before)
RUN groupadd --system --gid 999 nonroot \
  && useradd --system --gid 999 --uid 999 --create-home nonroot


# Use the non-root user to run our application
USER nonroot


# Use `/app` as the working directory
WORKDIR /app


# Run the application using a production WSGI server (Gunicorn)
#
# IMPORTANT:
# 1. 'gunicorn' MUST be included as a production dependency in your
#    pyproject.toml / uv.lock file.
#
# 2. 'main:app' assumes your Flask app instance is named 'app'
#    inside a file named 'main.py'. Adjust this to match your app's structure
#    (e.g., 'my_app.server:create_app()').
#
# 3. The --workers flag is set to 4 as a sensible default. For optimal
#    performance, this is often set to (2 * $num_cores) + 1. You can
#    override this at runtime, e.g.,
#    `docker run -e GUNICORN_WORKERS=8 ...` and modify the CMD to use an
#    entrypoint script that respects $GUNICORN_WORKERS.
#    For simplicity, we use a static `CMD` here.
CMD ["gunicorn", "--workers", "4", "--bind", "0.0.0.0:8000", "app:app"]
