# Jethro over Docker POC 
#
# docker build -t jethrodata/poc .

# based on centos(7):latest image
FROM centos:7

# Build-time parameters
ARG JETHRO_RPM_LOACTION
ARG JETHRO_RPM_NAME

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

# install hadoop:
RUN rpm --quiet --import http://archive.cloudera.com/cdh5/redhat/6/x86_64/cdh/RPM-GPG-KEY-cloudera
ADD http://archive.cloudera.com/cdh5/one-click-install/redhat/6/x86_64/cloudera-cdh-5-0.x86_64.rpm /jethro_install
RUN yum -y localinstall cloudera-cdh-5-0.x86_64.rpm

ENV HADOOP_PREFIX /etc/hadoop
ENV HADDOP_NAME_NODE_ADDRESS localhost:8080
ENV HADOOP_COMMON_PATH /bin
ENV HADOOP_HDFS_HOME /bin
ENV HADOOP_MAPRED_HOME /bin
ENV HADOOP_YARN_HOME /bin
ENV HADOOP_CONF_DIR $HADOOP_PREFIX/conf

# hadoop distributed
ADD core-site.xml.template $HADOOP_CONF_DIR/core-site.xml.template
ADD hdfs-site.xml $HADOOP_CONF_DIR/hdfs-site.xml
ADD mapred-site.xml $HADOOP_CONF_DIR/mapred-site.xml
ADD yarn-site.xml $HADOOP_CONF_DIR/yarn-site.xml

# install hive
RUN yum -y install hive hive-jdbc

# install Jethro
ADD $JETHRO_RPM_LOACTION /jethro_install
RUN rpm -i $JETHRO_RPM_NAME

# configure volumes
RUN mkdir /jethro -m 777
RUN mkdir /jethro/persist -m 777
RUN (test -d /opt/jethro/instances || mkdir /opt/jethro/instances) && (chmod 777 /opt/jethro/instances)
RUN (test -d /opt/jethro/current/instances || mkdir /opt/jethro/current/instances) && (chmod 777 /opt/jethro/current/instances)
RUN (test -d /var/log/jethro || mkdir /var/log/jethro) && (chmod 777 /var/log/jethro)
VOLUME ["/jethro/persist", "/opt/jethro/instances", "/var/log/jethro"]


# start all services
ENTRYPOINT ["sh", "-c", "/jethro_install/dockerBootstrap"]

# expose needed port numbers
EXPOSE 9100-9200 80 443 22