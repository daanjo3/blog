# syntax=docker/dockerfile:1
FROM python:3.12-alpine

WORKDIR /app

# Not sure if needed
RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY generator/ generator/
COPY posts/ posts/
COPY public/ public/
COPY templates/ templates/

COPY dev.py .

ENTRYPOINT ["python", "dev.py"]