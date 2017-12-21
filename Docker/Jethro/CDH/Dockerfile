# Jethro over Docker (for Cloudera HADOOP distribution) 

# based on jethrodata/jethro:HADOOP_BASE image
FROM jethrodata/jethro:HADOOP_BASE

# Build-time parameters
ARG JETHRO_RPM_LOACTION=http://jethro.io/latest-rpm
ARG JETHROMNG_RPM_LOACTION=http://jethro.io/latest-jethro-manager
ARG JAVA_VERSION=java-1.8.0-openjdk.x86_64
ARG HADOOP_DIST_VERSION=5

# install java
RUN yum -y install $JAVA_VERSION
ENV JAVA_HOME /usr/lib/jvm/jre

# install hadoop:
RUN rpm --quiet --import http://archive.cloudera.com/cdh$HADOOP_DIST_VERSION/redhat/6/x86_64/cdh/RPM-GPG-KEY-cloudera
ADD http://archive.cloudera.com/cdh$HADOOP_DIST_VERSION/one-click-install/redhat/6/x86_64/cloudera-cdh-$HADOOP_DIST_VERSION-0.x86_64.rpm /jethro_install
RUN yum -y localinstall cloudera-cdh-$HADOOP_DIST_VERSION-0.x86_64.rpm

# install hive
RUN yum -y install hive

# install impala-shell
#RUN yum -y install impala-shell

# install Jethro
ADD $JETHRO_RPM_LOACTION /jethro_install
RUN rpm -i /jethro_install/$(basename $JETHRO_RPM_LOACTION)

# Install Jethro Manager is asked
RUN if [ ! -z $JETHROMNG_RPM_LOACTION ]; then wget $JETHROMNG_RPM_LOACTION && rpm -i $(basename $JETHROMNG_RPM_LOACTION) && rm -f $(basename $JETHROMNG_RPM_LOACTION); fi

# Clear ssh key
RUN rm -f /home/jethro/.JethroKeys/id_rsa.pub && rm -f /home/jethro/.JethroKeys/id_rsa