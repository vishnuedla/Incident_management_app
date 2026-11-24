FROM python:3.12-slim

WORKDIR /app

COPY requirement.txt .

RUN pip install --no-cache-dir -r requirement.txt

COPY . .

RUN groupadd -r appuser && useradd -r -g appuser app  && chown -R  app:appuser /app/* && chown -R app:appuser /app && chmod 700 /app

EXPOSE 8001

USER app

CMD ["python","app.py","&"]

