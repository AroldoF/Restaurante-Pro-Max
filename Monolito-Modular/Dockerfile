FROM python:3.12-slim

# uv
RUN pip install uv

WORKDIR /app

# dependências python (cache)
COPY pyproject.toml uv.lock /app/

RUN uv sync --no-editable

# projeto
COPY . /app/

EXPOSE 8000

CMD ["uv", "run", "fastapi", "run", "main.py", "--host", "0.0.0.0", "--port", "8000"]