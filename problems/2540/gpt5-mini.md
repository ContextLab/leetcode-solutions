# [Problem 2540: Minimum Common Value](https://leetcode.com/problems/minimum-common-value/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The arrays are sorted, so this suggests a two-pointer approach: walk through both arrays simultaneously and look for the first value that appears in both. Since we want the minimum common integer, the first time both pointers point to the same value (while advancing the pointer with the smaller current value) will be the answer.  
An alternative is to put one array into a hash set and scan the other to find the smallest common element, but that uses extra space. Given the arrays are sorted, two pointers gives O(1) extra space and linear time.

## Refining the problem, round 2 thoughts
- Two pointers: i, j start at 0. If nums1[i] < nums2[j], increment i; if nums1[i] > nums2[j], increment j; if equal, return that value. If either pointer reaches the end, return -1.  
- Duplicates don't need special handling because equality check will catch a common value even if duplicates exist; returning the first equal value encountered is guaranteed to be the minimum common since arrays are sorted non-decreasingly.
- Time complexity O(n + m). Space complexity O(1).
- Edge cases: arrays of length 1, no common elements, arrays with identical values, extremely large values (but we're just comparing integers so fine).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def getCommon(self, nums1: List[int], nums2: List[int]) -> int:
        i, j = 0, 0
        n1, n2 = len(nums1), len(nums2)
        while i < n1 and j < n2:
            if nums1[i] == nums2[j]:
                return nums1[i]
            if nums1[i] < nums2[j]:
                i += 1
            else:
                j += 1
        return -1
```
- Notes:
  - Approach: two-pointer scan leveraging sorted order; when values match we return immediately (the first match is the minimum common value).
  - Time complexity: O(n + m), where n = len(nums1) and m = len(nums2).
  - Space complexity: O(1) extra space.
  - No special handling for duplicates is required since the arrays are sorted and the first match encountered is the smallest common value.