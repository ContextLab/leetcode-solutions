# [Problem 2515: Shortest Distance to Target String in a Circular Array](https://leetcode.com/problems/shortest-distance-to-target-string-in-a-circular-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is a circular array, so distances wrap around. Starting at startIndex you can move left or right with cost 1 per step. The target may appear multiple times; we want the minimum number of steps to any occurrence. My first thought: we could do BFS from startIndex, but that's overkill because the array is small and unweighted — essentially the shortest distance to an index i is just the minimum of clockwise and counterclockwise steps. So find all indices where words[i] == target and compute the minimal circular distance to startIndex (using modular arithmetic). If no occurrence, return -1.

## Refining the problem, round 2 thoughts
Edge cases:
- target equals words[startIndex] -> distance 0.
- multiple occurrences -> choose the closest by either direction.
- startIndex near ends -> circular wrap must be handled correctly.

Two ways:
- Scan all indices and compute min of min((i-start)%n, (start-i)%n).
- Or expand outward from startIndex checking left/right simultaneously until find target (this would also be O(n) worst-case).

Time complexity should be O(n), space O(1). n <= 100 so either approach is trivial. I'll implement the direct scan with modular distance computation for clarity.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def closetTarget(self, words: List[str], target: str, startIndex: int) -> int:
        n = len(words)
        best = float('inf')
        for i, w in enumerate(words):
            if w == target:
                # clockwise distance from startIndex to i
                clockwise = (i - startIndex) % n
                # counterclockwise distance is the other direction
                counterclockwise = (startIndex - i) % n
                dist = min(clockwise, counterclockwise)
                if dist < best:
                    best = dist
        return -1 if best == float('inf') else best
```
- Notes:
  - We iterate through all indices and compute circular distances using modulo arithmetic.
  - Time complexity: O(n) where n = len(words) since we check each word once.
  - Space complexity: O(1) extra space (aside from input).
  - This handles the case where the target is at startIndex (distance 0) and multiple occurrences by taking the minimum.