#!/bin/bash

# This Script is to automate the Array setup
# found at the Wiki: https://github.com/soundmapping/localization/wiki/Arrays 


# User Input for Installation
# PINUMBER=0
# echo -e "Enter Pi's ID Number (Default = 0) .\n\
# \tCurrent Raspberry Pi ID = $PINUMBER \n\
# Leave Blank and Hit Enter to keep current Pi ID Number"
# read newPiNumber
# if [ "$newPiNumber" = "" ] ; then
#         echo -e "Raspberry Pi ID Number: $PINUMBER \n"
# else
#         echo -e "Replacing Raspberry Pi ID Number $PINUMBER -> $newPiNumber
#      \n"
#         PINUMBER=$newPiNumber
    
# fi

SCRIPT=$(readlink -f "$0")

state_1(){
        (sudo crontab -l ; echo -e "@reboot su pi -c \"$SCRIPT\" ") | sudo crontab -
        echo -e "Now in State 1!"
        echo -e "Hello State 1!" > ~/Desktop/state_1.txt
        sudo reboot
}

state_2(){
        echo -e "Now in State 2!"
        echo -e "Hello State 2!" > ~/Desktop/state_2.txt
        sudo reboot
}

state_3(){
        echo -e "Now in State 3!"
        echo -e "Hello State 3!" > ~/Desktop/state_3.txt
        sudo reboot
}

state_end(){
        sudo crontab -l | grep -v "su pi -c \"$SCRIPT\"" | sudo crontab -
        echo -e "Thank you for Participating!"
        echo -e "Finished State, Please Delete This File" > ~/Desktop/end.txt
        rm ~/Desktop/state_1.txt
        rm ~/Desktop/state_2.txt
        rm ~/Desktop/state_3.txt
}

if [[ ! -f "/tmp/state.txt" ]] ; then
        echo -e "1" | tee /tmp/state.txt
        STATE_NUM=1
else
        STATE_NUM=$(cat /tmp/state.txt)
fi

case $STATE_NUM in

        1)
        state_1
        ;;
        2)
        state_2
        ;;
        3)
        state_3
        ;;
        4)
        state_end
        ;;
esac
