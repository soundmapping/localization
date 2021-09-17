#!/bin/bash
find /home/pi/odas/recordings/SSL -mmin +15 -exec rm {} \;
find /home/pi/odas/recordings/SST -mmin +15 -exec rm {} \;
find /home/pi/odas/recordings/separated -mmin +15 -exec rm {} \;
find /home/pi/odas/recordings/postfiltered -mmin +15 -exec rm {} \;
find /home/pi/odas/recordings/pureRaw -mmin +15 -exec rm {} \;

ls -1 /home/pi/odas/recordings/arecordLog/ | grep -E -v "recording.log|recording.raw|aTmT.txt" | xargs rm -f