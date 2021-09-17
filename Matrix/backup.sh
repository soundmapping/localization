
#! /bin/bash
rclone copy /home/pi/odas/recordings/SST RaspberryPi:/ODAS/logs7/SST
rclone copy /home/pi/odas/recordings/SSL RaspberryPi:/ODAS/logs7/SSL
rclone copy /home/pi/odas/recordings/separated RaspberryPi:/ODAS/recordings7/separated
rclone copy /home/pi/odas/recordings/postfiltered RaspberryPi:/ODAS/recordings7/postfiltered
rclone copy /home/pi/odas/recordings/pureRaw RaspberryPi:/ODAS/recordings7/pureRaw
rclone copy /home/pi/odas/recordings/arecordLog RaspberryPi:/ODAS/recordings7/arecordLog
