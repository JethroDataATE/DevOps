# Jethro over Docker (for HDP distribution) 

# based on jethrodata/jethro:HADOOP_BASE image
FROM jethrodata/jethro:HADOOP_BASE

# Build-time parameters
ARG JETHRO_RPM_LOACTION=http://jethro.io/latest-rpm
ARG JETHROMNG_RPM_LOACTION=http://jethro.io/latest-jethro-manager
ARG JAVA_VERSION=java-1.8.0-openjdk.x86_64
ARG HADOOP_DIST_VERSION=2.6.1

# install java
RUN yum -y install $JAVA_VERSION
ENV JAVA_HOME /usr/lib/jvm/jre

# install hadoop (HDP)
ADD http://public-repo-1.hortonworks.com/HDP/centos7/2.x/updates/$HADOOP_DIST_VERSION.0/hdp.repo /jethro_install
RUN cp /jethro_install/hdp.repo /etc/yum.repos.d/hdp.repo
RUN yum -y install hadoop-client

# install hive
RUN yum -y install hive

# install Jethro
ADD $JETHRO_RPM_LOACTION /jethro_install
RUN rpm -i /jethro_install/$(basename $JETHRO_RPM_LOACTION)

# Install Jethro Manager is asked
RUN if [ ! -z $JETHROMNG_RPM_LOACTION ]; then wget $JETHROMNG_RPM_LOACTION && rpm -i $(basename $JETHROMNG_RPM_LOACTION) && rm -f $(basename $JETHROMNG_RPM_LOACTION); fi

# Clear ssh key
RUN rm -f /home/jethro/.JethroKeys/id_rsa.pub && rm -f /home/jethro/.JethroKeys/id_rsa