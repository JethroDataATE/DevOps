#!/bin/bash
# This script upload file to a S3 bucket.

# exit script on first error.
set -e

filePath=$1
targetUrl=$2
updateLatest=$3

if [ -z $filePath ]
then
	echo "File path cannot be empty."
    exit 1
fi

if [ -z $targetUrl ]
then
	echo "Target URL cannot be empty."
    exit 1
fi

echo
echo ">> DEPLOY: copying $filePath to S3 at: $targetUrl"
aws s3 cp $filePath s3://$targetUrl --recursive --acl public-read

if [ -z $updateLatest ]
then
    # Do nothing
else
    echo 
    echo "Updating latest folder..."
    aws s3 rm --recursive s3://$targetUrl/latest/
    aws s3 cp $filePath s3://$targetUrl/latest/ --recursive --acl public-read
fi

echo 
echo "Upload to S3 completed."