#!/bin/bash
# This script upload file to a S3 bucket.

# exit script on first error.
set -e

filePath=$1
bucket=$2
bucket_inner_path=$2
updateLatest=$3
build_extension=$4

if [ -z $filePath ]
then
	echo "File path cannot be empty."
    exit 1
fi

if [ -z $bucket ]
then
	echo "Bucket name cannot be empty."
    exit 1
fi

if [ -z $bucket_inner_path ]
then
	echo "Bucket inner path cannot be empty."
    exit 1
fi

targetUrl="$bucket/$bucket_inner_path"

echo
echo ">> DEPLOY: copying $filePath to S3 at: $targetUrl"
aws s3 cp $filePath s3://$targetUrl --recursive --acl public-read

if ! [ -z $updateLatest ]
then

    if [ -z $build_extension ]
    then
        echo "build_extension is necessary in order to safely update latest path."
        exit 1
    fi

    echo 
    echo "Updating latest folder..."
    LATEST_PATH=$bucket_inner_path
    if  [[ "$LATEST_URL" == */ ]]  
    then
      LATEST_PATH=${bucket_inner_path}latest/
    else
      LATEST_PATH=$bucket_inner_path/latest/
    fi
    
    echo "Latest location: $LATEST_PATH"

    LATEST_URL="$bucket/$LATEST_PATH"
    # aws s3 rm --recursive s3://$LATEST_URL

    exsitedFiles=( $(aws s3api list-objects --bucket $bucket --prefix $LATEST_PATH | awk -v path="$LATEST_PATH" -v extension="$build_extension" -F ":" '{if(($0 ~ "Key") && ($2 !~ "$path\",") && ($2 ~ extension)) print substr($2,3, length($2)-5)}') )

    if ! [ -z ${exsitedFiles[0]} ]
    then
      echo
      echo "Matched file was found on 'latest' folder: ${exsitedFiles[0]} - deleting..."
      aws s3api delete-object --bucket jethro-gui --key ${exsitedFiles[0]}
    fi

    echo
    echo "Uploading file to 'latest' folder..."
    aws s3 cp $filePath s3://$LATEST_URL --recursive --acl public-read
fi

echo 
echo "Upload to S3 completed."