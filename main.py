# load modules
import pandas as pd
import time
import datetime
from more_itertools import pairwise

from gap_heap import GapHeap

# log start time
start_time = time.time()

# load input data set (Python pickle file)
df = pd.read_pickle('px.xz')

grouped_df = df.groupby('bbgid', sort=False)['dt'].apply(list).reset_index(name='dates')

gaps = GapHeap()
def find_gaps(row):
  bbgid = row['bbgid']
  dates = row['dates']
  dates.sort()
  for old_date, new_date in pairwise(dates):
    # Treat consecutive days as a gap of 0
    length = (new_date - old_date).days - 1
    if length > 0:
      start = old_date + datetime.timedelta(days=1)
      end = new_date - datetime.timedelta(days=1)
      gaps.add(start, end, length, bbgid)

grouped_df.apply(find_gaps, axis=1)  

# export result to Excel
stats = gaps.to_dataframe()
stats.iloc[0:1000].to_excel('px_stats.xlsx') 

# show execution time
print(f"--- {time.time() - start_time} seconds ---")