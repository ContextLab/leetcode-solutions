# [Problem 1345: Jump Game IV](https://leetcode.com/problems/jump-game-iv/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem asks for the minimum number of jumps from index 0 to the last index where allowed jumps are i+1, i-1, or any other index j with arr[j] == arr[i]. This is naturally a shortest-path problem on an implicit unweighted graph where each array index is a node and edges connect adjacent indices and indices with equal value. For unweighted shortest path, BFS is the standard approach.

We need to be careful with the "equal value" edges because if many indices share the same value, naively exploring them repeatedly can cause a big slowdown. So we should gather indices by value first (value -> list of indices). When we expand a node, we should enqueue all other indices with the same value, but ensure we don't do that same-value expansion repeatedly for the same value (clear or remove the list once processed). Also handle trivial case of single element (0 steps).

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- If n == 1, return 0 immediately.
- Use BFS level-order traversal to count steps.
- Maintain a visited array (or set) to avoid revisiting indices.
- Use a dictionary mapping each value to the list of indices that contain that value. After enqueuing all same-value indices once, clear the list in the dictionary to avoid O(n^2) repeated scans.
- Each index enqueued only once, so complexity is linear in number of indices (plus mapping overhead).

Time and space complexity considerations:
- Building the mapping is O(n) time and O(n) extra space.
- BFS visits each index at most once. Processing equal-value edges for a particular value happens only once (we clear the list after processing), so total work for equal-value edges is O(n) overall.
- Therefore overall time is O(n) and space is O(n).

## Attempted solution(s)
```python
from collections import defaultdict, deque
from typing import List

class Solution:
    def minJumps(self, arr: List[int]) -> int:
        n = len(arr)
        if n <= 1:
            return 0

        # Map value -> list of indices with that value
        positions = defaultdict(list)
        for i, v in enumerate(arr):
            positions[v].append(i)

        visited = [False] * n
        visited[0] = True
        q = deque([0])
        steps = 0
        target = n - 1

        while q:
            size = len(q)
            for _ in range(size):
                i = q.popleft()
                if i == target:
                    return steps

                # neighbors: i-1
                if i - 1 >= 0 and not visited[i - 1]:
                    visited[i - 1] = True
                    q.append(i - 1)

                # neighbors: i+1
                if i + 1 < n and not visited[i + 1]:
                    visited[i + 1] = True
                    q.append(i + 1)

                # neighbors: all indices j where arr[j] == arr[i]
                val = arr[i]
                for j in positions[val]:
                    if not visited[j]:
                        visited[j] = True
                        q.append(j)

                # Important optimization: avoid future re-processing of this value
                positions[val].clear()

            steps += 1

        # If unreachable (problem constraints imply reachable), return -1 as fallback
        return -1
```
- Notes about the approach:
  - We perform BFS from index 0 and count levels as steps. For each popped index, we visit i-1, i+1, and all indices with the same value arr[i].
  - After using the list of indices for a value once, we clear it to avoid revisiting the same-value neighbors again from other indices of the same value. This keeps the total processing of equal-value edges linear.
  - Time complexity: O(n) (building map O(n), each index enqueued/processed once, equal-value lists processed once).
  - Space complexity: O(n) for the map, visited array, and BFS queue.