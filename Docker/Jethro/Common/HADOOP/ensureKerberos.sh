#!/bin/bash
#
# ensure kerberos is enabled 


function displayUsage {
  echo "Ensure Kerberos - a utility to ensure kerberos is enabled on this host."
  echo "USAGE: ensureKerberos.sh principle_name keyatb_path "
}

function generateNewTicktes {
  echo  "Generating kerberos tickets..."
  kinit -kt $keyatb_path $principle_name
}

###############################
# MAIN SCRIPT STARTS HERE
###############################

# General checks
if [[ $EUID -eq 0 ]]; then
  # Running as root messes local file permissions
  echo
  echo "Error - this script must run as a non-root user, exiting"
  exit 1
fi

if [[ $# -eq 2 ]]; then
  principle_name=$1
  keyatb_path=$2
else
  displayUsage
  exit 1
fi

echo "Ensuring kerberos tickets are valid for user: $USER"
echo

klist -s

#If no ticktes found at all - create them
if [[ ! $? -eq 0 ]]; then
  echo "No ticktes found!"
  generateNewTicktes
else
  # For every cache file we find do:
  for CACHE_FILE in $(find /tmp -maxdepth 1 -type f -name "krb5cc*$UID"); do
  
    echo "Tickets cache file found for current user at: $CACHE_FILE".
    
    # Find the current owner and group of the ticket cache
    OWNER=$( ls -n $CACHE_FILE | awk '{print $3}' )
    GROUP=$( ls -n $CACHE_FILE | awk '{print $4}' )
  
    # Find the expirey time of the ticket granting ticket
    EXPIRE_TIME=$( date -d "$( klist -c $CACHE_FILE | grep krbtgt | awk '{print $3, $4}' )" +%s )
    echo "Ticket expertion date: $(date -d @$EXPIRE_TIME)".
  
    # If it has already expired, might as well delete it
    if [ $( date +%s ) -ge $EXPIRE_TIME ]; then
      kdestroy -c $CACHE_FILE &> /dev/null
      echo "Removed expired ticket cache ($CACHE_FILE) for user $USER"
      generateNewTicktes
  
    # Otherwise renew it
    elif [ $( expr $EXPIRE_TIME - $( date +%s ) ) -le 300 ]; then
      echo "Renewing exiting tickets..."
      kinit -R -c $CACHE_FILE &> /dev/null
      if [ $? -ne 0 ]; then
        echo "An error occurred while renewing $CACHE_FILE"
        echo "Regenrating ticktes..."
        echo
        generateNewTicktes
      else
        chown $OWNER:$GROUP $CACHE_FILE &> /dev/null
        echo "Renewed ticket cache ($CACHE_FILE) for user $USER"
      fi
    else
      echo
      echo "Tickets are still valid - nothing to do..."
    fi
  done
fi

echo
echo "Done!"
