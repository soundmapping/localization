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

# Recording Details
hardwareInfo = "hw:2,0"
sampleRate = "44100"
numChannels = "8"
typeFile = "raw"
outFile = "recording.raw"

# First set the working directory to /home/pi/odas/bin
wd = "/home/pi/odas/bin"
configDir = "../config/matrix-demo/matrix_creator_offline.cfg"

# File Location Details
recordedRaw = "/home/pi/odas/recordings/pureRaw/recorded.raw"

# start the program at a 5-minute mark, run countdown()
countdown5()

# start the recording loop
while True:  
    if not os.path.isfile(recordedRaw) :
        print("Waiting to go into the next cycle...")
        countdown5()

    try:
        # start odaslive
        startStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Starting odaslive offline \n"
        with open("/home/pi/odas/recordings/pureRaw/recording.log", "a") as f :
            f.write(startStr)
        print(startStr)
        p2 = Popen(["./odaslive", "-vc", configDir],
                   cwd=wd,
                   universal_newlines=True)
        p2.wait()   # Wait for odaslive to finish

        endStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Odaslive ended \n"
        with open("/home/pi/odas/recordings/pureRaw/recording.log", "a") as f :
            f.write(endStr)
        print(endStr)

        # Retrieve Timestamp
        f = open("/home/pi/odas/recordings/pureRaw/timeStamp.txt", "r")
        timeArray = f.readline()
        f.close()
        
        # obtain the last access and modified time of raw files
        atime = os.path.getatime(recordedRaw)
        mtime = os.path.getmtime(recordedRaw)
        aT = datetime.fromtimestamp(atime)
        mT = datetime.fromtimestamp(mtime)
        
        date0, time0 = str(aT).split()
        time0 = time0.split('.')[0]

        # run odasparsing.py to check if SST.log has empty data
        p3 = Popen(["python3", "/home/pi/odas/python/odasparsing.py"], 
                   stdout=PIPE, 
                   stdin=PIPE, 
                   universal_newlines=True)    
        # flag returns a string that says if the file is or is not useful            
        flag = p3.communicate(input="/home/pi/odas/recordings/SST/SST.log")[0].strip()
        
        # append recording start time and end time to the end of SST.log and SSL.log
        with open("/home/pi/odas/recordings/SST/cleaned.log", "a") as f:
            f.write("Start time: " + str(aT) + "\n")
            f.write("End time: " + str(mT))
        
        with open("/home/pi/odas/recordings/SSL/SSL.log", "a") as f:
            f.write("Start time: " + str(aT) + "\n")
            f.write("End time: " + str(mT))

        # Specify Timestamp on Recordings and Log Files
        cSSTName = "/home/pi/odas/recordings/SST/cSST_" + timeArray + ".log"
        cSSLName = "/home/pi/odas/recordings/SSL/cSSL_" + timeArray + ".log"
        sepName = "/home/pi/odas/recordings/separated/separated_" + timeArray + ".raw"
        posName = "/home/pi/odas/recordings/postfiltered/postfiltered_" + timeArray + ".raw"
        rawName = "/home/pi/odas/recordings/pureRaw/allChannels_" + timeArray + ".raw"
        
        # rename cleaned.log and remove SST.log
        os.rename("/home/pi/odas/recordings/SST/cleaned.log", cSSTName)
        os.remove("/home/pi/odas/recordings/SST/SST.log")
        
        # Rename recorded file into allChannels (Depend on config file)
        # os.remove(recordedRaw)
        os.rename(recordedRaw, "/home/pi/odas/recordings/pureRaw/allChannels.raw")
        
        # upload SST log
        Popen(["rclone","copy",cSSTName,"RaspberryPi:/ODAS/logs"+arrayInd+"/SST"])
        
        # if log file contains no data other than 0, delete raw files 
        key = "not useful"
        if flag == key:
            os.remove("/home/pi/odas/recordings/SSL/SSL.log")
            os.remove("/home/pi/odas/recordings/separated/separated.raw")
            os.remove("/home/pi/odas/recordings/postfiltered/postfiltered.raw")
            os.remove("/home/pi/odas/recordings/pureRaw/allChannels.raw")
            print("\n Files has been removed or flushed")
        else:          
            os.rename("/home/pi/odas/recordings/SSL/SSL.log", cSSLName)
            os.rename("/home/pi/odas/recordings/separated/separated.raw", sepName)
            os.rename("/home/pi/odas/recordings/postfiltered/postfiltered.raw", posName)
            os.rename("/home/pi/odas/recordings/pureRaw/allChannels.raw", rawName)
            # upload SSL, separated, postfiltered, pure raw files
            Popen(["rclone","copy",cSSLName,"RaspberryPi:/ODAS/logs"+arrayInd+"/SSL"])
            Popen(["rclone","copy",sepName,"RaspberryPi:/ODAS/recordings"+arrayInd+"/separated"])
            Popen(["rclone","copy",posName,"RaspberryPi:/ODAS/recordings"+arrayInd+"/postfiltered"])
            Popen(["rclone","copy",rawName,"RaspberryPi:/ODAS/recordings"+arrayInd+"/pureRaw"])

        cleanStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Clean up finished \n"
        with open("/home/pi/odas/recordings/pureRaw/recording.log", "a") as f :
            f.write(cleanStr)
        print(cleanStr)

        # wait until the next 5-minute mark
        print("Waiting to go into the next cycle...")
        countdown5()
                           
    except KeyboardInterrupt:
        p2.send_signal(signal.SIGINT)
        p2.wait()
        print("Interrupted +.+ ")
        break
print("Recording ended")
