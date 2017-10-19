#!/bin/bash

tar -xvf jethro-mpack.tar
rm -f /home/ec2/jethro-mpack.tar
tar -zcvf jethro-mpack.tar.gz  jethro-mpack

ambari-server install-mpack --mpack=/home/ec2-user/jethro-mpack.tar.gz 
ambari-server restart

curl -u admin:admin -H 'X-Requested-By: ambari' -X PUT http://localhost:8080/api/v1/links/

echo "Done!"
