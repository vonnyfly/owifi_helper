06 6 * * 1-5 bash $HOME/oracle_weixin/oracle_wifi.sh
05 3,9,17 * * * bash $HOME/oracle_weixin/upload_wifi.sh
5 9-17 * * * python $HOME/oracle_weixin/gen-bug-stats.py -o "/scratch/`id -un`/bugs.html"
5 9-17 * * * python $HOME/oracle_weixin/gen-bug-stats.py -r "12.0" -o "/scratch/`id -un`/s12_bugs.html"
