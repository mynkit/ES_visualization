FROM python:3.6

# Set timezone to JST
ENV TZ Asia/Tokyo

# Set Language
ENV LANG C.UTF-8

# workdirの指定
WORKDIR /app

COPY requirements.txt ./
# インストール
RUN apt-get update \
  && apt-get install graphviz -y \
  && pip install -r requirements.txt

# fontの移動
COPY src/data/fonts/ /usr/share/fonts/truetype/

CMD ["uwsgi","--ini","/app/uwsgi.ini"]