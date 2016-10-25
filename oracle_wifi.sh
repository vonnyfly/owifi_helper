#!/bin/bash

#BASE_DIR=~/oracle_weixin
BASE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/$(basename "${BASH_SOURCE[0]}")"
source $BASE_DIR/upload_wifi.sh

if [ `echo $content | grep Password | wc -l` -gt 0 ];then
  cat $file | /usr/sbin/sendmail -t -F "God" -r "li.feng@oracle.com"
fi
