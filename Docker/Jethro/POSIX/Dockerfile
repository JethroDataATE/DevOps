# Jethro over Docker (for POSIX env)

# based on centos(7):latest image
FROM centos:7

# Build-time parameters
ARG JETHRO_RPM_LOACTION=http://jethro.io/latest-rpm
ARG JETHROMNG_RPM_LOACTION=http://jethro.io/latest-jethro-manager
ARG JAVA_VERSION=java-1.8.0-openjdk.x86_64

WORKDIR /jethro_install

COPY Common/dockerBootstrap /jethro_install

# install systemd
RUN yum -y update; yum clean all
RUN yum -y install systemd initscripts; yum clean all

# install java
RUN yum -y install $JAVA_VERSION; yum clean all
ENV JAVA_HOME /usr/lib/jvm/jre

# install ssh
RUN yum -y install openssh openssh-server openssl openssh-clients; yum clean all

# Install utilities
RUN yum -y install which wget; yum clean all

# User mode parameters
ENV USER_ID 501 
ENV GROUP_ID 501

# change jethro user/group mode
RUN groupadd jethro --gid $GROUP_ID &&adduser jethro --uid $USER_ID --gid $GROUP_ID && echo jethro | passwd jethro --stdin
ENV JETHRO_INSTALL_USER=jethro
ENV JETHRO_INSTALL_GROUP=jethro

# install Jethro
ADD $JETHRO_RPM_LOACTION /jethro_install
RUN rpm -i /jethro_install/$(basename $JETHRO_RPM_LOACTION) && rm -f /jethro_install/$(basename $JETHRO_RPM_LOACTION)

# Install Jethro Manager is asked
RUN if [ ! -z $JETHROMNG_RPM_LOACTION ]; then wget $JETHROMNG_RPM_LOACTION && rpm -i $(basename $JETHROMNG_RPM_LOACTION) && rm -f $(basename $JETHROMNG_RPM_LOACTION); fi

# Clear ssh key
RUN rm -f /home/jethro/.JethroKeys/id_rsa.pub && rm -f /home/jethro/.JethroKeys/id_rsa

# SSH key generation parameters
ENV KEY_PATH "" 
ENV GENERAT_KEY_IF_NOT_EXIST "false"

# configure volumes
RUN mkdir /jethro -m 777 && mkdir /jethro/persist -m 777 && mkdir /jethro/instance_storage -m 777 && mkdir /jethro/instance_cache -m 777
VOLUME ["/jethro/persist", "/opt/jethro/instances", "/var/log/jethro", "/jethro/instance_storage", "/jethro/instance_cache"]

# Docker run options
ENV INSTANCE_NAME ""
ENV INSTANCE_STORAGE_PATH ""
ENV INSTANCE_CACHE_PATH "/home/jethro/instances_cache"
ENV INSTANCE_CACHE_SIZE "0G"
ENV RUN_JETHRO_MANAGER ""

# start container
RUN chmod a+x /jethro_install/dockerBootstrap
ENTRYPOINT ["sh", "-c", "/jethro_install/dockerBootstrap"]

# expose needed port numbers
EXPOSE 9100-9200 22