#!/bin/bash
#
# ensure kerberos is enabled 


function display_usage {
echo "Ensure Kerberos - a utility to ensure kerberos is enabled on this host."
echo "USAGE: ensureKerberos.sh principle_name keyatb_path "
}

###############################
# MAIN SCRIPT STARTS HERE
###############################
ARGS=( "$@" )
# General checks
if [[ $EUID -eq 0 ]]; then
  # Running as root messes local file permissions
  echo
  echo "Error - this script must run as a non-root user, exiting"
  exit 1
fi

if [[ $# -eq 2 ]]; then
  principle_name=`echo $1 | tr [:upper:] [:lower:]`
  keyatb_path=`echo $2 | tr [:upper:] [:lower:]`
else
  display_usage
  exit 1
fi

echo  "Generating kerberos tickets..."
kinit -r 1440m -kt $keyatb_path $principle_name
sleep 1
kinit -R

echo "Done!"

