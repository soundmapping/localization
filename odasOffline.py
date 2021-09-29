#!/usr/bin/env python
# coding: utf-8
# By YiHan Hu & Henrry Gunawan

import os
import time as timer
from datetime import datetime
from subprocess import Popen, PIPE
import signal
import numpy as np

# Define countdown(): a function that calculates the time difference T between now and the next 5 minute mark
# Put the system to sleep for the length of T
def countdown(rhythm_in_seconds = 300):
    timestamp = timer.time()
    t1 = datetime.fromtimestamp(timestamp)
    t2 = datetime.fromtimestamp(
            timestamp + rhythm_in_seconds - timestamp % rhythm_in_seconds)
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
    
from sys import platform as pf
if pf == "linux": # PI
    # Find the array Index
    f = open("/home/pi/odas/arrayInfo.txt","r")
    arrayInd = f.readline()
    f.close()
    odaspath = "/home/pi/odas"
    usbLocation  = "/media/pi/" + arrayInd
elif pf == "darwin": # manu macOS
    arrayInd = str(0)
    odaspath = "/Users/mha/dtu/mpl/odas"
    usbLocation = "/Volumes/"
    # ARRAY0/noSST/recordings3/pureRaw/allChannels_2021-09-24_08:30:00_3.raw

arrayAppendix = "_" + arrayInd
usbLocation  = "".join([usbLocation,"ARRAY",arrayInd])
recpath = "/Volumes/ARRAY0/noSST/"
recordingLog = "./recording.log"

odasConfigTemplate = "./../matrix_creator_offline.cfg"
odasConfigTmp = "./tmp_matrix_creator_offline.cfg"

# Recording Details
hardwareInfo = "hw:2,0"
sampleRate   = "44100"
numChannels  = "8"
typeFile     = "raw"
outFile      = "recording.raw"

# find all raw recursively and append in raw_files
raw_files = []
for dirpath, subdirs, files in os.walk(recpath):
    for x in files:
        if x.endswith(".raw"):
            raw_files.append(os.recpath.join(dirpath, x))
print("found these files in ", recpath)
[print(ff) for ff in raw_files]
print("\n")

# start the program at a (time%seconds==0) mark, run countdown(seconds), default 300 seconds
countdown(2)

def gen_config(
    raw_input_filepath, 
    target_path          = None, 
    template_config_path = "./../matrix_creator_offline.cfg",
    target_config_path   = "./tmp_matrix_creator_offline.cfg",
    verbose = False,
    ):
    # this function parses identifiers from raw filename, 
    # and replaces the paths in the ODAS config template accordingly
    # !!!! hardcoded search for SSL SST pureRaw to match template file !!!

    if not target_path:
        target_path = raw_input_filepath.split("pureRaw")[0]

    # parse
    if verbose: print(raw_input_filepath)
    inpath = raw_input_filepath.split("_")
    # if verbose: print(len(inpath),inpath)
    date = inpath[1]
    time = inpath[2]
    array_idx = inpath[-1][0]

    tag = "_".join([date,time,array_idx])
    target_path = target_path + "logs"+ array_idx + "/"
    # if verbose: print(target_path, tag)

    def replace_path(lines,keyword):
        # find matching lines
        if "pureRaw" in keyword:
            newpath = raw_input_filepath
            idx = np.where([(keyword in ll) for ll in lines])[0]
        else:
            newpath = "".join([target_path , keyword , "/c" , keyword , "_" , tag , ".log"])
            idx = np.where([(keyword in ll.split("/")[-1]) for ll in lines])[0]

        for ii in idx: # replace path in matching lines
            line = lines[ii].split("\"")
            lines[ii] = "\"".join([line[0], newpath, line[2]])
            if verbose: print(lines[ii])
        return lines, newpath

    with open(template_config_path) as f:
        lines = f.readlines()

    # set paths
    lines, rawpath = replace_path(lines, "pureRaw")
    lines, sslpath = replace_path(lines, "SSL")
    lines, sstpath = replace_path(lines, "SST")

    with open(target_config_path, "w") as f:
        f.writelines(lines)
    return rawpath, sslpath, sstpath


# single file test 
# raw_input_filepath = "/Volumes/ARRAY0/noSST/recordings3/pureRaw/allChannels_2021-09-24_08:30:00_3.raw"
# gen_config(raw_input_filepath,verbose=True);

# test cfg gen for all files
# [gen_config(ff) for ff in raw_files];


