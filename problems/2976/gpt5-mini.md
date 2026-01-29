# [Problem 2976: Minimum Cost to Convert String I](https://leetcode.com/problems/minimum-cost-to-convert-string-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to convert each character of source to the corresponding character in target. Each allowed operation is changing a single character x -> y at a given cost z if such an operation exists in the input arrays. Because we can apply operations any number of times and in any sequence, this is naturally a shortest-path problem on a directed graph of letters (26 nodes a..z). Each given (original[i] -> changed[i]) with cost[i] is a directed edge; repeated operations correspond to following a path.

So for each position where source[i] != target[i], we need the minimum path cost from source[i] to target[i] in that directed graph. If any required pair is unreachable, return -1. Sum the minimal costs over positions. Build a 26x26 distance matrix, initialize with +inf except zeros on diagonal, set direct edge costs to the minimum among duplicates, then run Floyd–Warshall (26^3 is tiny). Finally sum distances for each mismatch.

Potential pitfalls: directed edges (not undirected), multiple edges between same pair, large n so summation must be efficient, detect unreachable pairs.

## Refining the problem, round 2 thoughts
Floyd–Warshall is simplest and safe: 26 nodes -> 26^3 ~ 17576 iterations. Alternatively could run Dijkstra from each source letter that appears in source where it differs from target — still cheap but more bookkeeping. Use Floyd–Warshall for clarity.

Edge cases:
- If source[i] == target[i] cost is 0.
- If there is no path from source[i] to target[i], answer is -1.
- There may be multiple edges between same nodes; pick the smallest.
- Costs can be up to 1e6 and n up to 1e5, so total sum can be large but fits Python int.
Time complexity: O(26^3 + n) ~ O(1 + n) effectively; space O(26^2).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minimumCost(self, source: str, target: str, original: List[str], changed: List[str], cost: List[int]) -> int:
        n = len(source)
        # Quick length check (problem guarantees same length)
        if n != len(target):
            return -1
        
        INF = 10**18
        # 26 letters
        m = 26
        # dist[i][j] = min cost to convert chr(i+'a') -> chr(j+'a')
        dist = [[INF] * m for _ in range(m)]
        for i in range(m):
            dist[i][i] = 0
        
        # Populate direct edges (take min if multiple edges)
        for o, c, w in zip(original, changed, cost):
            u = ord(o) - ord('a')
            v = ord(c) - ord('a')
            if w < dist[u][v]:
                dist[u][v] = w
        
        # Floyd-Warshall to get all-pairs shortest paths
        for k in range(m):
            dk = dist[k]
            for i in range(m):
                di = dist[i]
                # minor micro-optimization: only proceed if di[k] not INF
                ik = di[k]
                if ik == INF:
                    continue
                # iterate j
                # Use local variables for speed
                for j in range(m):
                    nj = ik + dk[j]
                    if nj < di[j]:
                        di[j] = nj
        
        # Sum up costs for each position
        total = 0
        for i in range(n):
            s = source[i]
            t = target[i]
            if s == t:
                continue
            u = ord(s) - ord('a')
            v = ord(t) - ord('a')
            if dist[u][v] == INF:
                return -1
            total += dist[u][v]
        return total
```
- Approach: Model characters as nodes of a directed weighted graph. Use Floyd–Warshall to compute the minimum conversion cost between any pair of letters, then sum costs for each differing position in source/target. If any required conversion is impossible, return -1.
- Time complexity: O(26^3 + n) = O(n) effectively, since 26^3 is constant ~17.5k.
- Space complexity: O(26^2) = O(1) constant.
- Implementation details: Use INF large enough to avoid overflow; pick min when multiple direct edges exist; Floyd–Warshall triple loop with a small optimization skipping i when dist[i][k] is INF.