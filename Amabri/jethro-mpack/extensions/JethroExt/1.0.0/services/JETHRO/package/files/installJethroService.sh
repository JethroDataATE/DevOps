#!/bin/bash
#

# exit script on first error.
set -e

# Input paramaters
rpmName=$1
service=$2
instanceName=$3
storagePath=$4

# local params
services_ini_path=/opt/jethro/instances/services.ini
cachePath=/home/jethro/inst_cache
currentJethro=$(rpm -qa jethro)
port=""


resetInstanceServicesConfig() {
    port=$(awk -F  ":" -v instance="$instanceName" '{if ($1==instance) {print $2}}'  /opt/jethro/instances/services.ini)
    sed -i "/$instanceName/c $instanceName:$port:no:no:no" /opt/jethro/instances/services.ini
}

# Install jethro if not installed (or if the current installed version is different)
if [ -z $currentJethro ] || [ "$currentJethro*" = $rpmName ]
then
    echo "Installing jethro"
    rpm -Uvh --force "/tmp/$rpmName"
fi

# Clean temp file
rm -f "/tmp/$rpmName"

# Create/attach instance
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
      test -d $cachePath && rm -rf $cachePath
      su - jethro -c "mkdir -p $cachePath"
      su - jethro -c "JethroAdmin attach-instance $instanceName -storage-path=$storagePath -cache-path=$cachePath -cache-size=0G"
      resetInstanceServicesConfig
   else
      echo "instance already attached"
   fi

else
   echo "Instance $instanceName not found."
   echo "Creating instanse..."
   test -d $cachePath && rm -rf $cachePath
   su - jethro -c "mkdir -p $cachePath"
   su - jethro -c "JethroAdmin create-instance $instanceName -storage-path=$storagePath -cache-path=$cachePath -cache-size=0G"
   resetInstanceServicesConfig
fi

# Stopping all running jethro services
service jethro stop

# Update ini path
port=$(awk -F  ":" -v instance="$instanceName" '{if ($1==instance) {print $2}}'  /opt/jethro/instances/services.ini)
echo "instance port: $port"
server=$(awk -F  ":" -v instance="$instanceName" '{if ($1==instance) {print $3}}'  /opt/jethro/instances/services.ini)
maint=$(awk -F  ":" -v instance="$instanceName" '{if ($1==instance) {print $4}}'  /opt/jethro/instances/services.ini)
loadscheduler=$(awk -F  ":" -v instance="$instanceName" '{if ($1==instance) {print $5}}'  /opt/jethro/instances/services.ini)


echo "Replacing services.ini content..."
if [ $service = "server"]
then
    sed -i "/$instanceName/c $instanceName:$port:yes:$maint:$loadscheduler" /opt/jethro/instances/services.ini
fi

if [ $service = "maint"]
then
    sed -i "/$instanceName/c $instanceName:$port:$server:yes:$loadscheduler" /opt/jethro/instances/services.ini
fi

if [ $service = "loadscheduler"]
then
    sed -i "/$instanceName/c $instanceName:$port:$server:$maint:yes" /opt/jethro/instances/services.ini
fi

echo
echo "Done!"








