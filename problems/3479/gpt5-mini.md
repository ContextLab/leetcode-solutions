# [Problem 3479: Fruits Into Baskets III](https://leetcode.com/problems/fruits-into-baskets-iii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to place fruit types in baskets from left to right. For each fruit (in the given order) we must place it in the leftmost available basket whose capacity >= fruit quantity. Once a basket is used it can't be reused. If no such basket exists the fruit remains unplaced. We want the number of unplaced fruits.

Brute force: for each fruit scan baskets left-to-right skipping used ones until finding a basket with capacity >= fruit; that's O(n^2) worst-case and too slow for n up to 1e5.

We need an efficient way to, for a given fruit size x, find the minimum index j among all unused baskets with capacity >= x. This is a 2D-type query (threshold on capacity and minimize index). We can group baskets by capacity and for each capacity keep the set (or min-heap) of their indices. Then if we arrange capacities sorted, for a query x we want the minimal index across all capacity groups with capacity >= x. That suggests a segment tree over the capacity coordinate where each leaf stores the minimal unused index among baskets with that capacity; internal nodes store the minimum of children. Querying range [first_capacity_ge_x, +inf] returns the leftmost index available. After placing a fruit we remove that index from its capacity group (pop heap) and update the segment tree.

This yields O(n log n) time and O(n) space.

## Refining the problem, round 2 thoughts
- We'll compress unique basket capacities and map capacity -> index in sorted capacities.
- For each capacity bucket keep a min-heap of basket indices; the leaf value is heap[0] or INF if empty.
- Segment tree nodes store the pair (min_index, capacity_bucket_index) where min_index is minimal index inside that node's capacity range. Merging picks the pair with smaller min_index.
- For each fruit:
  - binary-search the first capacity >= fruit in sorted capacities
  - if none => cannot place
  - else segment-tree query on that capacity-range => gives (min_index, bucket_idx)
  - if min_index == INF => cannot place
  - else pop that index from heap[bucket_idx], update leaf to new heap[0] or INF
- Edge cases: repeated capacities, many baskets with same capacity — heap handles this. If fruit > max capacity obviously unplaced.
- Complexity: building heaps O(n), segment tree build O(m) where m <= n, each fruit O(log n) for binsearch + O(log n) for segment-tree query + O(log n) for heap pop in aggregate O(n log n). Space O(n).

## Attempted solution(s)
```python
from typing import List
import bisect
import heapq

class SegmentTree:
    # stores (min_index, bucket_pos) at each node
    def __init__(self, base):
        # base: list of (min_index, bucket_pos) for leaves
        self.n = len(base)
        self.size = 1
        while self.size < self.n:
            self.size <<= 1
        INF = 10**18
        self.tree = [(INF, -1)] * (2 * self.size)
        # build leaves
        for i in range(self.n):
            self.tree[self.size + i] = base[i]
        for i in range(self.size - 1, 0, -1):
            left = self.tree[2 * i]
            right = self.tree[2 * i + 1]
            # pick smaller min_index; tie-break doesn't matter
            self.tree[i] = left if left[0] <= right[0] else right

    def update(self, pos, val_pair):
        # pos: leaf index (0-based), val_pair: (min_index, bucket_pos)
        i = self.size + pos
        self.tree[i] = val_pair
        i //= 2
        while i:
            left = self.tree[2 * i]
            right = self.tree[2 * i + 1]
            self.tree[i] = left if left[0] <= right[0] else right
            i //= 2

    def query(self, l, r):
        # inclusive range [l, r], returns (min_index, bucket_pos)
        INF = 10**18
        l += self.size
        r += self.size
        res_left = (INF, -1)
        res_right = (INF, -1)
        while l <= r:
            if (l & 1) == 1:
                res_left = res_left if res_left[0] <= self.tree[l][0] else self.tree[l]
                l += 1
            if (r & 1) == 0:
                res_right = self.tree[r] if self.tree[r][0] <= res_right[0] else res_right
                r -= 1
            l //= 2
            r //= 2
        # merge left and right results
        return res_left if res_left[0] <= res_right[0] else res_right

class Solution:
    def unplacedFruits(self, fruits: List[int], baskets: List[int]) -> int:
        n = len(fruits)
        # compress unique capacities
        caps = sorted(set(baskets))
        m = len(caps)
        # bucket heaps per capacity (store indices)
        heaps = [[] for _ in range(m)]
        cap_to_pos = {c: i for i, c in enumerate(caps)}
        for idx, cap in enumerate(baskets):
            pos = cap_to_pos[cap]
            heapq.heappush(heaps[pos], idx)
        INF = 10**18
        base = []
        for i in range(m):
            if heaps[i]:
                base.append((heaps[i][0], i))
            else:
                base.append((INF, i))
        seg = SegmentTree(base)

        unplaced = 0
        for fruit in fruits:
            # find first capacity >= fruit
            pos = bisect.bisect_left(caps, fruit)
            if pos == m:
                unplaced += 1
                continue
            min_idx, bucket_pos = seg.query(pos, m - 1)
            if min_idx >= INF:
                unplaced += 1
            else:
                # assign that basket: remove its index from the heap and update segtree leaf
                heapq.heappop(heaps[bucket_pos])
                if heaps[bucket_pos]:
                    seg.update(bucket_pos, (heaps[bucket_pos][0], bucket_pos))
                else:
                    seg.update(bucket_pos, (INF, bucket_pos))
        return unplaced
```
- Notes:
  - Approach: compress capacities, maintain a heap of indices for each capacity (min-heap gives leftmost index in that capacity), and a segment tree over capacity positions storing the minimal index in each subtree. For each fruit, binary-search first capacity >= fruit then query the segtree for minimal index among those capacities. If none found, fruit is unplaced; else pop that index and update.
  - Time complexity: O(n log n) overall. Each fruit triggers a binary search O(log n), a segment-tree query O(log n), and a heap pop O(log n) when placed.
  - Space complexity: O(n) for heaps, segment tree, and auxiliary structures.
  - Important detail: the segment tree stores pairs (min_index, bucket_pos) so we can both get which bucket contributed the minimal index and update that bucket's leaf after a placement. This ensures we always pick the globally leftmost available basket among those with capacity >= the fruit size.