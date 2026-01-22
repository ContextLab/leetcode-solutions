# [Problem 1942: The Number of the Smallest Unoccupied Chair](https://leetcode.com/problems/the-number-of-the-smallest-unoccupied-chair/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share internal stream-of-consciousness reasoning, but here is a concise summary of the intended approach:

- Sort friends by arrival time (keep their original index).
- Maintain two min-heaps:
  - available chairs (min-heap of chair indices) to always pick the smallest free chair,
  - occupied chairs (min-heap of (leave_time, chair_index)) to free chairs when friends leave.
- For each arriving friend (in arrival order), free all chairs whose leave_time <= arrival time, then assign either the smallest available chair or the next new chair index. If this friend is the target, return the assigned chair.

## Refining the problem, round 2 thoughts
Again, I won’t provide iterative inner monologue, but here are refinements, edge-cases and complexity considerations:

- Edge cases: When a friend leaves at the same time another arrives, the chair must be considered free for that arrival (free when leave_time <= arrival).
- Arrival times are distinct so sorting is straightforward.
- Time complexity: O(n log n) due to sorting and heap operations.
- Space complexity: O(n) for heaps and bookkeeping.

Implementing this precisely with Python's heapq yields a clean and efficient solution.

## Attempted solution(s)
```python
import heapq
from typing import List

class Solution:
    def smallestChair(self, times: List[List[int]], targetFriend: int) -> int:
        # Annotate each friend with their original index and sort by arrival time
        people = sorted([(arr, leave, i) for i, (arr, leave) in enumerate(times)], key=lambda x: x[0])
        
        available = []  # min-heap of free chair indices
        occupied = []   # min-heap of (leave_time, chair_index)
        next_chair = 0  # next new chair index to use if none available
        
        for arr, leave, idx in people:
            # Free chairs for friends who have already left by this arrival time
            while occupied and occupied[0][0] <= arr:
                leave_time, chair_idx = heapq.heappop(occupied)
                heapq.heappush(available, chair_idx)
            
            # Assign a chair
            if available:
                chair = heapq.heappop(available)
            else:
                chair = next_chair
                next_chair += 1
            
            # If this is the target friend, return the chair number
            if idx == targetFriend:
                return chair
            
            # Mark this chair as occupied until 'leave'
            heapq.heappush(occupied, (leave, chair))
        
        # Should never reach here as targetFriend is guaranteed to be in times
        return -1
```
- Notes about the solution:
  - We process friends in increasing arrival order, freeing chairs whose leave_time <= current arrival so chairs freed at the same time as an arrival are available.
  - available is a min-heap to always pick the smallest-numbered free chair.
  - occupied is a min-heap keyed by leave time to efficiently free chairs as time progresses.
  - Complexity: Sorting takes O(n log n). For each of n friends we do heap operations that cost O(log n), so overall O(n log n) time. Space is O(n).