#!/bin/bash

cp -f /root/cdb/*.cdb /opt/sonus/sbx/tailf/var/confd/cdb/
/opt/sonus/sbx/tailf/bin/confd --cdb-debug-dump /opt/sonus/sbx/tailf/var/confd/cdb/ > /root/cdb/cdb-debug-dump.txt
