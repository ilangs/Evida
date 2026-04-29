FROM python:3.11-slim

WORKDIR /app

# 시스템 의존성 설치 (필요시)
RUN apt-get update && apt-get install -y gcc libpq-dev && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Vercel/Railway 등 서버리스 및 컨테이너 환경 대응
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
