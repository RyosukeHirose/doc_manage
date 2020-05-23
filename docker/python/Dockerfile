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
&& pip install scikit-learn

# mkdir doc_manage_pro
# cd bells_pro
# django-admin startproject config .
# python manage.py startapp doc_manage
# python manage.py makemigrations
# python manage.py migrate
# python manage.py createsuperuser

# python manage.py runserver 0:8000
