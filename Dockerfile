FROM python:3.11
WORKDIR /bot

# 必要なパッケージをインストール
COPY requirements.txt /bot/
RUN pip install -r requirements.txt

# ボットのコードをコピー
COPY . /bot
COPY ./fonts /app/fonts
# main.py と DesignersCafe.py を並行して実行
CMD ["sh", "-c", "python main.py & python DesignersCafe.py"]