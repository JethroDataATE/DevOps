#!/bin/bash

rm -f /home/ec2-user/jethro-mpack.tar.gz
rm -f /home/ec2-user/jethro-mpack.tar
rm -rf /home/ec2-user/jethro-mpack

ambari-server uninstall-mpack --mpack-name=jethro-mpack
ambari-server restart

echo "Done!"
