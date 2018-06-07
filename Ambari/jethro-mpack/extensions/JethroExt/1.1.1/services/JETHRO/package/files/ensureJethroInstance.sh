#!/bin/bash
#

# exit script on first error.
set -e

# Input paramaters
service=$1
instanceName=$2
storagePath=$3
cachePath=$4
cacheSizeNumber=$5
jethroUser=$6

# local params
services_ini_path=/opt/jethro/instances/services.ini
cacheSizeUnits=G
port=""

cacheSize=$cacheSizeNumber$cacheSizeUnits

resetInstanceServicesConfig() {
    # Stop all instance services (will be started from python)
    service jethro stop $instanceName
    service jethro stop $instanceName maint
    service jethro stop $instanceName loadscheduler

    # Reset services.ini
    port=$(awk -F  ":" -v instance="$instanceName" '{if ($1==instance) {print $2}}'  /opt/jethro/instances/services.ini)
    sed -i "/$instanceName/c $instanceName:$port:no:no:no" /opt/jethro/instances/services.ini
}

# Create/attach instance
instances=( $(su - $jethroUser -c "JethroAdmin list-storage-instances -storage-path=$storagePath -Dstorage.type=HDFS" | awk -v instance="$instanceName" '{if ($1==instance) {print $1, $3}}') )
if ! [ -z ${instances[0]} ]
then
   echo
   echo "Instance found"
   echo "checking if already attched..."
   if [ -z ${instances[1]} ] || [ ${instances[1]} = "Not" ]
   then
      echo "instance not attached"
      echo "Attaching instance..."
      test -d $cachePath || su - $jethroUser -c "mkdir -p $cachePath"
      su - $jethroUser -c "JethroAdmin attach-instance $instanceName -storage-path=$storagePath -cache-path=$cachePath -cache-size=$cacheSize"
      
      resetInstanceServicesConfig
   else
      echo "instance already attached"
   fi

else
   echo "Instance $instanceName not found."
   echo "Creating instanse..."
   test -d $cachePath || su - $jethroUser -c "mkdir -p $cachePath"
   su - $jethroUser -c "JethroAdmin create-instance $instanceName -storage-path=$storagePath -cache-path=$cachePath -cache-size=$cacheSize"
   resetInstanceServicesConfig
fi

# Update ini path 
port=$(awk -F  ":" -v instance="$instanceName" '{if ($1==instance) {print $2}}'  /opt/jethro/instances/services.ini)
echo "instance port: $port"
server=$(awk -F  ":" -v instance="$instanceName" '{if ($1==instance) {print $3}}'  /opt/jethro/instances/services.ini)
maint=$(awk -F  ":" -v instance="$instanceName" '{if ($1==instance) {print $4}}'  /opt/jethro/instances/services.ini)
loadscheduler=$(awk -F  ":" -v instance="$instanceName" '{if ($1==instance) {print $5}}'  /opt/jethro/instances/services.ini)


echo "Replacing services.ini content..."
if [ $service == "server" ]
then
    sed -i "/$instanceName/c $instanceName:$port:yes:$maint:$loadscheduler" /opt/jethro/instances/services.ini
    su - $jethroUser -c "service jethro start $instanceName"
    sleep 10
    su - $jethroUser -c "JethroClient $instanceName localhost:$port -u $jethroUser -p jethro -q 'set global dynamic.aggregation.auto.generate.enable=1;'"
fi

if [ $service == "maint" ]
then
    sed -i "/$instanceName/c $instanceName:$port:$server:yes:$loadscheduler" /opt/jethro/instances/services.ini
fi

if [ $service == "loadscheduler" ]
then
    sed -i "/$instanceName/c $instanceName:$port:$server:$maint:yes" /opt/jethro/instances/services.ini
fi

echo
echo "Done!"








