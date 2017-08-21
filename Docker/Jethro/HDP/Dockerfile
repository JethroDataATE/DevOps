# Jethro over Docker

# based on centos(7):latest image
FROM centos:7

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

# install hadoop (HDP)
ADD http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/2.4.2.0/hdp.repo /jethro_install
RUN cp /jethro_install/hdp.repo /etc/yum.repos.d/hdp.repo
RUN yum -y install hadoop-client


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
ADD http://jethrodownload.s3.amazonaws.com/RC/3.0.0/3.0.3/jethro-3.0.3-15840.x86_64.rpm /jethro_install
RUN rpm -U jethro-3.0.3-15840.x86_64.rpm

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