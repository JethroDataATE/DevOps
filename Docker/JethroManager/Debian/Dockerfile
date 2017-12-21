# Jethro Manager over Docker

# based on centos(7):latest image
FROM ubuntu:14.04

USER root

WORKDIR /jethro_workdir

COPY Debian/rpm2deb.sh /jethro_workdir
RUN chmod a+x /jethro_workdir/rpm2deb.sh

COPY Debian/dockerBootstrap /jethro_workdir
RUN chmod a+x /jethro_workdir/dockerBootstrap

# install alien
RUN sudo apt-get -y update
RUN sudo apt-get -y install alien

# install wget
RUN sudo apt-get install wget

ENV RPM_URL=""

# create mount point
RUN mkdir /jethro_volume -m 777
VOLUME ["/jethro_volume"]

# start all services
ENTRYPOINT ["sh", "/jethro_workdir/dockerBootstrap"]