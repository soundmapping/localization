import sys
import glob
import shutil
import os
import datetime
# from random import randint


# def append_random_string(filename):
#     """Duplicate files are a huge problem. Trying to append a random number before moving."""
#     suff = randint(10000000, 99999999)
#     suff_str = str(suff)
#     base_name = os.path.basename(filename)
#     base_name_no_ext = base_name[:-4]
#     new_name = base_name_no_ext + suff_str + '.log'
#     new_full_name = os.path.join(os.path.dirname(filename),new_name)
#     return(new_full_name)


mic_number = sys.argv[1]

str_com_pre = 'rclone deletefile RaspberryPi:ODAS/'


log_files = glob.glob('/home/ardelalegre/google-drive/ODAS/logs' + str(mic_number) + '/SST/*.log')
destination = '/home/ardelalegre/google-drive/ODAS/logs' + str(mic_number) + '/SST/Processing'
# destination2 = '/home/ardelalegre/google-drive/ODAS/logs' + str(mic_number) + '/SST/Duplicates'
if(not log_files):
    print(datetime.datetime.now(), ", There are no log files to move. Bye!")
    sys.exit()

for i in log_files:
#     print(i)
    new_sk = i[:i.find('/cSST')] + '/Processing/' + i[i.find('cSST'):]
    try:
        temp = shutil.move(i, destination)
    except shutil.Error:
        print(datetime.datetime.now(), ",", i, "already exists in Processing. Deleting...")
        str_com_post = i[i.find('/logs')+1:]
        del_command = str_com_pre + str_com_post
        print(datetime.datetime.now(),', Deleting file', i, 'using the command', del_command)
        os.system(del_command)
        continue
        
        
        
#         a = append_random_string(i)
#         try:
#             os.rename(i,a)
#             temp2 = shutil.move(a, destination2)
#         except FileNotFoundError:
#             continue
#         continue
#         print(i, "might be duplicate. Moving to Duplicates folder.")
#         try:
#             temp2 = shutil.move(i, destination2)
#         except shutil.Error:
#             print(i, "already exists in Duplicates, so we are renaming it.")
#             a = append_random_string(i)
#             os.rename(i,a)
#             temp2 = shutil.move(a, destination2)
#         continue


    com = 'python3 /home/ardelalegre/Documents/SQL_AllProc/logfile_uploader_del.py '+ new_sk + ' >> /home/ardelalegre/Documents/SQL_AllProc/logfile_uploader_out_'+str(mic_number)+'.txt 2>&1'
    val = os.system(com)
    print(datetime.datetime.now(), ',',val)