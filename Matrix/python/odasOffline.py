#!/usr/bin/env python
# coding: utf-8
# By YiHan Hu & Henrry Gunawan

import os
import sys
import time as timer
from datetime import datetime
from subprocess import Popen, PIPE
import signal
import numpy as np
    
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


# recpath is where the script looks for recordings and creates the log folders.
if len(sys.argv) > 1: # check if provided as command line arg
    recpath = sys.argv[1]
    if recpath[-1] == '/':
        recpath = recpath[:-1]
else: 
    # usbLocation  = "".join([usbLocation,"/ARRAY0"])
    # recpath      = usbLocation + "/experiment"
    recpath = "/home/soundmapping/share/test"

FS = 32000
odasConfigTemplate = "./../matrix_creator_offline.cfg" # can be relative
odasConfigTmp = recpath+"/tmp_matrix_creator_offline.cfg" # absolute path needed
recordingLog = "./recording.log"

# find all raw recursively and append in raw_files
raw_files = []
for dirpath, subdirs, files in os.walk(recpath):
    for x in files:
        if x.endswith(".raw") and not np.any([key in x for key in ['postfiltered','separated']]):
            raw_files.append(os.path.join(dirpath, x))
print("found these files in ", recpath)
[print(ff) for ff in raw_files]
print("\n")

def gen_config(
    raw_input_filepath, 
    target_path          = recpath, # destination for log and recording folders
    template_config_path = "./../matrix_creator_offline.cfg",
    target_config_path   = "./tmp_matrix_creator_offline.cfg",
    verbose = False,
    FS = FS,
    ):
    # this function parses identifiers from raw filename, 
    # and replaces the paths in the ODAS config template accordingly
    # !!!! hardcoded search for SSL SST pureRaw to match template file !!!

    # parse
    if verbose: print(raw_input_filepath)
    inpath = raw_input_filepath.split("_")
    # if verbose: print(len(inpath),inpath)
    date = inpath[1]
    time = inpath[2] 
    array_idx = inpath[-1][0]

    tag = "_".join([date,time,array_idx])
    # if verbose: print(target_path, tag)

    def replace_path(lines,keyword):
        # find matching lines
        if "pureRaw" in keyword:
            newpath = raw_input_filepath
            idx = np.where([(keyword in ll) for ll in lines])[0]
        elif keyword in ["SSL", "SST"]:
            newpath = "".join([target_path , "/logs", array_idx , "/", keyword , "/c" , keyword , "_" , tag , ".log"])
            idx = np.where([(keyword in ll.split("/")[-1]) for ll in lines])[0]
        elif keyword in ["separated", "postfiltered"]:
            idx = np.where([(keyword+".raw" in ll.split("/")[-1]) for ll in lines])[0]
            # newpath = "".join([target_path , "/recordings", array_idx , "/", keyword , "/" , keyword , "_" , tag , ".raw"])
            print('gen_config : use dummypath for', keyword) # to save disk space
            newpath = "".join([target_path , "/" , keyword , "_dummy.raw"])

        # gen dir if necessary
        dirname = os.path.dirname(newpath)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

        for ii in idx: # replace path in matching lines
            line = lines[ii].split("\"")
            lines[ii] = "\"".join([line[0], newpath, line[2]])
            if verbose: print(lines[ii])
        return lines, newpath

    with open(template_config_path) as f:
        lines = f.readlines()

    # hardcoded FS set
    lines[9] = "    fS = "+str(FS)+";\n"
    if verbose: print([lines[9]])

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
# raw_input_filepath = "/home/soundmapping/share/test/pureRaw/allChannels_0_0_0.raw"
# gen_config(raw_input_filepath,"/home/soundmapping/share/test/",verbose=True);

# test cfg gen for all files
# [gen_config(ff) for ff in raw_files];


for recordedRaw in raw_files:
    if not os.path.isfile(recordedRaw) :
        noFileStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". No Recordings to process yet\n"
        print(noFileStr)
        continue
    try:
        rawpath, sslpath, sstpath, seppath, pflpath = \
                gen_config(
            recordedRaw, 
            target_path          = recpath + "/", 
            template_config_path = odasConfigTemplate,
            target_config_path   = odasConfigTmp,
            verbose              = False)

        # start odaslive
        startStr = "Time is " + str(datetime.fromtimestamp(timer.time())) \
                + ".  Starting odaslive offline with input \n" \
                + rawpath + "\n"
        with open(recordingLog, "a") as f :
            f.write(startStr)
        print(startStr)
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
        p3 = Popen(["python3", odaspath+"/localization/Matrix/python/odasparsing.py", sstpath], 
                   stdout=PIPE, 
                   stdin=PIPE, 
                   universal_newlines=True)    

        # flag returns a string that says if the file is or is not useful            
        flag = p3.communicate(input=sstpath)[0].strip()
        if flag == "not useful":
            print("Files are not useful")
                           
    except KeyboardInterrupt:
        p2.send_signal(signal.SIGINT)
        p2.wait()
        interruptStr = "Time is " + str(datetime.fromtimestamp(timer.time())) + ". Interrupted +.+  \n"
        with open(recordingLog, "a") as f :
            f.write(interruptStr)
        print(interruptStr)
        break