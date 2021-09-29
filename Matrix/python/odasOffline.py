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
    import getpass
    user = getpass.getuser()
    odaspath = "/home/"+user+"/odas"
    usbLocation  = "/media/"+user
    odasbin = "/home/"+user+"/odas/bin"
elif pf == "darwin": # manu macOS
    odaspath = "/Users/mha/dtu/mpl/odas"
    usbLocation = "/Volumes"
    odasbin = None

usbLocation  = "".join([usbLocation,"/ARRAY0"])
recpath      = usbLocation + "/noSST"
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
            raw_files.append(os.path.join(dirpath, x))
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
        elif keyword in ["SSL", "SST"]:
            newpath = "".join([target_path , keyword , "/c" , keyword , "_" , tag , ".log"])
            idx = np.where([(keyword in ll.split("/")[-1]) for ll in lines])[0]
        elif keyword in ["separated", "postfiltered"]:
            idx = np.where([(keyword+".raw" in ll.split("/")[-1]) for ll in lines])[0]
            newpath = "".join([target_path , keyword , "/" , keyword , "_" , tag , ".raw"])

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
    lines, seppath = replace_path(lines, "separated")
    lines, pflpath = replace_path(lines, "postfiltered")

    with open(target_config_path, "w") as f:
        f.writelines(lines)
    return rawpath, sslpath, sstpath, seppath, pflpath

# single file test 
raw_input_filepath = "/Volumes/ARRAY0/noSST/recordings3/pureRaw/allChannels_2021-09-24_08:30:00_3.raw"
gen_config(raw_input_filepath,verbose=True);

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
        rawpath, sslpath, sstpath, seppath, pflpath = \
                gen_config(
            recordedRaw, 
            target_path          = None, 
            template_config_path = odasConfigTemplate,
            target_config_path   = odasConfigTmp,
            verbose              = False)
        p2 = Popen(["./odaslive", "-vc", odasConfigTmp],
                   cwd=odasbin,
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

        # run odasparsing.py to check if SST.log has empty data
        p3 = Popen(["python3", odaspath+"/localization/Matrix/python/odasparsing.py"], 
                   stdout=PIPE, 
                   stdin=PIPE, 
                   universal_newlines=True)    

        # flag returns a string that says if the file is or is not useful            
        flag = p3.communicate(input=sstpath)[0].strip()
        if flag == "not useful":
            print("Files are not useful")
        
        # append recording start time and end time to the end of SST.log and SSL.log
        with open(sstpath, "a") as f:
            f.write("Start time: " + str(aT) + "\n")
            f.write("End time: " + str(mT))
        
        with open(sslpath, "a") as f:
            f.write("Start time: " + str(aT) + "\n")
            f.write("End time: " + str(mT))

                           
    except KeyboardInterrupt:
        p2.send_signal(signal.SIGINT)
        p2.wait()
        interruptStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Interrupted +.+  \n"
        with open(recordingLog, "a") as f :
            f.write(interruptStr)
        print(interruptStr)
        break
