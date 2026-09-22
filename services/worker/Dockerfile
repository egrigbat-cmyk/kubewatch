FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
RUN useradd -m timmy
COPY --chown=<timmy>:timmy> . .
USER timmy
CMD ["celery", "-A", "worker.celery_app", "worker", "--loglevel=info"]
