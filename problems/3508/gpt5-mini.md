# [Problem 3508: Implement Router](https://leetcode.com/problems/implement-router/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need a Router that supports:
- addPacket(source, destination, timestamp) with duplicate detection and an eviction policy (oldest packet removed when capacity exceeded),
- forwardPacket() to return and remove the oldest packet (FIFO),
- getCount(destination, startTime, endTime) to count currently stored packets for a destination in a timestamp interval.

Observations:
- addPacket calls come in non-decreasing timestamp order. This is important: for each destination, timestamps of appended packets will be non-decreasing, so per-destination timestamp lists are sorted.
- FIFO queue of packets can be implemented with a deque.
- Duplicate detection needs a set of triples (source, destination, timestamp).
- For getCount we need to count timestamps in a sorted list -> use binary search (bisect).
- Removing the oldest packet (either by forwardPacket or eviction when adding) corresponds to removing the earliest entry for that packet's destination as well. Because arrival order is non-decreasing timestamps and we record per-destination arrivals in the same order, the packet we remove must be at the front among that destination's list. So we can maintain per-destination lists and a logical start index to support O(1) removals from the front and O(log n) count queries via bisect with lo offset.

## Refining the problem, round 2 thoughts
Data structures:
- deque for global FIFO queue of packet triples.
- set for duplicates.
- dict dest -> list of timestamps (append-only, sorted).
- dict dest -> start_index: logical front index for that destination (so popping front is just incrementing start_index).
- For getCount we perform bisect on dest list with lo = start_index.
- When a dest list becomes empty (start_index == len(list)), we can delete the entries to free memory.

Complexities:
- addPacket: O(1) average for set check + O(1) append + possible O(1) eviction. So O(1).
- forwardPacket: O(1).
- getCount: O(log k) where k is number of packets for that destination (only those still stored + those logically removed that remain in the list but accounted by start_index).

Edge cases:
- Duplicate attempts should not change stored state.
- When evicting a packet, remember to remove it from the duplicates set and increment that destination's start index.
- Ensure bisect is called with lo parameter equal to start_index to ignore logically removed timestamps.

## Attempted solution(s)
```python
import collections
from bisect import bisect_left, bisect_right
from collections import defaultdict, deque

class Router:
    def __init__(self, memoryLimit: int):
        self.limit = memoryLimit
        self.q = deque()               # global FIFO queue of (source, destination, timestamp)
        self.seen = set()              # set of (source, destination, timestamp) currently stored
        self.dest_times = defaultdict(list)  # destination -> list of timestamps (non-decreasing)
        self.start_idx = {}            # destination -> logical start index (front) in dest_times[destination]

    def addPacket(self, source: int, destination: int, timestamp: int) -> bool:
        key = (source, destination, timestamp)
        if key in self.seen:
            return False

        # Add packet
        self.seen.add(key)
        self.q.append(key)
        self.dest_times[destination].append(timestamp)
        # ensure start index exists (default 0)
        if destination not in self.start_idx:
            self.start_idx[destination] = 0

        # Evict oldest if over memory limit
        if len(self.q) > self.limit:
            old = self.q.popleft()
            # remove from seen
            self.seen.remove(old)
            _, old_dest, old_ts = old
            # advance logical start index for that destination
            idx = self.start_idx.get(old_dest, 0)
            # It's safe to assume dest_times[old_dest][idx] == old_ts under the problem's ordered-add constraints
            self.start_idx[old_dest] = idx + 1
            # cleanup if this destination has no more stored packets
            if self.start_idx[old_dest] >= len(self.dest_times[old_dest]):
                del self.dest_times[old_dest]
                del self.start_idx[old_dest]

        return True

    def forwardPacket(self):
        if not self.q:
            return []
        p = self.q.popleft()
        # remove from seen
        self.seen.remove(p)
        src, dest, ts = p
        # advance logical start for the destination
        idx = self.start_idx.get(dest, 0)
        self.start_idx[dest] = idx + 1
        if self.start_idx[dest] >= len(self.dest_times[dest]):
            del self.dest_times[dest]
            del self.start_idx[dest]
        return [src, dest, ts]

    def getCount(self, destination: int, startTime: int, endTime: int) -> int:
        if destination not in self.dest_times:
            return 0
        arr = self.dest_times[destination]
        lo = self.start_idx.get(destination, 0)
        # arr[lo:] is sorted; find indices within [startTime, endTime]
        left = bisect_left(arr, startTime, lo=lo)
        right = bisect_right(arr, endTime, lo=lo)
        return right - left
```

- Notes about approach:
  - We maintain global FIFO with deque so forward/ejection are O(1).
  - Duplicate detection via a set of triples.
  - Per-destination timestamps are appended in non-decreasing order thanks to the guarantee on addPacket timestamps; that enables binary search.
  - To avoid costly pops from the front of per-destination lists, we keep a start index per destination and use bisect with lo=start_index.
  - We clean up per-destination data when the logical start reaches the list length.

- Complexity:
  - addPacket: O(1) average (set check, append, possible O(1) eviction).
  - forwardPacket: O(1).
  - getCount: O(log k) where k is the number of timestamps stored for that destination (binary searches).
  - Space: O(n) where n is current number of stored packets plus some overhead for logically-deleted timestamps not yet physically removed; overall bounded by O(total ops) which is <= 1e5 per constraints.