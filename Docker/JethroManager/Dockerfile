# Jethro Manager over Docker
 
# based on centos(7):latest image
FROM centos:7

# Build-time parameters
ARG JETHROMNG_RPM_LOACTION

USER root

WORKDIR /jethro_install

COPY dockerBootstrap /jethro_install

# install systemd
RUN yum -y update; yum clean all
RUN yum -y install systemd initscripts

# install java
RUN yum -y install java-1.8.0-openjdk-devel.x86_64
ENV JAVA_HOME /usr/lib/jvm/jre

# install ssh
RUN yum -y install openssh openssh-server openssl openssh-clients

# Install Jethro Manager
ADD $JETHROMNG_RPM_LOACTION /jethro_install
RUN rpm -i /jethro_install/$(basename $JETHROMNG_RPM_LOACTION)

# configure volumes
RUN mkdir /jethro -m 777
RUN mkdir /jethro/persist -m 777
RUN (test -d /var/log/jethro || mkdir /var/log/jethro) && (chmod 777 /var/log/jethro)
VOLUME ["/jethro/persist", "/var/log/jethro"]

# start all services
RUN chmod a+x /jethro_install/dockerBootstrap
ENTRYPOINT ["sh", "-c", "/jethro_install/dockerBootstrap"]

# expose needed port numbers
EXPOSE 9100-9200 80 443 22