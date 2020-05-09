FROM python:3.7

# 作業ディレクトリを設定  
WORKDIR /usr/src/app  

ADD requirements.txt /usr/src/app  

# Pipenvをインストール  
RUN apt-get update \
&& pip install --upgrade pip \
&& pip install -r requirements.txt \
# PDFからのテキスト抽出ライブラリ
&& pip install pdfminer.six \
# mecab
&& apt install mecab \
&& apt install libmecab-dev \
&& apt install mecab-ipadic-utf8 \
&& pip3 install mecab-python3 \
# 機会学習ライブラリ
&& pip install scikit-learn


# mkdir bells_pro
# django-admin startproject config .
# python manage.py startapp bells
# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser

# python manage.py runserver 0:8000
