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

# Returns aT & mT from file
# filename (string): textfile containing aT & mT (seperated by \n)
# aT: access time, mT: modified time
def read_aT_mT(filename) :
    f = open(filename)
    aT = f.readline()
    mT = f.readline()
    f.close()

    return aT, mT
    
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
recordingLog = "/home/pi/odas/recordings/arecordLog/recording.log"
usbLocation="/media/pi/ARRAY" + arrayInd

# start the program at a 5-minute mark, run countdown()
countdown5()

# start the recording loop
while True:  
    if not os.path.isfile(recordedRaw) :
        noFileStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". No Recordings to process yet\n"
        with open(recordingLog, "a") as f :
            f.write(noFileStr)
        print(noFileStr)
        print("Waiting to go into the next cycle...")
        countdown5()
        continue

    try:
        # start odaslive
        startStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Starting odaslive offline \n"
        with open(recordingLog, "a") as f :
            f.write(startStr)
        print(startStr)
        p2 = Popen(["./odaslive", "-vc", configDir],
                   cwd=wd,
                   universal_newlines=True,
                   stdout=PIPE)
        p2.wait()   # Wait for odaslive to finish
        with open(recordingLog, "a") as f :
            f.write(str(p2.communicate()[0]))
        # print(p2.communicate()[0])

        endStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Odaslive ended \n"
        with open(recordingLog, "a") as f :
            f.write(endStr)
        print(endStr)

        # Retrieve Timestamp
        f = open("/home/pi/odas/recordings/pureRaw/timeStamp.txt", "r")
        timeArray = f.readline()
        f.close()
        
        # obtain the last access and modified time of raw files
        # atime = os.path.getatime(recordedRaw)
        # mtime = os.path.getmtime(recordedRaw)
        # aT = datetime.fromtimestamp(atime)
        # mT = datetime.fromtimestamp(mtime)
        aT, mT = read_aT_mT("/home/pi/odas/recordings/arecordLog/aTmT.txt")
        
        date0, time0 = str(aT).split()
        time0 = time0.split('.')[0]
        Popen(["mv", "/home/pi/odas/recordings/arecordLog/aTmT.txt",
         "/home/pi/odas/recordings/arecordLog/" + timeArray + ".txt"])

        timeStr = "Time is " + str(datetime.fromtimestamp(timer.time())) \
            + ". Timestamp " + timeArray + " Retrieved \n"
        with open(recordingLog, "a") as f :
            f.write(timeStr)
        print(timeStr)

        # run odasparsing.py to check if SST.log has empty data
        p3 = Popen(["python3", "/home/pi/odas/python/odasparsing.py"], 
                   stdout=PIPE, 
                   stdin=PIPE, 
                   universal_newlines=True)    
        # flag returns a string that says if the file is or is not useful            
        flag = p3.communicate(input="/home/pi/odas/recordings/SST/SST.log")[0].strip()

        emptyStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Checked for useful data \n"
        with open(recordingLog, "a") as f :
            f.write(emptyStr)
        print(emptyStr)
        
        # append recording start time and end time to the end of SST.log and SSL.log
        with open("/home/pi/odas/recordings/SST/cleaned.log", "a") as f:
            f.write("Start time: " + str(aT) + "\n")
            f.write("End time: " + str(mT))
        
        with open("/home/pi/odas/recordings/SSL/SSL.log", "a") as f:
            f.write("Start time: " + str(aT) + "\n")
            f.write("End time: " + str(mT))

        # To support NTFS (since ext is not supported in MacOS)
        timeArray = timeArray.replace(":", "T")

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

        moveStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". recorded.raw -> allChannels.raw \n"
        with open(recordingLog, "a") as f :
            f.write(moveStr)
        print(moveStr)
        
        # upload SST log
        Popen(["rclone","copy",cSSTName,"RaspberryPi:/ODAS/logs"+arrayInd+"/SST"])

        sstStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". SST log successfully uploaded \n"
        with open(recordingLog, "a") as f :
            f.write(sstStr)
        print(sstStr)
        
        # if log file contains no data other than 0, delete raw files 
        key = "not useful"
        if flag == key:
            # Keep Raw File for reference
            os.rename("/home/pi/odas/recordings/pureRaw/allChannels.raw", rawName)
            upRaw = Popen(["cp","-v",rawName,usbLocation+"/ODAS/recordings"+arrayInd+"/pureRaw"],
                stdout=PIPE, stderr=PIPE)
            
            os.remove("/home/pi/odas/recordings/SSL/SSL.log")
            os.remove("/home/pi/odas/recordings/separated/separated.raw")
            os.remove("/home/pi/odas/recordings/postfiltered/postfiltered.raw")
