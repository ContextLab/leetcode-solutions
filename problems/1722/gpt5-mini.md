# [Problem 1722: Minimize Hamming Distance After Swap Operations](https://leetcode.com/problems/minimize-hamming-distance-after-swap-operations/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see allowedSwaps describes pairs of indices in source that can be swapped any number of times. That means indices connected by those pairs form components where elements of source can be permuted arbitrarily within each component. So the problem reduces to: for each connected component of indices, we can freely rearrange the source values to best match the target values at those indices. The best is to match as many equal values as possible. So for each component count frequencies of values in source and target, match greedily by value: matched = sum(min(count_src[val], count_target[val])) across values; the remainder in that component contributes to Hamming distance.

Union-Find (DSU) or building graph + DFS to find components is the natural approach. DSU is straightforward and efficient for up to 1e5 indices and swaps.

## Refining the problem, round 2 thoughts
Edge cases: no allowedSwaps => result is direct Hamming distance. Values may be large but we only use them as keys in Counters. Duplicate values handled by counts. Complexity: union operations O(m α(n)), building components O(n), counting/matching values sums to O(n) work across components. Space O(n) for DSU and grouping. Alternative: use BFS/DFS on adjacency list instead of DSU; both fine. Implementation details: use path compression + union by size/rank. For each component, use collections.Counter for source and target sublists and compute matched counts.

## Attempted solution(s)
```python
from collections import defaultdict, Counter
from typing import List

class DSU:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        # path compression
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a: int, b: int) -> None:
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return
        # union by size
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]

class Solution:
    def minimumHammingDistance(self, source: List[int], target: List[int], allowedSwaps: List[List[int]]) -> int:
        n = len(source)
        dsu = DSU(n)
        for a, b in allowedSwaps:
            dsu.union(a, b)

        groups = defaultdict(list)
        for i in range(n):
            root = dsu.find(i)
            groups[root].append(i)

        hamming = 0
        for indices in groups.values():
            # Count frequencies of values in source and target for this component
            cnt_src = Counter()
            cnt_tgt = Counter()
            for i in indices:
                cnt_src[source[i]] += 1
                cnt_tgt[target[i]] += 1

            # Number of matches possible is sum over values of min counts
            matches = 0
            # iterate over smaller counter for efficiency
            if len(cnt_src) <= len(cnt_tgt):
                for val, c in cnt_src.items():
                    matches += min(c, cnt_tgt.get(val, 0))
            else:
                for val, c in cnt_tgt.items():
                    matches += min(c, cnt_src.get(val, 0))

            # Unmatched positions contribute to hamming distance
            hamming += len(indices) - matches

        return hamming
```
- Notes:
  - Approach: use DSU to group indices that can be freely permuted; inside each group, match counts of values between source and target to maximize matched positions. The remainder in each component are mismatches contributing to the minimal Hamming distance.
  - Time complexity: O(n + m * α(n) + U) where n = len(source), m = len(allowedSwaps), α is inverse-Ackermann (practically constant), and U is the total work to count/match values across all components (O(n) amortized). So overall roughly O(n + m).
  - Space complexity: O(n) for DSU arrays and grouping plus extra for counters.