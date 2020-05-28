FROM python:3.7

# 作業ディレクトリを設定  
WORKDIR /code/

ADD requirements.txt /code  

RUN apt-get update \
&& pip install --upgrade pip \
&& pip install -r requirements.txt \
# mysqlに利用
&& apt-get install -y python3-dev default-libmysqlclient-dev \

# PDFからのテキスト抽出ライブラリ
&& pip install pdfminer.six \
# mecab
&& apt-get -y install mecab \
&& apt-get -y install libmecab-dev \
&& apt-get -y install mecab-ipadic-utf8 \
&& pip3 install mecab-python3 \
# 機会学習ライブラリ
&& pip install scikit-learn \

# ここから、wkhtmltopdf のインストール
&& apt-get install -y \
      build-essential \
      xorg \
      libssl-dev \
      libxrender-dev \
      wget \
      unzip \
      gdebi \
 && apt-get autoremove \
 && apt-get clean

ENV WKHTMLTOPDF_VERSION 0.12.4
RUN wget https://github.com/wkhtmltopdf/wkhtmltopdf/releases/download/${WKHTMLTOPDF_VERSION}/wkhtmltox-${WKHTMLTOPDF_VERSION}_linux-generic-amd64.tar.xz
RUN tar vxfJ wkhtmltox-${WKHTMLTOPDF_VERSION}_linux-generic-amd64.tar.xz \
 && ln -s /opt/wkhtmltox/bin/wkhtmltopdf /usr/bin/wkhtmltopdf

# 日本語フォントとして Noto Fonts をインストールする。
RUN wget https://noto-website.storage.googleapis.com/pkgs/Noto-unhinted.zip \
 && unzip -d NotoSansJapanese Noto-unhinted.zip \
 && mkdir -p /usr/share/fonts/opentype \
 && mv -fv ./NotoSansJapanese /usr/share/fonts/opentype/NotoSansJapanese \
 && rm -rfv Noto-unhinted.zip \
 && fc-cache -fv


# mkdir doc_manage_pro
# cd bells_pro
# django-admin startproject config .
# python manage.py startapp doc_manage
# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser

# python manage.py runserver 0:8000
