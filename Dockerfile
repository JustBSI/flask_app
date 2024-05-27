FROM python:3.12.3

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

WORKDIR /app/src

CMD uwsgi --ini ../uwsgi.ini