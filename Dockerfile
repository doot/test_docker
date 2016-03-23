FROM python:3.4

ENV PYTHONUNBUFFERED 1

ADD . /app/src

WORKDIR /app/src

RUN pip install -r /app/requirements.txt

CMD gunicorn app:app -b 0.0.0.0:8000
