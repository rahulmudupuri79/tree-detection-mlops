FROM python:3.14-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    MODEL_PATH=/models/best.pt     INFERENCE_DEVICE=cpu

WORKDIR /app

COPY requirements.txt ./requirements.txt
RUN python -m pip install --upgrade pip \
    && python -m pip install -r requirements.txt

COPY src ./src

RUN useradd --create-home --uid 10001 appuser \
    && mkdir -p /models \
    && chown -R appuser:appuser /app /models

USER 10001:10001

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=60s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health/live', timeout=2)" || exit 1

CMD ["python", "-m", "uvicorn", "src.inference_api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1"]
