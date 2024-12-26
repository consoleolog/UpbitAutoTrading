FROM python:3.9-slim

WORKDIR /app

RUN apt-get update && apt-get install -y tzdata

RUN pip install --upgrade pip

COPY ./requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY ./ ./

EXPOSE 8000

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8000"]