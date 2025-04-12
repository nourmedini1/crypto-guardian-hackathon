FROM python:3.12.7-slim

WORKDIR /app

COPY src/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY /src .

EXPOSE 5020

CMD ["python", "main.py"]
