FROM httpd

RUN set -ex && \
    apt update && \
    apt install -y vim && \
    apt install -y nano && \
    apt install -y less && \
    apt install -y tree && \
    cp /usr/share/zoneinfo/Japan /etc/localtime && \
    sed -i '/#ServerName/a ServerName www.matchaism.net:80' /usr/local/apache2/conf/httpd.conf'
