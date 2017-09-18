#!/bin/bash
#

# exit script on first error.
set -e

instanceName=$1
storagePath=$2
cachePath=/home/jethro/inst_cache/

instances=( $(su - jethro -c "JethroAdmin list-storage-instances -storage-path=$storagePath -Dstorage.type=HDFS" | awk -v instance="$instanceName" '{if ($1==instance) {print $1, $3}}') )

if ! [ -z ${instances[0]} ]
then
   echo
   echo "Instance found"
   echo "checking if already attched..."
   if [ -z ${instances[1]} ] || [ ${instances[1]} = "Not" ]
   then
      echo "instance not attached"
      echo "Attaching instance..."
      test -d $cachePath || su - jethro -c "mkdir -p $cachePath"
      su - jethro -c "JethroAdmin attach-instance $instanceName -storage-path=$storagePath -cache-path=$cachePath -cache-size=0G"
   else
      echo "instance already attached"
   fi

else
   echo "Instance $instanceName not found."
   echo "Creating instanse..."
   test -d $cachePath || su - jethro -c "mkdir -p $cachePath"
   su - jethro -c "JethroAdmin create-instance $instanceName -storage-path=$storagePath -cache-path=$cachePath -cache-size=0G"
fi
