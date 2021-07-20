
#! /bin/bash
IP=$(hostname -I)
time=$(date)
echo "$time: $IP" >> /home/pi/odas/IP6.log 
rclone copy /home/pi/odas/IP6.log RaspberryPi:/ODAS
