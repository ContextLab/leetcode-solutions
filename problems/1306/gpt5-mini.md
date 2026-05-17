# [Problem 1306: Jump Game III](https://leetcode.com/problems/jump-game-iii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This looks like a graph/reachability problem: treat each index i as a node and you have directed edges to i + arr[i] and i - arr[i] (if in bounds). We need to know if there's any path from start to an index whose value is 0. A straightforward approach is BFS or DFS from start, marking visited nodes to avoid cycles. Since arr values are non-negative and < n, we can mark visited in-place (e.g., set to -1) or use a boolean visited array. BFS is simple and ensures we process each index at most once.

## Refining the problem, round 2 thoughts
- Edge case: start might already be at a 0 — immediate true.
- Avoid infinite loops by marking visited as soon as an index is processed (or enqueued).
- arr[i] may be 0 for some indices — we can short-circuit when encountering such an index.
- Constraints up to 5*10^4 => O(n) or O(n log n) is fine; recursion depth (DFS recursion) might blow the stack for large n, so iterative BFS/DFS is safer.
- Two main implementations: BFS with deque or iterative stack DFS. I'll use BFS (queue) and mark visited by setting arr[idx] = -1 (safe because arr values are non-negative).

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def canReach(self, arr: List[int], start: int) -> bool:
        n = len(arr)
        # Quick check
        if arr[start] == 0:
            return True

        q = deque([start])

        while q:
            i = q.popleft()
            # If already visited, skip
            if arr[i] < 0:
                continue
            # If this index has value 0, success
            if arr[i] == 0:
                return True

            step = arr[i]
            # mark visited
            arr[i] = -1

            # neighbors
            for j in (i + step, i - step):
                if 0 <= j < n and arr[j] >= 0:
                    if arr[j] == 0:
                        return True
                    q.append(j)

        return False
```
- Approach notes:
  - We perform a BFS from start across indices with edges to i ± arr[i].
  - Mark visited by setting arr[i] = -1 to avoid revisiting; this is safe because arr elements are non-negative by problem statement.
  - We check for value 0 during traversal for early exit.

- Complexity:
  - Time: O(n). Each index is visited at most once and we do O(1) work per visit.
  - Space: O(n) in the worst case for the queue (and O(1) extra if counting in-place visited marks).