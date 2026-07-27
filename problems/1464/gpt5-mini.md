# [Problem 1464: Maximum Product of Two Elements in an Array](https://leetcode.com/problems/maximum-product-of-two-elements-in-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share internal stream-of-consciousness, but here’s a concise summary of the approach: we only need the two largest elements in the array because (nums[i]-1)*(nums[j]-1) is maximized by the two largest nums values. Two straightforward ways: sort and take the top two, or make a single pass to track the largest and second-largest. Single-pass gives O(n) time and O(1) extra space.

## Refining the problem, round 2 thoughts
I can’t provide internal deliberation, but here is a short refinement and edge-case checklist:
- The array length is at least 2, so there will always be two elements.
- Values range from 1 to 1000, no overflow concerns for Python.
- Two valid implementations: sort (O(n log n)) or one-pass linear scan (O(n)) with constant extra space.
- Choose one-pass for optimal time/space.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        # Track the largest and second largest values
        max1 = -1
        max2 = -1
        for x in nums:
            if x > max1:
                max2 = max1
                max1 = x
            elif x > max2:
                max2 = x
        return (max1 - 1) * (max2 - 1)
```
- Notes:
  - Approach: Single-pass linear scan to find the largest (max1) and second-largest (max2) numbers, then compute (max1-1)*(max2-1).
  - Time complexity: O(n), where n = len(nums).
  - Space complexity: O(1) extra space (only a couple of variables).
  - Implementation detail: Initialize max1 and max2 to -1 (safe because nums[i] >= 1), update appropriately when a new larger element is found. This handles duplicates correctly (e.g., two equal largest values).