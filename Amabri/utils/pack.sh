#!/bin/bash

tar -xvf jethro-mpack.tar
rm -f /home/ec2/jethro-mpack.tar

#cd jethro-mpack/extensions/JethroExt/1.0.0/services/JETHRO/package/files/
#wget http://jethro-gui.s3.amazonaws.com/builds/master/jethromng-1.3.0-57p_cn6.x86_64.rpm
#wget http://jethrodownload.s3.amazonaws.com/RC/3.0.0/3.0.5/jethro-3.0.5-16389.x86_64.rpm
#cd /home/ec2-user
tar -zcvf jethro-mpack.tar.gz  jethro-mpack

ambari-server install-mpack --mpack=/home/ec2-user/jethro-mpack.tar.gz 
ambari-server restart

curl -u admin:admin -H 'X-Requested-By: ambari' -X PUT http://localhost:8080/api/v1/links/

echo "Done!"
