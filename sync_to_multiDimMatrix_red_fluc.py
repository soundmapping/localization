import csv   
import datetime
import numpy as np
import pandas as pd
from sqlalchemy import create_engine
import time



engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                       .format(user="root",
                               pw="test",
                               db="odas_db_proc"))

INTERVAL = 0.064
THRESHOLD = 0.00385
RAW_TABLE_QUERY = '''
SELECT *, ({2} + ((`Time In Seconds` - {2}) DIV {0}) * {0}) as quantized_time
FROM raw
WHERE `Time In Seconds` >= {2} and `Time In Seconds`< {3}
'''
# RAW_TABLE_QUERY = "SELECT *, ((`Time In Seconds` DIV {0}) * {0}) AS quantized_time from raw where `Time In Seconds` >= {2} and `Time In Seconds`< {3}"
# Might change this later
GROUP_BY_QUERY ='''
INSERT INTO multiDimMatrix
select
  derivedTable.quantized_time,
  sum(case when derivedTable.`Microphone Number` = 0 then derivedTable.X_0 end) / count(case when derivedTable.`Microphone Number` = 0 then derivedTable.X_0 end) as X_0_0,
  sum(case when derivedTable.`Microphone Number` = 0 then derivedTable.Y_0 end) / count(case when derivedTable.`Microphone Number` = 0 then derivedTable.Y_0 end) as Y_0_0,
  sum(case when derivedTable.`Microphone Number` = 0 then derivedTable.Z_0 end) / count(case when derivedTable.`Microphone Number` = 0 then derivedTable.Z_0 end) as Z_0_0,
  sum(case when derivedTable.`Microphone Number` = 1 then derivedTable.X_0 end) / count(case when derivedTable.`Microphone Number` = 1 then derivedTable.X_0 end) as X_0_1,
  sum(case when derivedTable.`Microphone Number` = 1 then derivedTable.Y_0 end) / count(case when derivedTable.`Microphone Number` = 1 then derivedTable.Y_0 end) as Y_0_1,
  sum(case when derivedTable.`Microphone Number` = 1 then derivedTable.Z_0 end) / count(case when derivedTable.`Microphone Number` = 1 then derivedTable.Z_0 end) as Z_0_1,
  sum(case when derivedTable.`Microphone Number` = 2 then derivedTable.X_0 end) / count(case when derivedTable.`Microphone Number` = 2 then derivedTable.X_0 end) as X_0_2,
  sum(case when derivedTable.`Microphone Number` = 2 then derivedTable.Y_0 end) / count(case when derivedTable.`Microphone Number` = 2 then derivedTable.Y_0 end) as Y_0_2,
  sum(case when derivedTable.`Microphone Number` = 2 then derivedTable.Z_0 end) / count(case when derivedTable.`Microphone Number` = 2 then derivedTable.Z_0 end) as Z_0_2,
  sum(case when derivedTable.`Microphone Number` = 3 then derivedTable.X_0 end) / count(case when derivedTable.`Microphone Number` = 3 then derivedTable.X_0 end) as X_0_3,
  sum(case when derivedTable.`Microphone Number` = 3 then derivedTable.Y_0 end) / count(case when derivedTable.`Microphone Number` = 3 then derivedTable.Y_0 end) as Y_0_3,
  sum(case when derivedTable.`Microphone Number` = 3 then derivedTable.Z_0 end) / count(case when derivedTable.`Microphone Number` = 3 then derivedTable.Z_0 end) as Z_0_3,
  sum(case when derivedTable.`Microphone Number` = 4 then derivedTable.X_0 end) / count(case when derivedTable.`Microphone Number` = 4 then derivedTable.X_0 end) as X_0_4,
  sum(case when derivedTable.`Microphone Number` = 4 then derivedTable.Y_0 end) / count(case when derivedTable.`Microphone Number` = 4 then derivedTable.Y_0 end) as Y_0_4,
  sum(case when derivedTable.`Microphone Number` = 4 then derivedTable.Z_0 end) / count(case when derivedTable.`Microphone Number` = 4 then derivedTable.Z_0 end) as Z_0_4,
  sum(case when derivedTable.`Microphone Number` = 5 then derivedTable.X_0 end) / count(case when derivedTable.`Microphone Number` = 5 then derivedTable.X_0 end) as X_0_5,
  sum(case when derivedTable.`Microphone Number` = 5 then derivedTable.Y_0 end) / count(case when derivedTable.`Microphone Number` = 5 then derivedTable.Y_0 end) as Y_0_5,
  sum(case when derivedTable.`Microphone Number` = 5 then derivedTable.Z_0 end) / count(case when derivedTable.`Microphone Number` = 5 then derivedTable.Z_0 end) as Z_0_5
from ({0}) as derivedTable
group by quantized_time
'''

# This function groups a 5-min-long data from 10 mins ago according to timestamp and append it to PCA matrix
def group_by():
    
    nowTimestamp = datetime.datetime.now()
    startTimestamp = datetime.timedelta(minutes = 10)
    endTimestamp = datetime.timedelta(minutes = 5)
    
    start_time = nowTimestamp - startTimestamp
    end_time = nowTimestamp - endTimestamp

    unixtime_start = time.mktime(start_time.timetuple())
    unixtime_end = time.mktime(end_time.timetuple())
    
    query1 = RAW_TABLE_QUERY.format(INTERVAL,THRESHOLD,unixtime_start,unixtime_end) 
    query2 = GROUP_BY_QUERY.format(query1)
    
    tmpData = engine.execute(query2)
    
    
script_start = datetime.datetime.now()
group_by()    
script_end = datetime.datetime.now()
execution_time = script_end - script_start
print('Pushed data successfully at', datetime.datetime.now())
app_list = [script_end, execution_time]

with open(r'/home/ardelalegre/Documents/SQL_AllProc/sync_to_multiDimMatrix_csv.csv', 'a') as f:
    w = csv.writer(f)
    w.writerow(app_list)