#             os.remove("/home/pi/odas/recordings/pureRaw/allChannels.raw")
            rmStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Files has been removed or flushed \n"
            with open(recordingLog, "a") as f :
                f.write(rmStr)
            print(rmStr)
            # print("\n Files has been removed or flushed")
        else:          
            os.rename("/home/pi/odas/recordings/SSL/SSL.log", cSSLName)
            os.rename("/home/pi/odas/recordings/separated/separated.raw", sepName)
            os.rename("/home/pi/odas/recordings/postfiltered/postfiltered.raw", posName)
            os.rename("/home/pi/odas/recordings/pureRaw/allChannels.raw", rawName)
            # upload SSL, separated, postfiltered, pure raw files
            uploadingStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Starting mv to USB Drive \n"
            with open(recordingLog, "a") as f :
                f.write(uploadingStr)
            print(uploadingStr)
            Popen(["cp", "-v", cSSLName, usbLocation+"/ODAS/logs"+arrayInd+"/SSL"])
            Popen(["cp", "-v", cSSTName, usbLocation+"/ODAS/logs"+arrayInd+"/SST"])
            Popen(["cp","-v",sepName,usbLocation+"/ODAS/recordings"+arrayInd+"/separated"])
            Popen(["cp","-v",posName,usbLocation+"/ODAS/recordings"+arrayInd+"/postfiltered"])
            upRaw = Popen(["cp","-v",rawName,usbLocation+"/ODAS/recordings"+arrayInd+"/pureRaw"],
                stdout=PIPE, stderr=PIPE)

            # Popen(["rclone","copy",cSSLName,"RaspberryPi:/ODAS/logs"+arrayInd+"/SSL"])
            # Popen(["rclone","copy",sepName,"RaspberryPi:/ODAS/recordings"+arrayInd+"/separated"])
            # Popen(["rclone","copy",posName,"RaspberryPi:/ODAS/recordings"+arrayInd+"/postfiltered"])
            # upRaw = Popen(["rclone","copy",rawName,"RaspberryPi:/ODAS/recordings"+arrayInd+"/pureRaw"],
            #     stdout=PIPE, stderr=PIPE)
            upRawOut, upRawErr = upRaw.communicate()
            upRawStr = "\n Output of copying raw data: " + str(upRawOut) + \
                 "\n Error of Copying (Blank if None): " + str(upRawErr) + "\n"
            
            with open(recordingLog, "a") as f :
                f.write(upRawStr)
            
            uploadedStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Files uploaded to USB Drive \n"
            with open(recordingLog, "a") as f :
                f.write(uploadedStr)
            print(uploadedStr)

        cleanStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Clean up finished \n"
        with open(recordingLog, "a") as f :
            f.write(cleanStr)
        print(cleanStr)

        # wait until the next 5-minute mark
        print("Waiting to go into the next cycle...")
        countdown5()
                           
    except KeyboardInterrupt:
        p2.send_signal(signal.SIGINT)
        p2.wait()
        interruptStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Interrupted +.+  \n"
        with open(recordingLog, "a") as f :
            f.write(interruptStr)
        print(interruptStr)
        break
print("Recording ended")

odasPushStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". OdasPush.py terminated  \n"
with open(recordingLog, "a") as f :
    f.write(odasPushStr)
print(odasPushStr)
