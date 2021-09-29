#!/usr/bin/env python
# coding: utf-8

# CSE4223-ODAS will be installed in /home/pi/odas

import subprocess as p

def usbSetup(arrayInd) :
    usbLocation = "/media/pi/ARRAY" + arrayInd
    odasDir = usbLocation + "/ODAS"

    # create ODAS Folder
    p.run(["mkdir", "ODAS"], cwd=usbLocation)
    # create logs & recordings folder
    p.run(["mkdir","logs"+arrayInd, "recordings"+arrayInd],cwd=odasDir)
    p.run(["mkdir","SST","SSL"],cwd=odasDir+"/logs"+arrayInd)
    p.run(["mkdir","separated","postfiltered","pureRaw"],cwd=odasDir+"/recordings"+arrayInd) 
    p.run(["mkdir","arecordLog"],cwd=odasDir+"/recordings"+arrayInd)


# Setting up working directory
wd = "/home/pi/odas/localization/Matrix"

# Ask for array index from user input 
arrayInd = input("Enter array index: ")

# Create backup.sh based on array index
with open ("/home/pi/odas/localization/Matrix/backup.sh", "w") as rsh:
    rsh.write(
'''
#! /bin/bash
rclone copy /home/pi/odas/recordings/SST RaspberryPi:/ODAS/logs{0}/SST
rclone copy /home/pi/odas/recordings/SSL RaspberryPi:/ODAS/logs{0}/SSL
rclone copy /home/pi/odas/recordings/separated RaspberryPi:/ODAS/recordings{0}/separated
rclone copy /home/pi/odas/recordings/postfiltered RaspberryPi:/ODAS/recordings{0}/postfiltered
rclone copy /home/pi/odas/recordings/pureRaw RaspberryPi:/ODAS/recordings{0}/pureRaw
rclone copy /home/pi/odas/recordings/arecordLog RaspberryPi:/ODAS/recordings{0}/arecordLog
'''.format(arrayInd))

# Create IPupload.sh based on array index
with open ('/home/pi/odas/localization/Matrix/IPupload.sh', 'w') as rsh:
    rsh.write(
'''
#! /bin/bash
IP=$(hostname -I)
time=$(date)
echo "$time: $IP" >> /home/pi/odas/IP{0}.log 
rclone copy /home/pi/odas/IP{0}.log RaspberryPi:/ODAS
''' .format(arrayInd))

# Save arrayInd into a file
with open("/home/pi/odas/arrayInfo.txt","w") as f:
    f.writelines(arrayInd)
    # f.write(str(arrayInd))

# Create USB Directory
usbSetup(arrayInd)

# Make bash scripts executables, set up crontab, set up rclone, and copy files to their working directory
p.run(["sudo","chmod","+x","cleanup.sh","filemanager.sh","startup.sh","IPupload.sh","backup.sh"],cwd=wd)
p.run(["sudo","crontab","crontab"],cwd=wd)
p.run(["cp","backup.sh","cleanup.sh","crontab","filemanager.sh","IPupload.sh","rclone.conf","startup.sh","/home/pi/odas"],cwd=wd)
p.run(["mkdir","matrix-demo"],cwd="/home/pi/odas/config")

# Updated config files
p.run(["cp","matrix_creator_local.cfg","/home/pi/odas/config/matrix-demo"],cwd=wd)
p.run(["cp","matrix_creator_wRaw.cfg","/home/pi/odas/config/matrix-demo"],cwd=wd)
p.run(["cp","matrix_creator_wRaw_dev6.cfg","/home/pi/odas/config/matrix-demo"],cwd=wd)
p.run(["cp","matrix_creator_offline.cfg","/home/pi/odas/config/matrix-demo"],cwd=wd)

p.run(["cp","-r","python","/home/pi/odas"],cwd=wd)
p.run(["cp","rclone.conf","/home/pi/.config/rclone"],cwd=wd)

# create recordings folder
p.run(["mkdir","recordings"],cwd="/home/pi/odas")
p.run(["mkdir","SST","SSL","separated","postfiltered","pureRaw"],cwd="/home/pi/odas/recordings") 
p.run(["mkdir","arecordLog"],cwd="/home/pi/odas/recordings")


# reboot
p.run(["sudo","reboot"])