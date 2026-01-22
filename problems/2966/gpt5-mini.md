# [Problem 2966: Divide Array Into Arrays With Max Difference](https://leetcode.com/problems/divide-array-into-arrays-with-max-difference/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to split nums (length n, multiple of 3) into n/3 groups of size 3 such that in each group the max difference ≤ k. Sorting the array is a natural first step for grouping by closeness. After sorting, the smallest element must be grouped with the two smallest remaining elements to minimize differences — if that triple still violates the k constraint, that smallest element can never be in a valid triple (because any other choice would only increase the max difference). This suggests a simple greedy: sort and take consecutive triples.

## Refining the problem, round 2 thoughts
Refinement / proof idea:
- After sorting, consider the smallest unused element x at index i. If arr[i+2] - arr[i] > k then any triple containing arr[i] will have difference > k (since any later elements are >= arr[i+2]). So it's impossible.
- Thus the only valid choice for arr[i] is to pair it with arr[i+1] and arr[i+2]. If that triple satisfies the constraint, we can take it and continue with the rest.
- So a correct algorithm is: sort nums, then iterate in blocks of 3 (i=0,3,6,...). For each block check arr[i+2]-arr[i] ≤ k; if any block fails, return []; otherwise return the blocks.

Time complexity: sorting O(n log n) dominates. Extra space O(n) for result (or O(1) besides sorted array if in-place used). Edge cases: duplicates, already sorted, small n, etc. n is guaranteed a multiple of 3 so no leftover elements.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def divideArray(self, nums: List[int], k: int) -> List[List[int]]:
        n = len(nums)
        nums.sort()
        res = []
        # process consecutive triples in sorted order
        for i in range(0, n, 3):
            if nums[i+2] - nums[i] > k:
                return []
            res.append([nums[i], nums[i+1], nums[i+2]])
        return res
```
- Notes:
  - Approach: sort and greedily take consecutive triples. If any triple (i, i+1, i+2) has max-min > k, return empty because the smallest element of that triple cannot be placed in any valid triple.
  - Time complexity: O(n log n) due to sorting.
  - Space complexity: O(n) for the output (and O(1) additional besides sorted array if sorting in-place).