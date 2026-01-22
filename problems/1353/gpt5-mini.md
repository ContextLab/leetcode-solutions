# [Problem 1353: Maximum Number of Events That Can Be Attended](https://leetcode.com/problems/maximum-number-of-events-that-can-be-attended/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We want to attend as many events as possible where each event is an interval [start, end] and we can attend at most one event per day. This suggests a greedy strategy: whenever we pick an event to attend on a given day, we should prefer the event that ends the earliest (so it blocks future days the least). That points to an "earliest end first" greedy, and to efficiently choose the event with the smallest end among currently available events we can use a min-heap keyed by end day.

We also need to consider which events are currently available on a particular day. If we iterate day-by-day and add all events whose start <= current day into the heap, we can then pop expired events (end < day) and attend one event (pop the smallest end). To avoid iterating over days that have no events, we can jump the current day forward to the next event's start when the heap is empty.

Sorting the events by start day first makes it easy to add events into the heap as we advance days.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- Multiple events can have identical start and/or end days — we must push all with start <= day into the heap.
- Events that already expired (end < day) should be popped/discarded from the heap before attempting to attend.
- If the heap is empty and there are remaining events, we can jump the current day to the next event's start day rather than incrementing day one by one.
- Complexity: sorting costs O(n log n). Each event gets pushed and popped at most once from the heap, so heap operations cost O(n log n) overall. The day pointer increases at most until the maximum end day (but because of the jump optimization, we won't iterate unnecessarily).
- Constraints allow up to 1e5 events and days up to 1e5, so the approach is efficient.

Alternative approaches: Another valid approach is to iterate day-by-day explicitly up to the maximum end day, but the heap-with-jump method is more efficient when there are gaps.

## Attempted solution(s)
```python
import heapq
from typing import List

class Solution:
    def maxEvents(self, events: List[List[int]]) -> int:
        # Sort events by start day
        events.sort(key=lambda x: x[0])
        n = len(events)
        i = 0  # pointer into events
        day = 0
        attended = 0
        min_heap = []  # will store end days of events currently available

        while i < n or min_heap:
            # If no available events, jump day to the next event's start
            if not min_heap and i < n:
                day = max(day, events[i][0])

            # Add all events that start on or before current day
            while i < n and events[i][0] <= day:
                heapq.heappush(min_heap, events[i][1])
                i += 1

            # Remove events that have already ended before current day
            while min_heap and min_heap[0] < day:
                heapq.heappop(min_heap)

            # Attend the event that ends the earliest (if any)
            if min_heap:
                heapq.heappop(min_heap)
                attended += 1
                day += 1  # move to next day after attending
            # else: loop will either add events or break if none left

        return attended
```
- Approach: Sort events by start day, iterate days while maintaining a min-heap of end days for events available on the current day. Always attend the available event with the earliest end day. If no event is available, jump to the next event's start.
- Time complexity: O(n log n) due to sorting and heap operations (each event pushed and popped at most once).
- Space complexity: O(n) for the heap in the worst case.
- Implementation details: We ensure expired events (end < day) are discarded before attending. The "jump day" optimization avoids scanning empty days unnecessarily.