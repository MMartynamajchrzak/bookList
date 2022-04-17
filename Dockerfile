FROM python:3.10

COPY requirements.txt /requirements.txt

RUN pip install -r /requirements.txt

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x entrypoint.sh

WORKDIR /app