for recordedRaw in raw_files:
    if not os.path.isfile(recordedRaw) :
        noFileStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". No Recordings to process yet\n"
        print(noFileStr)
        continue
    try:
        # start odaslive
        startStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Starting odaslive offline \n"
        with open(recordingLog, "a") as f :
            f.write(startStr)
        print(startStr)
        rawpath, sslpath, sstpath = gen_config(
            recordedRaw, 
            target_path          = None, 
            template_config_path = odasConfigTemplate,
            target_config_path   = odasConfigTmp,
            verbose              = False)
        p2 = Popen(["./odaslive", "-vc", odasConfig],
                   cwd="/home/pi/odas/bin",
                   universal_newlines=True,
                   stdout=PIPE)
        p2.wait() # Wait for odaslive to finish
        with open(recordingLog, "a") as f :
            f.write(str(p2.communicate()[0]))
        # print(p2.communicate()[0])

        endStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Odaslive ended \n"
        with open(recordingLog, "a") as f :
            f.write(endStr)
        print(endStr)

        # Retrieve Timestamp
        f = open(recpath + "pureRaw/timeStamp.txt", "r")
        timeArray = f.readline()
        f.close()
        
        # obtain the last access and modified time of raw files
        # atime = os.path.getatime(recordedRaw)
        # mtime = os.path.getmtime(recordedRaw)
        # aT = datetime.fromtimestamp(atime)
        # mT = datetime.fromtimestamp(mtime)
        aT, mT = read_aT_mT(recpath + "arecordLog/aTmT.txt")
        
        date0, time0 = str(aT).split()
        time0 = time0.split('.')[0]
        Popen(["mv", 
            recpath + "arecordLog/aTmT.txt",
            recpath + "arecordLog/" + timeArray + ".txt"])

        timeStr = "Time is " + str(datetime.fromtimestamp(timer.time())) \
            + ". Timestamp " + timeArray + " Retrieved \n"
        with open(recordingLog, "a") as f :
            f.write(timeStr)
        print(timeStr)

        # run odasparsing.py to check if SST.log has empty data
        p3 = Popen(["python3", odaspath+"/python/odasparsing.py"], 
                   stdout=PIPE, 
                   stdin=PIPE, 
                   universal_newlines=True)    
        # flag returns a string that says if the file is or is not useful            
        flag = p3.communicate(input=sstpath)[0].strip()

        emptyStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Checked for useful data \n"
        with open(recordingLog, "a") as f :
            f.write(emptyStr)
        print(emptyStr)
        
        # append recording start time and end time to the end of SST.log and SSL.log
        with open(sstpath, "a") as f:
            f.write("Start time: " + str(aT) + "\n")
            f.write("End time: " + str(mT))
        
        with open(sslpath, "a") as f:
            f.write("Start time: " + str(aT) + "\n")
            f.write("End time: " + str(mT))

        # To support NTFS (since ext is not supported in MacOS)
        timeArray = timeArray.replace(":", "T")

        # Specify Timestamp on Recordings and Log Files
        sepName  = recpath + "separated/separated_" + timeArray + ".raw"
        posName  = recpath + "postfiltered/postfiltered_" + timeArray + ".raw"
        rawName  = recpath + "pureRaw/allChannels_" + timeArray + ".raw"
        
        # upload SST log
        Popen(["rclone","copy",cSSTName,"RaspberryPi:/ODAS/logs"+arrayInd+"/SST"])

        sstStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". SST log successfully uploaded \n"
        with open(recordingLog, "a") as f :
            f.write(sstStr)
        print(sstStr)
        
        # if log file contains no data other than 0, delete raw files 
        key = "not useful"
        if flag == key:
            upRaw = Popen(["cp","-v",rawName,usbLocation+"/ODAS/recordings"+arrayInd+"/pureRaw"],
                stdout=PIPE, stderr=PIPE)
            os.remove(recpath + "/SSL/SSL.log")
            os.remove(recpath + "separated/separated.raw")
            os.remove(recpath + "postfiltered/postfiltered.raw")
            os.remove(recpath + "pureRaw/allChannels.raw")
            rmStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Files has been removed or flushed \n"
            with open(recordingLog, "a") as f :
                f.write(rmStr)
            print(rmStr)
            # print("\n Files has been removed or flushed")
        else:          
            os.rename(recpath + "SSL/SSL.log", cSSLName)
            os.rename(recpath + "separated/separated.raw", sepName)
            os.rename(recpath + "postfiltered/postfiltered.raw", posName)
            os.rename(recpath + "pureRaw/allChannels.raw", rawName)
            # upload SSL, separated, postfiltered, pure raw files
            uploadingStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Starting mv to USB Drive \n"
            with open(recordingLog, "a") as f :
                f.write(uploadingStr)
            print(uploadingStr)
            Popen(["cp","-v",cSSLName,usbLocation+"/ODAS/logs"+arrayInd+"/SSL"])
            Popen(["cp","-v",cSSTName,usbLocation+"/ODAS/logs"+arrayInd+"/SST"])
            Popen(["cp","-v", sepName,usbLocation+"/ODAS/recordings"+arrayInd+"/separated"])
            Popen(["cp","-v", posName,usbLocation+"/ODAS/recordings"+arrayInd+"/postfiltered"])
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
        countdown(5)
                           
    except KeyboardInterrupt:
        p2.send_signal(signal.SIGINT)
        p2.wait()
        interruptStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Interrupted +.+  \n"
        with open(recordingLog, "a") as f :
            f.write(interruptStr)
        print(interruptStr)
        break
