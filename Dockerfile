FROM python:3.12-slim

# 作業ディレクトリ
WORKDIR /app

# 依存関係
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーション本体
COPY . .

# FastAPI起動
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
