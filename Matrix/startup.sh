#!/bin/bash

# echo -e $(python3 -u /home/pi/odas/python/recordingv4.py &) >> /home/pi/recordingLogs.txt
# python3 -u /home/pi/odas/python/recording.v3.py &
# python3 -u /home/pi/odas/python/watchdog.v1.py &

python3 -u /home/pi/odas/python/arecording.py &
python3 -u /home/pi/odas/python/odasPush.py &