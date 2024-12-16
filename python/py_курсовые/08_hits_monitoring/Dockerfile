FROM ghcr.io/linuxserver/openssh-server

RUN apk update && \
    apk add python3-dev && \
    apk add python3 && \
    apk add py3-pip

RUN mkdir -p /opt/vmware/vcloud-director/logs && \
    mkdir -p /opt/app && \
    mkdir -p /var/lib/node_exporter

COPY data/*.request.log /opt/vmware/vcloud-director/logs
COPY config/crontab /etc/crontabs/root
COPY app/. /opt/app
RUN pip3 install --break-system-packages --no-cache-dir -r /opt/app/requirements.txt

