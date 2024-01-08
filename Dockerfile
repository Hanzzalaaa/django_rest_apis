FROM python:3.10-slim-buster

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 9000


CMD python manage.py runserver 0.0.0.0:9000