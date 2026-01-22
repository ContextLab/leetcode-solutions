# [Problem 3068: Find the Maximum Sum of Node Values](https://leetcode.com/problems/find-the-maximum-sum-of-node-values/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The operation chooses an edge [u,v] and XORs both endpoints by k. Each time an endpoint is involved in an operation it flips (XORed by k). If a node has an odd number of chosen incident edges then it ends up XORed by k; if even number then it stays the same. So the final state is determined by the parity of chosen incident edges for each node.

This is a tree. For a tree we can pick edges along the path between any two nodes: selecting all edges on a path flips exactly the two endpoints (interior nodes have degree 2 in that chosen subgraph and thus flip 0 mod 2). So any pair of nodes can be flipped simultaneously. By pairing up nodes we can realize any subset with even size. Linear algebra viewpoint: incidence matrix over GF(2) for a connected tree has image = all vectors with even total parity, so achievable flip patterns are exactly subsets of nodes of even cardinality.

Thus the whole problem reduces to: for each node i, flipping it changes sum by delta[i] = (nums[i] XOR k) - nums[i]. We can choose any subset with even cardinality to maximize the total sum = sum(nums) + sum_{i in S} delta[i]. So choose an even-sized subset S maximizing sum of deltas. This is equivalent to picking deltas with largest positive contribution but respecting even count.

So solution strategy: take all positive deltas. If their count is even, include them all. If count is odd, we must either remove the smallest positive delta or add the largest (closest to zero) non-positive delta — pick whichever gives the larger total.

## Refining the problem, round 2 thoughts
Edge cases:
- No positive deltas -> best is do nothing (0 selected), sum unchanged.
- All deltas positive and count odd -> we must drop the smallest positive.
- There may be no non-positive delta to add; then removal is the only option.
- We must ensure integer arithmetic and O(n) time. We don't need to sort all values; we only need the smallest positive and the largest non-positive.

Complexity: single pass to compute deltas, sum, count, min_pos, max_nonpos => O(n) time and O(1) extra space (besides input). This is optimal.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maximumSum(self, nums: List[int], k: int, edges: List[List[int]]) -> int:
        # We don't actually need the edges for the computation because
        # in a tree any even-sized subset of nodes can be flipped.
        base = sum(nums)
        min_pos = float('inf')
        max_nonpos = -float('inf')
        sum_pos = 0
        cnt_pos = 0
        
        for x in nums:
            d = (x ^ k) - x
            if d > 0:
                sum_pos += d
                cnt_pos += 1
                if d < min_pos:
                    min_pos = d
            else:
                if d > max_nonpos:
                    max_nonpos = d
        
        if cnt_pos % 2 == 0:
            return base + sum_pos
        
        # cnt_pos is odd: we must either remove the smallest positive delta
        # or add the best non-positive delta (if exists).
        best1 = -float('inf')
        best2 = -float('inf')
        if min_pos != float('inf'):  # there is at least one positive
            best1 = base + sum_pos - min_pos
        if max_nonpos != -float('inf'):  # there is at least one non-positive
            best2 = base + sum_pos + max_nonpos
        
        return int(max(best1, best2))
```
- Notes:
  - Key observation: on a tree any even-sized set of nodes can be flipped (flip pairs along paths), so edges are irrelevant beyond guaranteeing a tree.
  - We compute delta[i] = (nums[i] XOR k) - nums[i]. We greedily include all positive deltas; if their count is even we are done. If odd, we either drop the smallest positive or add the largest non-positive, whichever hurts sum less (i.e., yields larger total).
  - Time complexity: O(n) to compute deltas and the few aggregates.
  - Space complexity: O(1) extra (ignoring input).