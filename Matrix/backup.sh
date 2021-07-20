
#! /bin/bash
rclone copy /home/pi/odas/recordings/SST RaspberryPi:/ODAS/logs6/SST
rclone copy /home/pi/odas/recordings/SSL RaspberryPi:/ODAS/logs6/SSL
rclone copy /home/pi/odas/recordings/separated RaspberryPi:/ODAS/recordings6/separated
rclone copy /home/pi/odas/recordings/postfiltered RaspberryPi:/ODAS/recordings6/postfiltered
rclone copy /home/pi/odas/recordings/pureRaw RaspberryPi:/ODAS/recordings6/pureRaw
