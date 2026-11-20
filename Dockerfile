# installing python + uv
FROM python:3.14.4-slim-bookworm
COPY --from=docker.io/astral/uv:latest /uv /uvx /bin/


WORKDIR /usr/src/fastapi_course_app

COPY requirements.txt .

# init & run via uv
RUN uv init && uv add -r requirements.txt

# copy all contents after installing deps
COPY . .

CMD ["uv", "run", "fastapi", "dev"]
