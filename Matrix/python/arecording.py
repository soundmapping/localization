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
wd = "/home/pi/odas/recordings/arecordLog/"
configDir = "../config/matrix-demo/matrix_creator_wRaw.cfg"

# Recording Details
hardwareInfo = "hw:2,0"
sampleFormat = "S16_LE"
sampleRate = "32000"
numChannels = "8"
typeFile = "raw"

outFile = wd + "recording.raw"
recordingLog = "/home/pi/odas/recordings/arecordLog/recording.log"
recordedRaw = "/home/pi/odas/recordings/pureRaw/recorded.raw"

if int(arrayInd) == 7 : # Only Applies to Device 6 because of Hardware Interface
    hardwareInfo = "hw:3,0"

# start the program at a 5-minute mark, run countdown()
countdown5()

# start the recording loop
while True:  
    try:
        # start odaslive
        startStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Starting arecord command \n"
        with open(recordingLog, "a") as f :
            f.write(startStr)
        print(startStr)
        p2 = Popen(["arecord","-v", "-D", hardwareInfo,
            "-t", typeFile, "-r", sampleRate, "-f", sampleFormat,
            "-c", numChannels, outFile],
            universal_newlines=True,
            stdout=PIPE)
        # leave 20s for the remaining process and clean up
        timer.sleep(280)
        # end odaslive
        p2.send_signal(signal.SIGINT)
        p2.wait()

        # print("p2.communicate = ", type(p2.communicate()))
        # print("Accessing index 0 = ", type(p2.communicate()[0]))
        p2out, p2err = p2.communicate()

        with open(recordingLog, "a") as f :
            arecordStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + \
                str(p2out) + ", \n Errors found (blank=None): " + str(p2err) + "\n" 
            f.write(arecordStr)

        endStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". arecord ended \n"
        with open(recordingLog, "a") as f :
            f.write(endStr)
        print(endStr)
        
        # obtain the last access and modified time of raw files
        atime = os.path.getatime(outFile)
        mtime = os.path.getmtime(outFile)
        aT = datetime.fromtimestamp(atime)
        mT = datetime.fromtimestamp(mtime)
        
        date0, time0 = str(aT).split()
        time0 = time0.split('.')[0]
        timeArray = date0 + "_" + time0 + arrayAppendix
        timeLog = "/home/pi/odas/recordings/arecordLog/aTmT.txt"

        with open(timeLog, "w") as f :
            f.write(str(aT))
            f.write("\n")
            f.write(str(mT))

        with open("/home/pi/odas/recordings/pureRaw/timeStamp.txt", "w") as f :
            f.write(timeArray)

        Popen(["mv", outFile, recordedRaw]) # File has been fully recorded
        # Popen(["rclone","copy",timeLog,"RaspberryPi:/ODAS/recordings"+arrayInd+"/arecordLog"])

        # wait until the next 5-minute mark
        print("Waiting to go into the next cycle...")
        countdown5()
                           
    except KeyboardInterrupt:
        p2.send_signal(signal.SIGINT)
        p2.wait()

        with open(recordingLog, "a") as f :
            f.write("arecord: Interrupted +.+ ")
        print("Interrupted +.+ ")
        break

with open(recordingLog, "a") as f :
    f.write("arecord: Recording ended")
print("Recording ended")

