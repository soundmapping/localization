import os
import sys

import subprocess as p

arrayNum = "2"
gdrive = "/Volumes/GoogleDrive/My Drive/ODAS/logs"
desktopDir = "/Users/odas2/Desktop/ODAS_USB"
usbDir = "/Volumes/ARRAY" + str(arrayNum) + "/ODAS"
# usbDir = "/Volumes/ARRAY1/ODAS"

for root, dirs, files in os.walk(usbDir, topdown=False):
    rootSplit = root.split("/")
    print("rootSplit = ", rootSplit)
    if rootSplit[-1] is "ODAS" :
        break
    p.run(["mkdir", rootSplit[-2]], cwd=desktopDir)
    p.run(["mkdir", rootSplit[-1]], cwd=os.path.join(desktopDir, rootSplit[-2]))
    print("Now in Directory: ", rootSplit[-1])
    for name in files:
    #    print(os.path.join(root, name))
    #    print(" For name: ", name)
    #    print("   For root: ", root)
    #    print("     Root split: ", root.split("/"))
    #    print("      New name: ", name.replace("T", ":"))
    #    rootSplit = root.split("/")
        
        oldFile = os.path.join(root, name)
        newDir = desktopDir + "/" + rootSplit[-2] + "/" + rootSplit[-1] + "/"
        if rootSplit[-1] == "SST" :
            newFile = os.path.join(newDir, name.replace("T", ":").replace(":", "T", 1))
        else :
            newFile = os.path.join(newDir, name.replace("T", ":"))
        print("Source File: ", oldFile)
        print("    Moving into: ", newFile)
        p.run(["cp", "-v", oldFile, newFile])
#    for name in dirs:
#       print(os.path.join(root, name))
