#!/bin/bash

cdb_dir=$1


if [ -z $cdb_dir ]; then
	echo "Usage: $0 cdb_dir"
	exit 1;
fi

if [ ! -d ./tailf ]; then
	echo "tailf directory needs to be copied from sbc here"
	exit 1;
fi

if [ ! -d $cdb_dir ]; then
	echo "cdb directory with files are missing needs to be copied from sbc here"
	exit 3;
fi

if ! ls $cdb_dir/*.cdb >& /dev/null; then
	echo "cdb files are missing"
	exit 4;
fi

docker rm `docker ps -a -q`
docker build -t confd .
docker run -v /home/prasanth/examples/docker-confd/cdb:/opt/sonus/sbx/tailf/var/confd/cdb/ confd 
