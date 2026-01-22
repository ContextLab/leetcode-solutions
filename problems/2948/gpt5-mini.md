# [Problem 2948: Make Lexicographically Smallest Array by Swapping Elements](https://leetcode.com/problems/make-lexicographically-smallest-array-by-swapping-elements/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can swap two elements only if their values differ by at most limit. That suggests viewing the array as nodes in a graph where an edge exists between two indices if |nums[i] - nums[j]| <= limit; within a connected component we can perform swaps to rearrange values among those indices. However, swaps change values and thus might change which edges are available later — so I need to check whether it's sufficient to analyze the initial graph.

If two elements are connected by a path of pairwise "close" elements (each adjacent pair in the path has value difference <= limit), then we can swap along that path and effectively move values around inside that connected component. Intuitively components are formed by values that can be chained together via pairwise differences <= limit. If we sort by value, any component must be contiguous in that sorted order because a gap > limit between adjacent sorted values means no edge crosses that gap. So components correspond to maximal runs in the sorted-by-value list such that every adjacent difference <= limit.

Once components are identified, we can arbitrarily permute values inside each component, so to make the whole array lexicographically smallest, we should place the smallest available values of a component at the smallest indices of that component.

So plan: pair values with original indices, sort by value, break into groups when gap > limit, for each group collect indices and values, sort indices ascending and values ascending, assign smallest values to smallest indices.

## Refining the problem, round 2 thoughts
- Need to justify that initial connectivity (based on initial values) suffices. Reasoning: an edge between two elements exists initially iff their values differ by <= limit. If we have a chain v1 - v2 - ... - vk where differences between consecutive values are <= limit, we can swap along these edges to move any value within that chain to any index in the chain (permutations achievable). Because the graph on values (with edges for diff <= limit) is an undirected graph; connected components of that graph give sets of values/indices among which arbitrary permutations are achievable via sequences of allowed swaps. Sorting by value shows these components are contiguous segments in the sorted-by-value list: a gap > limit between adjacent sorted values breaks connectivity.
- Edge cases: duplicates (no problem), all gaps > limit (no swaps allowed), whole array connected (we can sort the whole array).
- Complexity: sorting pairs O(n log n). Grouping and assignment O(n log n) due to sorting indices inside groups; but overall still O(n log n). Space O(n) for pairs and result.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def smallestArray(self, nums: List[int], limit: int) -> List[int]:
        n = len(nums)
        # Pair each value with its original index and sort by value
        pairs = sorted((val, i) for i, val in enumerate(nums))
        res = nums[:]  # will overwrite positions for groups
        
        # Walk through sorted pairs and form groups where consecutive value diffs <= limit
        group_vals = []
        group_idxs = []
        prev_val = None
        
        def flush_group():
            if not group_vals:
                return
            # sort indices and values and assign smallest values to smallest indices
            group_idxs.sort()
            group_vals.sort()
            for idx, val in zip(group_idxs, group_vals):
                res[idx] = val
        
        for val, idx in pairs:
            if prev_val is None or val - prev_val <= limit:
                group_vals.append(val)
                group_idxs.append(idx)
            else:
                # gap > limit -> finalize previous group and start a new group
                flush_group()
                group_vals = [val]
                group_idxs = [idx]
            prev_val = val
        
        # flush last group
        flush_group()
        return res
```
- Notes about approach:
  - We pair values with indices and sort by value. Consecutive values in sorted order that differ by at most limit belong to the same connected component (they can be chained via edges). If a gap > limit occurs between consecutive sorted values, no edge can connect across the gap, so components are contiguous segments in the sorted list.
  - For each component, we collect original indices and component values; sorting indices ascending and values ascending, and assigning smallest values to smallest indices yields the lexicographically smallest arrangement achievable for that component.
- Complexity:
  - Time: O(n log n) dominated by sorting the value-index pairs and sorting indices/values inside groups (overall still O(n log n) across all groups).
  - Space: O(n) for pairs, result array, and temporary group storage.