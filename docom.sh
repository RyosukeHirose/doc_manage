#!/bin/sh

# MySQL 用はパスワードのみ指定する場合
# こちらを使う場合はsettings.py で外部ファイルから DB 設定を読み込むようにすること
MYSQL_PW=password docker-compose $1 $2 $3 $4 $5 $6 $7 $8 $9