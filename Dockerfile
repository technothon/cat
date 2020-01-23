FROM ubuntu:18.04
MAINTAINER pramachandran

RUN apt-get update && apt-get install -y authbind && apt-get clean && rm -rf /var/lib/apt/lists/*
#ENV APACHE_RUN_USER  www-data
#ENV APACHE_RUN_GROUP www-data
#ENV APACHE_LOG_DIR   /var/log/apache2
#ENV APACHE_PID_FILE  /var/run/apache2/apache2.pid
#ENV APACHE_RUN_DIR   /var/run/apache2
#ENV APACHE_LOCK_DIR  /var/lock/apache2
#ENV APACHE_LOG_DIR   /var/log/apache2
#EXPOSE 80

#RUN apt-get install -y authbind 
ENV APP_INSTALL_DIR_BASE /opt/sonus/sbx
 
RUN mkdir -p /opt/sonus/sbx/tailf
RUN mkdir -p /opt/sonus/sbx/fxs
#RUN mkdir -p /root/cdb/
RUN rm -f /opt/sonus/sbx/tailf/var/confd/cdb/*.xml
COPY tailf /opt/sonus/sbx/tailf
COPY fxs /opt/sonus/sbx/fxs/
COPY files/scripts/dumper.sh /root
COPY files/libs/* /usr/lib/x86_64-linux-gnu/
COPY user-storage-trans-app /root
RUN sed -i 's/10.0.1.20/127.0.0.1/g' /opt/sonus/sbx/tailf/confd.conf
RUN sed -i '/confdIpcExtraListenIp/d' /opt/sonus/sbx/tailf/confd.conf
RUN sed -i '/extraIpPorts/d' /opt/sonus/sbx/tailf/confd.conf


#CMD [ "/bin/bash", "-c" , "/root/dumper.sh > /opt/sonus/sbx/tailf/var/confd/cdb/d.txt" ]

ENTRYPOINT "/root/dumper.sh" && /bin/bash
