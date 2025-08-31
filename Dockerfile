FROM python:3.13-alpine

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY .env /app/

COPY /app /app/

EXPOSE 8000

CMD [ "fastapi", "run", "main.py" ]