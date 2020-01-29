# load modules
import pandas as pd
import time
import datetime
from more_itertools import pairwise

# log start time
start_time = time.time()

# load input data set (Python pickle file)
df = pd.read_pickle('px.xz')

grouped_df = df.groupby('bbgid', sort=False)['dt'].apply(list).reset_index(name='dates')

def foo(row):
  bbgid = row['bbgid']
  dates = row['dates']
  dates.sort()
  for old_date, new_date in pairwise(dates):
    length = (new_date - old_date).days
    if length > 1:
      start = old_date + datetime.timedelta(days=1)
      end = new_date - datetime.timedelta(days=1)
      gaps.append([start, end, length, bbgid])

gaps = []
grouped_df.apply(foo, axis=1)  

# export result to Excel
stats = pd.DataFrame(gaps, columns=['start', 'end', 'length', 'bbgid']).sort_values('length', ascending=False)
stats.iloc[0:1000].to_excel('px_stats.xlsx') 

# show execution time
print(f"--- {time.time() - start_time} seconds ---")