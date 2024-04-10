FROM python:3.9-alpine

ENV PYTHONBUFFERED=1

WORKDIR /referralAPI

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD python manage.py runserver 0:0:0:0:8000