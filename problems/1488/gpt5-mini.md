# [Problem 1488: Avoid Flood in The City](https://leetcode.com/problems/avoid-flood-in-the-city/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to avoid raining on a lake that's already full. On days with 0 I can dry one lake. The challenge is to decide which lake to dry on each 0 day so that no full lake gets rained on again before it was dried.

A straightforward idea: whenever a lake rains, record the day. For a later rain on the same lake, we must have chosen some zero-day between those two rains to dry that lake. So for each rain occurrence we need to match it with some future zero-day before its next occurrence. This is a matching problem between "next rain deadlines" and available zero days.

Two common approaches come to mind:
- Maintain a sorted set (TreeSet) of zero-day indices and for each rain check the smallest zero-day strictly after its previous rain (use bisect). Python lacks a native TreeSet, but we can simulate with a sorted list and bisect (but deletes are O(n)).
- Greedy + heap: precompute the positions of future rains for each lake. When a lake rains, push the index of its next rain (if any) into a min-heap (the earlier the next rain, the higher the priority to dry that lake). On a zero-day, pop the heap to dry the lake whose next rain is soonest. Also track which lakes are currently full to detect unavoidable floods.

The heap-based greedy looks clean and efficient (O(n log n)) and avoids costly deletions from the middle of arrays.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- Precompute for each lake a queue (deque) of indices where it rains. When processing index i for lake x, pop i from the deque; if there is a next index for x, push that next index into a min-heap keyed by the next occurrence.
- Maintain a set of currently full lakes. If it rains on lake x and x is already in the full set -> impossible (return []).
- On a zero-day: if heap non-empty, pop (nextIndex, lake) and dry that lake (remove from full set); otherwise pick any lake (e.g., 1) to dry (drying an empty lake is allowed).
- Complexity: building position lists O(n), iterating O(n) with heap operations O(log n) each -> overall O(n log n) time, O(n) space.
- Be careful: when pushing into heap we push (nextIndex, lake). The heap element always corresponds to a lake that is currently full at insertion time, and the heap entry will be popped exactly when we decide to dry it. There are no stale entries because we only dry lakes via popping the heap, and we only ever push one next-occurrence entry per rain occurrence.

Now implement the described solution.

## Attempted solution(s)
```python
from collections import defaultdict, deque
import heapq

class Solution:
    def avoidFlood(self, rains):
        n = len(rains)
        # Precompute positions for each lake
        pos = defaultdict(deque)
        for i, lake in enumerate(rains):
            if lake > 0:
                pos[lake].append(i)

        ans = [1] * n  # default for zero-days (1 is arbitrary valid lake to dry)
        full = set()   # lakes that are currently full
        heap = []      # min-heap of (next_rain_index, lake)

        for i, lake in enumerate(rains):
            if lake > 0:
                # It's raining on 'lake' today
                ans[i] = -1
                # Remove this occurrence from its queue
                pos[lake].popleft()
                # If the lake is already full => flood
                if lake in full:
                    return []
                # Mark lake as full
                full.add(lake)
                # If there's a next rain for this lake, push that next index as a deadline
                if pos[lake]:
                    next_idx = pos[lake][0]
                    heapq.heappush(heap, (next_idx, lake))
            else:
                # Dry day: pick the lake whose next rain is earliest (if any)
                if heap:
                    next_idx, lake_to_dry = heapq.heappop(heap)
                    ans[i] = lake_to_dry
                    # Dry it -> remove from full set
                    if lake_to_dry in full:
                        full.remove(lake_to_dry)
                else:
                    # No urgent lake to dry; dry arbitrary lake (1)
                    ans[i] = 1
        return ans
```
- Notes about the approach:
  - We precompute all rain indices for each lake using a deque to efficiently get the next occurrence.
  - When processing a rain on lake x, we check if x is already full (then return []), otherwise mark it full and, if it has a next rain index, push that (next_index, x) into a min-heap. The heap orders lakes by the earliest upcoming rain; these are the ones that must be dried first.
  - On a dry day, we pop the heap to dry the lake with the nearest next rain, ensuring we avoid its flood. If the heap is empty, we dry any arbitrary lake (drying an empty lake is allowed).
  - Time complexity: O(n log n) due to heap operations.
  - Space complexity: O(n) for position deques, heap, and auxiliary structures.