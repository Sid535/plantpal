FROM python:3.12-slim

WORKDIR /app

# Install uv
RUN pip install uv

COPY . .

# Install dependencies from your existing pyproject.toml
RUN uv sync

EXPOSE 7860

CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]