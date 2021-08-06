#!/bin/bash

MOUNTDIR='/Users/odas2/Google Drive/My Drive/ODAS'
USERNAME="pi"
PINUMBER=0


echo -e "Enter Pi's ID Number (Default = 0) .\n\
\tCurrent Raspberry Pi ID = $PINUMBER \n\
Leave Blank and Hit Enter to keep current Pi ID Number"
read newPiNumber
if [ "$newPiNumber" = "" ] ; then
        echo -e "Raspberry Pi ID Number: $PINUMBER \n"
else
        echo -e "Replacing Raspberry Pi ID Number $PINUMBER -> $newPiNumber
     \n"
        PINUMBER=$newPiNumber
    
fi

IPLOG="${MOUNTDIR}/IP${PINUMBER}.log"
LATEST_IP="$(python3 read_ip.py --log_file "${IPLOG}")"

echo -e "Raspberry Pi ${PINUMBER} 's IP Address: \n \
\t ${LATEST_IP} \n"

echo -e "Now Attempting to SSH ..."
ssh ${USERNAME}@${LATEST_IP} 
