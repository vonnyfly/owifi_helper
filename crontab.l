ORACLE_WEIXIN=/home/`id -un`/oracle_weixin
06 6 * * 1-5 bash $ORACLE_WEIXIN/oracle_wifi.sh
05 3,9,17 * * * bash $ORACLE_WEIXIN/upload_wifi.sh
5 9-17 * * * python $ORACLE_WEIXIN/gen-bug-stats.py -o "/scratch/`id -un`/bugs.html"
5 9-17 * * * python $ORACLE_WEIXIN/gen-bug-stats.py -r "12.0" -o "/scratch/`id -un`/s12_bugs.html"
