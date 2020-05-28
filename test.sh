#!/bin/sh

count=0
while :
do
  if $count < 5; then
    break
  else
    count=$count+1
    sleep 1
    echo count
  fi
done

exit 0
