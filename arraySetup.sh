#!/bin/bash

# This Script is to automate the Array setup
# found at the Wiki: https://github.com/soundmapping/localization/wiki/Arrays 


# User Input for Installation
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

# Installing Matrix Software
curl https://apt.matrix.one/doc/apt-key.gpg | sudo apt-key add -
echo "deb https://apt.matrix.one/raspbian $(lsb_release -sc) main" | sudo tee /etc/apt/sources.list.d/matrixlabs.list

sudo apt-get update -y
sudo apt-get upgrade -y

sudo apt install matrixio-creator-init -y
sudo apt install libmatrixio-creator-hal -y
sudo apt install libmatrixio-creator-hal-dev -y

sudo apt install matrixio-kernel-modules -y

# Installing ODAS
# Dependencies:
sudo apt-get install g++ git cmake
sudo apt-get install libfftw3-dev
sudo apt-get install libconfig-dev
sudo apt-get install libasound2-dev
sudo apt install libjson-c-dev

cd ~/
git clone https://github.com/soundmapping/odas.git
cd odas
git checkout record
mkdir build
cd build
cmake ..
make

# Installing Recording System
curl -L https://raw.github.com/pageauc/rclone4pi/master/rclone-install.sh | bash

sudo apt-get install ntp -y
sudo systemctl stop systemd-timesyncd
sudo systemctl disable systemd-timesyncd
​sudo /etc/init.d/ntp stop
sudo /etc/init.d/ntp start

# Clock Synchronization
sudo echo -e "# pool.ntp.org maps to more than 300 low-stratum NTP servers. \n\
# Your server will pick a different set every time it starts up. \n\
# *** Please consider joining the pool! *** \n\
# *** *** \n\
server ntp.ucsd.edu \n" >> /etc/ntp.conf

sudo /etc/init.d/ntp restart

cd ~/odas
git clone https://github.com/soundmapping/localization.git
cd localization
git checkout array

# Enable SSH & Build Array
sudo systemctl enable ssh
sudo systemctl start ssh
python3 build.py ${PINUMBER}
sudo reboot
