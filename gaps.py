from collections import namedtuple
from heapq import heappush, nlargest, heapreplace
from pandas import DataFrame

# Maximum number of records stored
MAXIMUM_RECORDS = 1000

# Named tuple that mimics the final columns of the output
Gap = namedtuple('Gap', ['start', 'end', 'length', 'bbgid'])

# Class for storing the top 1000 length gaps
class Gaps:
  def __init__(self):
    self.gap_heap = []

  def add(self, start, end, length, bbgid):
    # First item is the heap priority
    item = (length, Gap(start=start, end=end, length=length, bbgid=bbgid))

    if len(self.gap_heap) == MAXIMUM_RECORDS and length > self.gap_heap[0][0]:
      # heappushpop always removes the smallest item, meaning that we will always have the largest gaps
      heapreplace(self.gap_heap, item)
    else:
      heappush(self.gap_heap, item)

  def to_dataframe(self):
    gap_list = [item[1] for item in nlargest(MAXIMUM_RECORDS, self.gap_heap)]
    return DataFrame(gap_list)