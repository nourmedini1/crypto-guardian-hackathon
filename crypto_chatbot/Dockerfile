FROM python:3.12.7-slim

ENV TRANSFORMERS_CACHE="/models"
ENV PIP_REQUIRE_HASHES=0

WORKDIR /app

RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

COPY src/requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

RUN python -c "from transformers import AutoModel; AutoModel.from_pretrained('BAAI/bge-m3')"

COPY /src .

EXPOSE 5010

CMD ["python", "main.py"]
