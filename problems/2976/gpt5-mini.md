# [Problem 2976: Minimum Cost to Convert String I](https://leetcode.com/problems/minimum-cost-to-convert-string-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to transform source -> target by repeatedly applying character substitutions that are allowed by given (original -> changed) operations with associated costs. Each operation changes a single character at some cost; operations can be chained (e.g., a -> c then c -> b). For a single position, the minimal cost to change letter x to y is just the shortest path cost from x to y in a directed weighted graph where nodes are letters and edges are given substitutions. Because substitutions are independent per character position, total cost is the sum of minimal per-position costs. If any required conversion is impossible (no path), answer is -1.

This suggests building a graph on 26 lowercase letters and computing shortest paths between all pairs; since alphabet size is small (26), Floyd-Warshall is appropriate and simple. Alternative: run Dijkstra from each source letter encountered, but Floyd-Warshall is easy and fast enough.

## Refining the problem, round 2 thoughts
- Build a 26x26 distance matrix, initialize distances to INF, dist[i][i] = 0.
- For each given original[i] -> changed[i] with cost[i], set dist[u][v] = min(dist[u][v], cost[i]) because multiple edges may be present.
- Run Floyd-Warshall to get minimal costs between all letter pairs.
- Iterate positions of source/target: if source[i] == target[i], cost 0; else if dist[src][tgt] is INF -> return -1; otherwise add dist[src][tgt].
- Time complexity: O(26^3) for Floyd-Warshall (~17k operations) + O(n) to sum costs. Space O(26^2).
- Use a sufficiently large INF (e.g., 10**18) to avoid overflow.
- Edge cases: identical strings (return 0), unreachable conversions (return -1).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minimumCost(self, source: str, target: str, original: List[str], changed: List[str], cost: List[int]) -> int:
        n = len(source)
        # Quick length check (given by problem they are equal)
        if n != len(target):
            return -1
        
        ALPH = 26
        INF = 10**18
        # dist[a][b] = minimum cost to convert letter a -> b
        dist = [[INF] * ALPH for _ in range(ALPH)]
        for i in range(ALPH):
            dist[i][i] = 0
        
        # Populate edges (take min if multiple edges between same pair)
        m = len(cost)
        for i in range(m):
            u = ord(original[i]) - ord('a')
            v = ord(changed[i]) - ord('a')
            if cost[i] < dist[u][v]:
                dist[u][v] = cost[i]
        
        # Floyd-Warshall
        for k in range(ALPH):
            dk = dist[k]
            for i in range(ALPH):
                di = dist[i]
                # small micro-optimization: if di[k] is INF skip inner
                ik = di[k]
                if ik == INF:
                    continue
                # iterate j
                # use local references
                for j in range(ALPH):
                    # if dk[j] == INF skip
                    val = ik + dk[j]
                    if val < di[j]:
                        di[j] = val
        
        total = 0
        for i in range(n):
            a = ord(source[i]) - ord('a')
            b = ord(target[i]) - ord('a')
            if a == b:
                continue
            if dist[a][b] == INF:
                return -1
            total += dist[a][b]
        return total
```
- Approach: Model characters as nodes in a directed weighted graph; compute all-pairs shortest paths with Floyd-Warshall; sum minimal per-position costs, returning -1 if any required conversion is unreachable.
- Time complexity: O(26^3 + n) = O(n) for large n (26^3 is constant ≈ 17k ops).
- Space complexity: O(26^2) = O(1) (constant).
- Implementation notes: multiple given conversions between same pair are reduced by taking the minimum cost edge; self-conversions cost 0; INF is chosen large to avoid overflow.