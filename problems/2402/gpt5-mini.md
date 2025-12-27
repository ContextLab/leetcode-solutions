# [Problem 2402: Meeting Rooms III](https://leetcode.com/problems/meeting-rooms-iii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- We need to allocate meetings to rooms 0..n-1 following the given rules. The meetings have unique start times; it's natural to sort by start time (or use the given unique starts to process in increasing start).
- At any meeting start time s, some rooms might already be free (their meeting end <= s). We should track free rooms and busy rooms. A min-heap of free room indices (so we always pick the smallest available room id) and a min-heap of busy rooms keyed by end time (and then room id to break ties) is a common design.
- If there is a free room at meeting start s, assign the lowest-numbered free room and schedule it to end at the meeting's end.
- If no free room exists at start s, the meeting must be delayed until the earliest busy room frees. We should pop the earliest finishing busy room (end_time, room), compute the delayed meeting's new end = end_time + duration, and assign it to that room. Because meetings are processed in original start order, delayed meetings will be considered in the correct priority order (earlier original start first).
- Maintain counts per room; at the end, return the room with the highest count (ties broken by lowest index).

## Refining the problem, round 2 thoughts
- Edge cases: n = 1, many meetings — all will be sequentially delayed; algorithm must correctly compute new end times.
- Need to be careful about tie-breaking when multiple rooms finish at the same time: using a busy heap keyed by (end_time, room_id) ensures that when multiple rooms free simultaneously the popped room is the one with the smallest id, which matches the rule about choosing the smallest-numbered unused room.
- Complexity: each meeting triggers at most a constant number of heap operations on heaps of size at most n (n <= 100), so overall time is O(m log n) where m = len(meetings). Space O(n) for heaps and counts.
- Implementation detail: sort meetings by start. For each meeting (s, e):
  - Release any busy rooms with end_time <= s into the free heap.
  - If free not empty: pop smallest room, assign, push (e, room) into busy, increment count.
  - Else: pop earliest busy (end, room), compute new_end = end + (e - s), assign, push (new_end, room) back, increment count.
- Finally, pick the room with maximum count (tie -> smallest index).

## Attempted solution(s)
```python
import heapq
from typing import List

class Solution:
    def mostBooked(self, n: int, meetings: List[List[int]]) -> int:
        # Sort meetings by original start time
        meetings.sort(key=lambda x: x[0])
        
        # Free rooms min-heap by room index
        free_rooms = list(range(n))
        heapq.heapify(free_rooms)
        
        # Busy rooms min-heap by (end_time, room_index)
        busy = []
        
        # Count of meetings per room
        counts = [0] * n
        
        for s, e in meetings:
            # Free any rooms that have finished by time s
            while busy and busy[0][0] <= s:
                end_time, room = heapq.heappop(busy)
                heapq.heappush(free_rooms, room)
            
            duration = e - s
            if free_rooms:
                # assign lowest-numbered free room
                room = heapq.heappop(free_rooms)
                counts[room] += 1
                heapq.heappush(busy, (e, room))
            else:
                # no free rooms: delay until earliest room frees
                end_time, room = heapq.heappop(busy)
                # meeting starts at end_time and lasts 'duration'
                new_end = end_time + duration
                counts[room] += 1
                heapq.heappush(busy, (new_end, room))
        
        # find room with highest count (tie -> lowest index)
        best_room = 0
        for i in range(1, n):
            if counts[i] > counts[best_room]:
                best_room = i
        return best_room
```
- Notes:
  - Approach: sort by start time, use two heaps: free_rooms (min room index) and busy (min end time, then room index). For each meeting free any rooms that have finished by its start, otherwise delay by popping earliest busy room and scheduling the meeting to start at that end time.
  - Complexity: Time O(m log n) where m = number of meetings and n <= 100 (heap ops cost log n). Space O(n) for the heaps and counts.
  - Important detail: busy heap stores tuples (end_time, room) so when multiple rooms free at the same end time, the one with smaller room id is popped first (tie-breaker), which matches requirement to use the smallest-numbered unused room. The processing order (sorted original starts) ensures delayed meetings are awarded rooms in order of original start times.