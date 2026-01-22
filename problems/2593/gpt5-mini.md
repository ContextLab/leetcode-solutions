# [Problem 2593: Find Score of an Array After Marking All Elements](https://leetcode.com/problems/find-score-of-an-array-after-marking-all-elements/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem statement literally prescribes a greedy selection: always pick the smallest unmarked element (tie: smallest index). That suggests simulating the described process. We need to repeatedly pick the smallest remaining element; a min-heap or sorting the elements by (value, index) will let us iterate in that order. Once we pick an element, we add its value to the score and mark it and its neighbors. A boolean array of visited/marked flags can represent which indices are already marked.

Sorting by (value, index) yields the correct tie-breaking automatically. Then for each (val, idx) in increasing order, if idx is unmarked, add val and mark idx-1, idx, idx+1. That should finish when all get marked because we iterate over all elements.

This looks like O(n log n) dominated by the sort and O(n) extra space for visited.

## Refining the problem, round 2 thoughts
Edge cases:
- n = 1: pick the single element.
- n = 2: picking one element marks both (if adjacent), so ensure bounds checks.
- Multiple equal values: we must pick left-most among equal values — sorting by (value, index) handles this.
Alternative: maintain a min-heap of (value, index) and pop until unmarked, doing same marking step; complexity similar (O(n log n)). Sorting is simpler and deterministic.

Correctness reasoning: The problem forces this greedy choice; we only need to simulate it in the specified order. There's no need for more complex DP or interval structures because marking is local (index ±1) and the selection order is fully determined by values then indices.

Time complexity: O(n log n) for sorting, O(n) extra space for the visited array. Implementation must be careful to only add the element's value when it's still unmarked.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findScore(self, nums: List[int]) -> int:
        n = len(nums)
        # Pair value with index and sort by value then index
        pairs = sorted((val, i) for i, val in enumerate(nums))
        marked = [False] * n
        score = 0
        
        for val, i in pairs:
            if not marked[i]:
                score += val
                # mark i and neighbors if within bounds
                marked[i] = True
                if i - 1 >= 0:
                    marked[i - 1] = True
                if i + 1 < n:
                    marked[i + 1] = True
        return score
```
- Notes:
  - Approach: sort elements by (value, index) and simulate marking. For each element in ascending order, if it's still unmarked, add its value to the score and mark it and its neighbors.
  - Time complexity: O(n log n) due to sorting n elements.
  - Space complexity: O(n) for the sorted pairs (implicit) and the marked boolean array.
  - Implementation details: Sorting by (value, index) automatically enforces the "smallest index on ties" requirement. Bounds checks are used when marking neighbors.