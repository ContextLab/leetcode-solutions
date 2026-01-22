# [Problem 1298: Maximum Candies You Can Get from Boxes](https://leetcode.com/problems/maximum-candies-you-can-get-from-boxes/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are given boxes that may be open or closed, each contains candies, keys to other boxes, and possibly more boxes. We also start with some initial boxes. We can take candies from any open box, use keys found to open boxes, and use boxes found inside open boxes.

This feels like a graph / BFS-like exploration problem where the state is "which boxes we currently have" and "which keys we have". When we can open a box (either initially open or we have its key), we should open it, collect candies, add its keys and contained boxes to our possessions. We repeat until we cannot open any more boxes.

We need to avoid opening the same box multiple times, and we need to revisit boxes we already have if we later obtain keys for them. So maintain sets: available boxes we own, keys we have, and opened boxes. Iteratively open any available box that is open or for which we have a key until no new openings occur.

## Refining the problem, round 2 thoughts
- Keep a set "available" of boxes we currently have (initialBoxes plus boxes found inside opened boxes).
- Keep a set "keys" for keys we've obtained.
- Keep a set "opened" to ensure each box is processed only once.
- While we can open at least one new box from available, open them, collect candies, add their keys to keys, add their contained boxes to available.
- Terminate when no available-but-closable box exists.
- Complexity: each box is opened at most once, and we process each key and contained edge at most once. With n up to 1000, iterating available set repeatedly is fine. A more optimized approach uses a queue and dynamic revisit when new keys arrive, but a simple loop with sets is clear and correct.
- Edge cases: initialBoxes empty -> result 0. Boxes may contain keys to boxes we don't have yet; we should still record keys since when we later get those boxes we can open them.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def maxCandies(self, status: List[int], candies: List[int],
                   keys: List[List[int]], containedBoxes: List[List[int]],
                   initialBoxes: List[int]) -> int:
        # available boxes we currently have (may be open or closed)
        available = set(initialBoxes)
        # keys we have collected
        have_keys = set()
        # boxes we've already opened and collected candies from
        opened = set()
        total = 0

        # Keep looping until no new box can be opened in an iteration
        while True:
            opened_this_round = []
            # find any box in available that can be opened now and isn't opened before
            for b in list(available):
                if b in opened:
                    continue
                if status[b] == 1 or b in have_keys:
                    opened_this_round.append(b)

            if not opened_this_round:
                break

            # open them and collect resources
            for b in opened_this_round:
                if b in opened:
                    continue
                opened.add(b)
                total += candies[b]
                # collect keys found in box b
                for k in keys[b]:
                    if k not in have_keys:
                        have_keys.add(k)
                # collect boxes found inside box b
                for nb in containedBoxes[b]:
                    if nb not in available:
                        available.add(nb)

        return total
```
- Notes:
  - Approach: maintain sets for available boxes, keys, and opened boxes. Repeatedly open any available box that is open or for which we have a key. When opening, add candies, keys, and contained boxes. Stop when no new boxes can be opened.
  - Time complexity: O(n + E) where E is the total number of entries across keys and containedBoxes. Each box is opened at most once and each key/contained-box edge is processed when its source box is opened. The outer loop can run up to O(n) iterations but overall work across iterations remains O(n + E). With n <= 1000 this is efficient.
  - Space complexity: O(n + E) for storing sets and to represent keys/containedBoxes input (input already holds them).