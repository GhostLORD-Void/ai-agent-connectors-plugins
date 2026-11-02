FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /app
RUN useradd --create-home --uid 10001 appuser
COPY src/ ./src/
COPY catalog/ ./catalog/
COPY docs/ ./docs/
USER appuser
CMD ["python", "src/mcp_server.py"]
