#!/bin/sh

function notifyme
{
  tmp=/tmp/myerr.log
  cat >$tmp <<EOF
To:lifeng1519@gmail.com
Subject:[ERROR] Pls Check WI-FI Password
EOF
  cat $tmp | /usr/sbin/sendmail -t -F "God" -r "lifeng1519@oracle.com"
}

BASE_DIR=$HOME/oracle_weixin
# usging newfox
#To:sps_BJ_DEV_CN_GRP@oracle.com
content=`python $BASE_DIR/get_wifi.py 2>/dev/null`
file=/tmp/mypasswd.log
#To:hcts_auto_notify_cn_grp@oracle.com
to=`curl -s http://on12.us.oracle.com/expn\?q\=hcts_auto_notify_cn_grp%40oracle.com | grep -v ' ' | grep "@oracle.com" | sed 's/<.*>//g' | grep -v '<' | sed '/^$/d' | perl -p -e 's/\n/,/'`
cat >$file <<EOF
Bcc:${to}
Subject:WiFi guest

$content

EOF

#http://stackoverflow.com/questions/3044315/how-to-set-the-authorization-header-using-curl
if [ `echo $content | grep Password | wc -l` -gt 0 ];then
  curl --user guest:guest  -x http://10.188.60.183:80 -F filedata=@${file}  http://l.abest.me/upload.php
else
  notifyme
fi
