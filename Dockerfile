FROM python:3.6-alpine

COPY . /app

WORKDIR /app

RUN pip3 install -r requirements.txt

ENV PRODUCTION=True
ENV FLASK_APP=app.py
ENV FLASK_ENV=production
ENV HOST=0.0.0.0
ENV PORT=9080

CMD gunicorn --bind $HOST:$PORT app:app