#!/bin/bash

cp -f /root/cdb/*.cdb /opt/sonus/sbx/tailf/var/confd/cdb/
#/opt/sonus/sbx/tailf/bin/confd --cdb-debug-dump /opt/sonus/sbx/tailf/var/confd/cdb/ > /root/cdb/cdb-debug-dump.txt

/opt/sonus/sbx/tailf/bin/confd -c /opt/sonus/sbx/tailf/confd.conf --foreground 2>&1 > /dev/null &
sleep 5;
/root/user-storage-trans-app 2>&1 > /dev/null &
sleep 2;
echo "show configuration addressContext | nomore | display json" | /opt/sonus/sbx/tailf/bin/confd_cli -u admin > /root/cdb/cfg.json

