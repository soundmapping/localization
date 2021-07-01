import sys
import glob
import shutil
import os
import datetime

mic_number = sys.argv[1]

str_com_pre = 'rclone deletefile RaspberryPi:ODAS/'
gdrive = "/Users/odas2/Google Drive/My Drive/ODAS/logs"

log_files = glob.glob(gdrive+str(mic_number)+'/SST/*.log')
destination = gdrive + str(mic_number) + '/SST/Processing'

if(not log_files):
    print(datetime.datetime.now(), ", There are no log files to move. Bye!")
    sys.exit()

for i in log_files:
    file_path = i[:i.find('/cSST')] + '/Processing/' + i[i.find('cSST'):]
    try:
        temp = shutil.move(i, destination)
    except shutil.Error:
        print(datetime.datetime.now(), ",", i, "already exists in Processing. Deleting...")
        str_com_post = i[i.find('/logs')+1:]
        del_command = str_com_pre + str_com_post
        print(datetime.datetime.now(),', Deleting file', i, 'using the command', del_command)
        os.system(del_command)
        continue
    # update the env path
    file_path = file_path.replace(' ', '\ ')
    com = '/opt/anaconda3/envs/soundmapping/bin/python3 ~/Desktop/SoundMapping/server/localization/data_uploader.py '+file_path+' >> ~/Desktop/SoundMapping/server/localization/output/data_uploader_out_'+str(mic_number)+'.txt 2>&1'
    val = os.system(com)
    print(datetime.datetime.now(), ',',val)