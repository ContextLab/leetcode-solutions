# [Problem 2099: Find Subsequence of Length K With the Largest Sum](https://leetcode.com/problems/find-subsequence-of-length-k-with-the-largest-sum/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need a subsequence of length k with the largest possible sum. The order in the result must match the original array. The straightforward idea: pick the k largest elements (by value) and then return them in the original order. That suggests selecting indices of the top-k values, then sorting those indices to restore original order. Edge cases: negative numbers (still fine — pick the largest negatives), duplicates (if multiple equal values exist, any selection of k of them that yields the maximum sum is acceptable). Efficiency: n is up to 1000, so O(n log n) sorting is fine. Alternatively, a heap of size k gives O(n log k).

## Refining the problem, round 2 thoughts
- Implementation detail: we need indices to restore order. So get indices sorted by value descending, take first k indices, then sort those indices ascending and output nums at those indices.
- When values tie, Python's sort is stable. Using a key on index range (key = nums.__getitem__) and reverse=True will keep earlier indices before later ones for equal values — that's fine, though the problem accepts any valid subsequence.
- Complexity: sorting indices by value O(n log n). Extracting and sorting selected indices O(k log k) (k ≤ n). Memory: O(n) for indices.
- Alternative: use heapq.nlargest to get k indices in O(n log k) then sort indices O(k log k). Both are acceptable; sorted full array is simpler and clear.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxSubsequence(self, nums: List[int], k: int) -> List[int]:
        n = len(nums)
        # Get indices sorted by value descending (largest values first)
        indices_by_value = sorted(range(n), key=nums.__getitem__, reverse=True)
        # Take top k indices
        top_k_indices = indices_by_value[:k]
        # Sort these indices to restore original order (subsequence)
        top_k_indices.sort()
        # Build result in original order
        return [nums[i] for i in top_k_indices]
```
- Notes:
  - Approach: select indices of the k largest values, then output those elements in original order to form a subsequence.
  - Time complexity: O(n log n) due to sorting all indices by their values; plus O(k log k) to sort the selected indices (dominant term O(n log n)). If using a heap to find top-k, we could achieve O(n log k).
  - Space complexity: O(n) for auxiliary index lists.