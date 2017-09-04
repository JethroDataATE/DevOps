# Jethro over Docker (for HDP distribution) 

# based on centos(7):latest image
FROM centos:7

# Build-time parameters
ARG JETHRO_RPM_LOACTION
ARG JAVA_VERSION=java-java-1.8.0-openjdk.x86_64
ARG HADOOP_DIST_VERSION=2.4.2

USER root

WORKDIR /jethro_install

COPY Common/dockerBootstrap /jethro_install

# install systemd
RUN yum -y update; yum clean all
RUN yum -y install systemd initscripts

# install java
RUN yum -y install $JAVA_VERSION
ENV JAVA_HOME /usr/lib/jvm/jre

# install ssh
RUN yum -y install openssh openssh-server openssl openssh-clients

# install hadoop (HDP)
ADD http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/$HADOOP_DIST_VERSION.0/hdp.repo /jethro_install
RUN cp /jethro_install/hdp.repo /etc/yum.repos.d/hdp.repo
RUN yum -y install hadoop-client

# hadoop distributed
ENV HADOOP_PREFIX /etc/hadoop
ENV HADDOP_NAME_NODE_ADDRESS localhost:8080
ENV HADOOP_CONF_DIR $HADOOP_PREFIX/conf
COPY Common/core-site.xml.template $HADOOP_CONF_DIR/core-site.xml.template

# install hive
RUN yum -y install hive

# install Jethro
ADD $JETHRO_RPM_LOACTION /jethro_install
RUN rpm -i /jethro_install/$(basename $JETHRO_RPM_LOACTION)

# configure volumes
RUN mkdir /jethro -m 777
RUN mkdir /jethro/persist -m 777
RUN mkdir /jethro/instance_storage -m 777
RUN (test -d /opt/jethro/instances || mkdir /opt/jethro/instances) && (chmod 777 /opt/jethro/instances)
RUN (test -d /opt/jethro/current/instances || mkdir /opt/jethro/current/instances) && (chmod 777 /opt/jethro/current/instances)
RUN (test -d /var/log/jethro || mkdir /var/log/jethro) && (chmod 777 /var/log/jethro)
VOLUME ["/jethro/persist", "/opt/jethro/instances", "/var/log/jethro", "/jethro/instance_storage"]

# Auto attach instance parameters
ENV AUTO_ATTACH_INSTANCE_NAME ""
ENV AUTO_ATTACH_INSTANCE_PATH "" 

# start container
ENTRYPOINT ["sh", "-c", "/jethro_install/dockerBootstrap"]

# expose needed port numbers
EXPOSE 9100-9200 22