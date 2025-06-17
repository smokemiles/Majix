FROM python:3.9-slim-buster

WORKDIR /app

COPY . .

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 5001

ENV FLASK_APP=main.py
ENV FLASK_ENV=production

CMD ["flask", "run", "--host=0.0.0.0"]

# This Dockerfile sets up a Python Flask application in a Docker container.