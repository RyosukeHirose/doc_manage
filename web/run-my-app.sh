#!/bin/sh

app=doc_manage_pro
while :
do
  if python /code/$app/manage.py migrate; then
    break
  else
    sleep 1
  fi
done
uwsgi --ini /code/$app/config/uwsgi.ini

exit 0