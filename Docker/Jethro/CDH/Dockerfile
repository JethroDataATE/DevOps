# Jethro over Docker (for Cloudera HADOOP distribution) 

# based on centos(7):latest image
FROM centos:7

# Build-time parameters
ARG JETHRO_RPM_LOACTION
ARG JAVA_VERSION=java-1.8.0-openjdk-devel.x86_64
ARG CDH_VERSION=5
# ENV CDH_SRC "http://archive.cloudera.com/cdh$CDH_VERSION/redhat/6/x86_64/cdh/RPM-GPG-KEY-cloudera"
# ENV CDH_RPM "http://archive.cloudera.com/cdh$CDH_VERSION/one-click-install/redhat/6/x86_64/cloudera-cdh-$CDH_VERSION-0.x86_64.rpm"

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

# install hadoop:
RUN rpm --quiet --import http://archive.cloudera.com/cdh$CDH_VERSION/redhat/6/x86_64/cdh/RPM-GPG-KEY-cloudera
# RUN rpm --quiet --import $CDH_SRC
# RUN rpm --quiet --import http://archive.cloudera.com/cdh5/redhat/6/x86_64/cdh/RPM-GPG-KEY-cloudera
ADD http://archive.cloudera.com/cdh$CDH_VERSION/one-click-install/redhat/6/x86_64/cloudera-cdh-$CDH_VERSION-0.x86_64.rpm /jethro_install
# ADD $CDH_RPM /jethro_install
# ADD http://archive.cloudera.com/cdh5/one-click-install/redhat/6/x86_64/cloudera-cdh-5-0.x86_64.rpm /jethro_install
# RUN yum -y localinstall cloudera-cdh-5-0.x86_64.rpm
RUN yum -y localinstall cloudera-cdh-$CDH_VERSION-0.x86_64.rpm

# hadoop distributed
ENV HADOOP_PREFIX /etc/hadoop
ENV HADDOP_NAME_NODE_ADDRESS localhost:8080
ENV HADOOP_CONF_DIR $HADOOP_PREFIX/conf
COPY Common/core-site.xml.template $HADOOP_CONF_DIR/core-site.xml.template

# install hive
RUN yum -y install hive-jdbc

# install Jethro
ADD $JETHRO_RPM_LOACTION /jethro_install
RUN rpm -i /jethro_install/$(basename $JETHRO_RPM_LOACTION)

# configure volumes
RUN mkdir /jethro -m 777
RUN mkdir /jethro/persist -m 777
RUN (test -d /opt/jethro/instances || mkdir /opt/jethro/instances) && (chmod 777 /opt/jethro/instances)
RUN (test -d /opt/jethro/current/instances || mkdir /opt/jethro/current/instances) && (chmod 777 /opt/jethro/current/instances)
RUN (test -d /var/log/jethro || mkdir /var/log/jethro) && (chmod 777 /var/log/jethro)
VOLUME ["/jethro/persist", "/opt/jethro/instances", "/var/log/jethro"]


# start container
ENTRYPOINT ["sh", "-c", "/jethro_install/dockerBootstrap"]

# expose needed port numbers
EXPOSE 9100-9200 22