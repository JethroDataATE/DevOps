#!/bin/bash
#

# exit script on first error.
set -e

# Input paramaters
rpmPath=$1
jethroUser=$2
jethroGroup=$3


rpmName=$(basename $rpmPath)
rpmLocalPath="/tmp/$rpmName"
currentJethro=$(rpm -qa jethro)

# if jethro already installed (and the versions are the same) exit
if [ ! -z $currentJethro ] && [ "$currentJethro.rpm" == $rpmName ]
then
    echo "Jethro already installed."
    exit 0
fi

# check rpm located on hdfs
if [[ "$rpmPath" == hdfs://* ]] ; then
    echo
    echo "Search for rpm path on hdfs..."

    if su - hdfs -c "hdfs dfs -test -e $rpmPath";
    then
    echo "$rpmPath exists!"

    # copy key file
    echo "Copy key file to local fs."
    su - hdfs -c "hadoop fs -copyToLocal $rpmPath $rpmLocalPath"
    else
    echo "$rpmName not found on HDFS"
    exit 1
    fi

elif [[ "$rpmPath" == http* ]] ; then
    echo
    echo "Downloading rpm from s3..."
    cd /tmp
    wget $rpmPath
else
    echo "rpm path not supported."
    exit 1
fi


echo "Installing..."

if  [[ "$jethroUser" != "jethro" ]] ; then
    export JETHRO_INSTALL_USER=$jethroUser
    export JETHROMNG_INSTALL_USER=$jethroUser
fi

if  [[ "$jethroGroup" != "jethro" ]] ; then
    export JETHRO_INSTALL_GROUP=$jethroGroup
    export JETHROMNG_INSTALL_GROUP=$jethroGroup
fi

rpm -Uvh --force $rpmLocalPath

sleep 3
test -d /opt/jethro/instances/jethro.out && chown $jethroUser:$jethroGroup /opt/jethro/instances/jethro.out

# Clean temp file
rm -f $rpmLocalPath
