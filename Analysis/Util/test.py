import sqlalchemy
db_engine = sqlalchemy.create_engine("mysql+pymysql://soundmapping:odasodas@soundmapping.local/soundmapping")
print(db_engine)
query1_str = "SELECT * FROM soundmapping.multiDimMatrix5 WHERE quantized_time >= 1624564818"
query1 = db_engine.execute(query1_str)
dataPoints = query1.fetchall()

import pandas
import pandas as pd
import numpy as np
df = pd.DataFrame(dataPoints)
df.columns = dataPoints[0].keys()
df.fillna(value=np.nan)

# from .. import tools
from Tools import *
strTime_to_unixTime("Jun 24 2021 12:05PM", "Jun 24 2021 12:10PM")
strTime_to_unixTime("Jun 24 2021 12:20PM", "Jun 24 2021 12:22PM")
print(df[99:100]["quantized_time"])
print(type(df[99:100]["quantized_time"]))
# df[:100]["quantized_time"].to_numpy()
x = df[:100]["quantized_time"].to_numpy()
import datetime
FORMAT_TIMESTRING = '%b %d %Y %I:%M%p'
# datetime.datetime.utcfromtimestamp(1624564832).strftime('%Y-%m-%dT%H:%M:%SZ')
# datetime.datetime.utcfromtimestamp(x[0]).strftime('%Y-%m-%dT%H:%M:%SZ')
x = df[:]["quantized_time"].to_numpy()
tester = datetime.datetime.utcfromtimestamp(x[1000]).strftime('%Y-%m-%dT%H:%M:%SZ')
print(tester)
# datetime.datetime.utcfromtimestamp(x[10000]).strftime('%Y-%m-%dT%H:%M:%SZ')
# datetime.datetime.utcfromtimestamp(x[5000]).strftime('%Y-%m-%dT%H:%M:%SZ')
# datetime.datetime.fromtimestamp(x[5000]).strftime('%Y-%m-%dT%H:%M:%SZ')
# datetime.datetime.fromtimestamp(x[0]).strftime('%Y-%m-%dT%H:%M:%SZ')