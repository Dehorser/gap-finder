# load modules
import pandas as pd
import time
import datetime
from gaps import Gaps

# log start time
start_time = time.time()

# load input data set (Python pickle file)
df = pd.read_pickle('px.xz')

# Dataframe needs to be sorted from earliest to latest
sorted_df = df.sort_values('dt')

last_seen = {}
gaps = Gaps()

for _, row in df.iterrows():
  bbgid = row['bbgid']
  date = row['dt']

  # If we have seen this id before, we can compare to when it was last seen to see if there were any gaps
  if bbgid in last_seen:
    length = (date - last_seen[bbgid]).days

    # We'd expect to see a gap of one day between consecutive records
    if length > 1:

      # It's cheaper to store all the data as a list of lists, and then convert into a dataframe
      # Rather than create a dataframe and append row by row
      gaps.add(start=last_seen[bbgid], end=date, length=length, bbgid=bbgid)
    
  last_seen[bbgid] = date

# export result to Excel
stats = gaps.to_dataframe()
stats.iloc[0:1000].to_excel('px_stats.xlsx') 

# show execution time
print(f"--- {time.time() - start_time} seconds ---")