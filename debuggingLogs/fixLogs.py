import os
import sys

def timeExtract(filename):
    with open(filename, 'rb') as f:
        # Start counting from the last byte
        counter = 1
        # Go to the 2nd byte before the end of the last line
        f.seek(-2, 2) 
        while f.read(1) != b'\n':
            f.seek(-2, 1)
            counter=counter+1
        endTime_line = f.readline().decode()

        # Go to the 2nd byte before the end of the last second line
        f.seek(-counter-2, 2)
        # To accomadate accidental nextline in log files:
        if f.readline() == b'\n' :
            print("Only White Space: ", f.readline())
            f.seek(-counter-3, 2)
            print("\n Moving into prev line")
        else : # Necessary because readline() was invoked (needs to be repointed)
            f.seek(-counter-2,2) 
        
        while f.read(1) != b'\n':
            f.seek(-2, 1)
        startTime_line = f.readline().decode()

    return [startTime_line, endTime_line]

origDir = "/Users/odas2/Desktop/29Sept2021"
destDir = "/Users/odas2/Desktop/logs_32kHz"

for arrayNum in range(8) :
    origArray = origDir + "/logs" + str(arrayNum) + "/SST"
    destArray = destDir + "/logs" + str(arrayNum) + "/SST"

    for root, dirs, files in os.walk(origArray, topdown=False):
        for name in files :
            origFilename = os.path.join(origArray, name)
            destFilename = os.path.join(destArray, name)
            try :
                [startTime_line, endTime_line] = timeExtract(origFilename)
                timeString = "\n" + startTime_line + "\n" + endTime_line
                with open(destFilename, "a") as f :
                    f.write(timeString)

            except :
                print("Error in: ", origFilename)
                continue