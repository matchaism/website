FROM httpd

RUN apt update
RUN apt install -y vim
RUN apt install -y nano
RUN apt install -y less
RUN apt install -y tree

RUN cp /usr/share/zoneinfo/Japan /etc/localtime
