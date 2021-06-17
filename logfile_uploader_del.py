import glob
import os
import pandas as pd
import re 
import json
import datetime
import time
import shutil
import datetime
from sqlalchemy import create_engine
import sys
from random import randint

# Functions


def append_random_string(filename):
    """Duplicate files are a huge problem. Trying to append a random number before moving."""
    suff = randint(10000000, 99999999)
    suff_str = str(suff)
    base_name = os.path.basename(filename)
    base_name_no_ext = base_name[:-4]
    new_name = base_name_no_ext + suff_str + '.log'
    new_full_name = os.path.join(os.path.dirname(filename),new_name)
    return(new_full_name)


# Extract time information of each recording from the log file
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
        while f.read(1) != b'\n':
            f.seek(-2, 1)
        startTime_line = f.readline().decode()

    return [startTime_line, endTime_line]

# Calculate duration of each recording in microseconds
def durationinMicroseconds(filename):
    startTime = timeExtract(filename)[0].split()[2:]
    endTime = timeExtract(filename)[1].split()[2:]
    startTimeStr = startTime[0] + ' ' + startTime[1]
    endTimeStr = endTime[0] + ' ' + endTime[1]
    T1 = datetime.datetime.strptime(startTimeStr, '%Y-%m-%d %H:%M:%S.%f')
    T2 = datetime.datetime.strptime(endTimeStr, '%Y-%m-%d %H:%M:%S.%f')
    delta = T2-T1
    duration = delta.seconds*1000000 + delta.microseconds
    
    return duration, T1, T2


# Converts .log files into pandas dataframes
def extractDirectionalities(filename, mic_number):
    with open(filename, 'r') as f:
        text = f.read()

        # Use repex to store blocks of data into a list
    data = re.split('(?<=})\n(?={)', text)
    # Delete the time info from the last data block
    tmp = data[-1][:(data[-1].rfind("}") + 1)]
    data[-1] = tmp

    # list of src blocks
    srcList = [json.loads(block)["src"] for block in data]

    # initialize dataframe to have colums: timestamp, time, data inside source
    # timestamp is the initial time stamp
    # time is the datetime value converted from the timestamp and intitial time
    # source is a 4 by 6 array where the rows are the source, and the columns are the source values
    df = pd.DataFrame(
        columns=['Timestamp', 'Time', 'Time In Seconds', 'Microphone Number', 'Source ID_0', 'X_0', 'Y_0', 'Z_0',
                 'Activity_0', 'Source ID_1', 'X_1', 'Y_1', 'Z_1', 'Activity_1', 'Source ID_2', 'X_2', 'Y_2', 'Z_2',
                 'Activity_2', 'Source ID_3', 'X_3', 'Y_3', 'Z_3', 'Activity_3'])

    # Used for calculating timestamps -> time
    duration, startTime, endTime = durationinMicroseconds(filename)
    start_time_in_seconds = time.mktime(startTime.timetuple())
    t = duration / len(data) / 1000000.0

    index = 1.0
    ind = 0
    df_dict = {}
    for block in srcList:
        if block[0]["id"] != 0 or block[1]["id"] != 0 or block[2]["id"] != 0 or block[3]["id"] != 0:
            time_in_seconds = start_time_in_seconds + (index - 1.0) * t
            # for i in range(0, 4):
            #     if block[i]['id'] != 0:
            df_dict[ind] = {"Timestamp": [index], "Time":datetime.datetime.fromtimestamp(time_in_seconds).strftime("%A, %B %d, %Y %I:%M:%S"), "Time In Seconds": time_in_seconds, "Microphone Number":mic_number, "Source ID_0": block[0]["id"], "X_0": block[0]["x"], "Y_0": block[0]["y"], "Z_0": block[0]["z"], "Activity_0": block[0]["activity"], "Source ID_1": block[1]["id"], "X_1": block[1]["x"], "Y_1": block[1]["y"], "Z_1": block[1]["z"], "Activity_1": block[1]["activity"], "Source ID_2": block[2]["id"], "X_2": block[2]["x"], "Y_2": block[2]["y"], "Z_2": block[2]["z"], "Activity_2": block[2]["activity"], "Source ID_3": block[3]["id"], "X_3": block[3]["x"], "Y_3": block[3]["y"], "Z_3": block[3]["z"], "Activity_3": block[3]["activity"]}
            ind = ind + 1

        index = index + 1.0

    df = df.append(pd.DataFrame.from_dict(df_dict, "index"))
    return (df)



newest = sys.argv[1]

mic_number = newest[-5] # given currently used file nomenclature _x.log


destination = "/home/ardelalegre/google-drive/ODAS/logs" + str(mic_number) + "/SST/Processed"
destination2 = '/home/ardelalegre/google-drive/ODAS/logs' + str(mic_number) + '/SST/Duplicates'

str_com_pre = 'rclone deletefile RaspberryPi:ODAS/'

with open(newest, 'r') as f:
        firstline = f.readline()
        if firstline == "SST log contains no useful data\n":
            print(datetime.datetime.now(),', No data in file')
            try:
                temp = shutil.move(newest,destination)
            except:
                print(datetime.datetime.now(),', ',newest, "is a duplicate. Deleting...")
                str_com_post = newest[newest.find('/logs')+1:]
                del_command = str_com_pre + str_com_post
                print(datetime.datetime.now(),', Deleting file', newest, 'using the command', del_command)
                err_num = os.system(del_command)
                if(err_num):
                    print(datetime.datetime.now(), ',' ,err_num, 'was the exit code of the error')
#                 a = append_random_string(newest)
#                 os.rename(newest,a)
#                 temp2 = shutil.move(a, destination2)
            sys.exit()
df = extractDirectionalities(newest, mic_number)
# code to shift notebook to processed directory


# create sqlalchemy engine
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="test",
                               db="odas_db_proc"))

df.to_sql('raw', con = engine, if_exists = 'append', chunksize = 1000)

try:
    temp = shutil.move(newest,destination)
except shutil.Error:
    print(datetime.datetime.now(),', ',newest, "is a duplicate (non-empty). Deleting.")
    str_com_post = newest[newest.find('/logs')+1:]
    del_command = str_com_pre + str_com_post
    print(datetime.datetime.now(),', Deleting file', newest, 'using the command', del_command)
    os.system(del_command)
#     a = append_random_string(newest)
#     os.rename(newest,a)
#     temp2 = shutil.move(a, destination2)

