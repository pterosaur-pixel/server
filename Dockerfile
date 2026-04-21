FROM python:slim-bookworm

WORKDIR /app

COPY server.py /app
RUN apt update

CMD [ "python3", "server.py" ]
