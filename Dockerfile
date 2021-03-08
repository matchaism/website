FROM httpd

COPY ./local/*.pem /usr/local/apache2/conf/

RUN set -ex && \
    apt update && \
    apt install -y vim && \
    apt install -y nano && \
    apt install -y less && \
    apt install -y tree && \
    cp /usr/share/zoneinfo/Japan /etc/localtime && \
    sed -i '/#ServerName/a ServerName www.matchaism.net:80' /usr/local/apache2/conf/httpd.conf

RUN sed -ie 's/^#\(Include .*httpd-ssl.conf\)/\1/' /usr/local/apache2/conf/httpd.conf
RUN sed -ie 's/^#\(LoadModule .*mod_ssl.so\)/\1/' /usr/local/apache2/conf/httpd.conf
RUN sed -ie 's/^#\(LoadModule .*mod_socache_shmcb.so\)/\1/' /usr/local/apache2/conf/httpd.conf

RUN sed -ri -e 's/server\.crt/fullchain\.pem/g' /usr/local/apache2/conf/extra/httpd-ssl.conf
RUN sed -ri -e 's/server\.key/privkey\.pem/g' /usr/local/apache2/conf/extra/httpd-ssl.conf

RUN sed -ri '!#SSLCertificateChainFile!a SSLCertificateChainFile "/usr/local/apache2/conf/chain.pem"' /usr/local/apache2/conf/extra/httpd-ssl.conf

