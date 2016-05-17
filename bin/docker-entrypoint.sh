#!/bin/sh
echo Run startup script
/usr/bin/supervisord
sleep 10
python /root/boot.py
start /root/kafka.py
consul watch -type keyprefix -prefix / /bin/kv_handler.sh
