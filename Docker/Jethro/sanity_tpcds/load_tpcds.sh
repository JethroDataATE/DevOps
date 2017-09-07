#!/bin/bash

# Create instance directories
su - jethro -c "mkdir /home/jethro/instances"
su - jethro -c "mkdir /home/jethro/cache"

# Create instance
su - jethro -c "JethroAdmin create-instance sanity_tpcds -storage-path=/home/jethro/instances -cache-path=/home/jethro/cache -cache-size=10G -Dstorage.type=POSIX"

# Create tables
su - jethro -c "JethroClient sanity_tpcds localhost:9111 -p jethro -i /jethro_install/createTables.sql"

# Create tables
su - jethro -c "JethroClient sanity_tpcds localhost:9111 -p jethro -q 'show tables'"

# Load data
declare -a tables=(
                "call_center" 
                "catalog_page"
                "catalog_returns"
                "catalog_sales"
                "customer"
                "customer_address"
                "customer_demographics"
                "date_dim"
                "household_demographics"
                "income_band"
                "inventory"
                "item"
                "promotion"
                "reason"
                "ship_mode"
                "store"
                "store_returns"
                "store_sales"
                "time_dim"
                "warehouse"
                "web_page"
                "web_returns"
                "web_sales"
                "web_site"
                )

# loop through the above tables array and create new load for each of them
for i in "${tables[@]}"
do
   echo "Loading into:  $i"

   # fetch load files
   wget http://jethro-automation.s3.amazonaws.com/data/sanity_tpcds/$i/$i
   wget http://jethro-automation.s3.amazonaws.com/data/sanity_tpcds/$i/$i.desc
   chmod 777 $i
   chmod 777 $i.desc

   # create load
   su - jethro -c "JethroLoader sanity_tpcds /jethro_install/$i.desc /jethro_install/$i"

   # Cleanup
   rm -f $i/$i
   rm -f $i/$i.desc
done




