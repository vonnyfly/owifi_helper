#!/bin/bash

BASE_DIR=~/oracle_weixin
source $BASE_DIR/upload_wifi.sh

if [ `echo $content | grep Password | wc -l` -gt 0 ];then
  cat $file | /usr/sbin/sendmail -t -F "God" -r "li.feng@oracle.com"
fi
