#!/usr/bin/env python
# coding: utf-8
# By YiHan Hu & Henrry Gunawan

import os
import time as timer
from datetime import datetime
from subprocess import Popen, PIPE
import signal

# Define countdown(): a function that calculates the time difference T between now and the next 5 minute mark
# Put the system to sleep for the length of T
def countdown5():
    timestamp = timer.time()
    t1 = datetime.fromtimestamp(timestamp)
    t2 = datetime.fromtimestamp(timestamp + 300 - timestamp % 300)
    duration = t2 - t1
    sleepTime = round(duration.total_seconds(),3)
    print("Time is " + str(t1) + ". Going to sleep now...")
    timer.sleep(sleepTime)
    print("Time is " + str(datetime.fromtimestamp(timer.time())) + ". Waking up now...")
    
# Find the array Index
f = open("/home/pi/odas/arrayInfo.txt","r")
arrayInd = f.readline()
f.close()
arrayAppendix = "_" + arrayInd

# First set the working directory to /home/pi/odas/bin
wd = "/home/pi/odas/recordings/pureRaw/"
configDir = "../config/matrix-demo/matrix_creator_wRaw.cfg"

# Recording Details
hardwareInfo = "hw:2,0"
sampleFormat = "S16_LE"
sampleRate = "44100"
numChannels = "8"
typeFile = "raw"
outFile = wd + "recording.raw"

if int(arrayInd) == 5 : # Only Applies to Device 6 because of Hardware Interface
    hardwareInfo = "hw:3,0"

# start the program at a 5-minute mark, run countdown()
countdown5()

# start the recording loop
while True:  
    try:
        # start odaslive
        startStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Starting arecord command \n"
        with open("/home/pi/odas/recordings/pureRaw/recording.log", "a") as f :
            f.write(startStr)
        print(startStr)
        p2 = Popen(["arecord","-v", "-D", hardwareInfo,
            "-t", typeFile, "-r", sampleRate, "-f", sampleFormat,
            "-c", numChannels, outFile])
        # leave 10s for the remaining process and clean up
        timer.sleep(290)
        # end odaslive
        p2.send_signal(signal.SIGINT)
        p2.wait()

        endStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". arecord ended \n"
        with open("/home/pi/odas/recordings/pureRaw/recording.log", "a") as f :
            f.write(endStr)
        print(endStr)
        
        # obtain the last access and modified time of raw files
        atime = os.path.getatime("/home/pi/odas/recordings/pureRaw/recording.raw")
        mtime = os.path.getmtime("/home/pi/odas/recordings/pureRaw/recording.raw")
        aT = datetime.fromtimestamp(atime)
        mT = datetime.fromtimestamp(mtime)
        
        date0, time0 = str(aT).split()
        time0 = time0.split('.')[0]
        timeArray = date0 + "_" + time0 + arrayAppendix

        with open("/home/pi/odas/recordings/pureRaw/timeStamp.txt", "w") as f :
            f.write(timeArray)

        Popen(["mv", outFile, wd+"recorded.raw"]) # File has been fully recorded

        # wait until the next 5-minute mark
        print("Waiting to go into the next cycle...")
        countdown5()
                           
    except KeyboardInterrupt:
        p2.send_signal(signal.SIGINT)
        p2.wait()
        print("Interrupted +.+ ")
        break
print("Recording ended")

