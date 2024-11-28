FROM python:3.12

RUN pip install uv

WORKDIR /src

RUN python -m venv venv
RUN . /src/venv/bin/activate

ADD pyproject.toml ./

RUN uv sync
 
ENV VIRTUAL_ENV=.venv \
    PATH="/.venv/bin:$PATH"
 
COPY /* ./

EXPOSE 80

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--log-level", "debug"]