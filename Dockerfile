FROM httpd

COPY ./local/*.pem /usr/local/apache2/conf/

RUN set -ex && \
    apt update && \
    apt install -y vim && \
    apt install -y nano && \
    apt install -y less && \
    apt install -y tree && \
    cp /usr/share/zoneinfo/Japan /etc/localtime && \
    sed -i '/#ServerName/a ServerName www.matchaism.net:80' /usr/local/apache2/conf/httpd.conf && \
    sed -ie 's/^#\(Include .*httpd-ssl.conf\)/\1/' /usr/local/apache2/conf/httpd.conf && \
    sed -ie 's/^#\(LoadModule .*mod_ssl.so\)/\1/' /usr/local/apache2/conf/httpd.conf && \
    sed -ie 's/^#\(LoadModule .*mod_socache_shmcb.so\)/\1/' /usr/local/apache2/conf/httpd.conf && \
    sed -ri -e 's/server\.crt/fullchain\.pem/g' /usr/local/apache2/conf/extra/httpd-ssl.conf && \
    sed -ri -e 's/server\.key/privkey\.pem/g' /usr/local/apache2/conf/extra/httpd-ssl.conf && \
    sed -ie 's/^#SSLCertificateChainFile/SSLCertificateChainFile/1' /usr/local/apache2/conf/extra/httpd-ssl.conf && \
    sed -ri -e 's/server-ca\.crt/chain\.pem/g' /usr/local/apache2/conf/extra/httpd-ssl.conf && \
    sed -ri -e 's/www\.example\.com/matchaism\.net/g' /usr/local/apache2/conf/extra/httpd-ssl.conf
