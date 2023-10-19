# ベースイメージとして公式Pythonイメージを使用
FROM python:3.9-slim-buster

# 作業ディレクトリを設定
WORKDIR /usr/src/app

# 依存関係のインストール
COPY ./endpoint/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# アプリケーションのコードをコピー
COPY ./endpoint/ .

# ポートを開放
EXPOSE 8000

ENV PYTHONPATH="${PYTHONPATH}:."

# コマンド実行
# CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
CMD ["/bin/bash"]
