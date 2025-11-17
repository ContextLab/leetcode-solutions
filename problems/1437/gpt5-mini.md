# [Problem 1437: Check If All 1's Are at Least Length K Places Away](https://leetcode.com/problems/check-if-all-1s-are-at-least-length-k-places-away/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to verify that every pair of 1s in the array has at least k zeros between them. The array length up to 1e5 so an O(n) scan is fine. The simplest idea: walk the array, remember the index of the previous 1; when I encounter a new 1, compute the gap between indices and check whether there are at least k zeros between them. If any gap is too small, return False. If I finish the scan, return True.

Edge quick thoughts: if k == 0 it's always true because no separation required. For the first encountered 1 there is no previous to compare with. Use -inf or None to indicate no previous 1. Be careful with off-by-one: if previous 1 at i_prev and current at i, number of places between = i - i_prev - 1, so require i - i_prev - 1 >= k -> equivalently i - i_prev > k.

## Refining the problem, round 2 thoughts
Implementation details:
- Iterate with enumerate to get indices.
- Keep prev index initialized to None.
- On nums[i] == 1:
  - If prev is not None, check if i - prev - 1 < k -> return False.
  - Update prev = i.
- Complexity: single pass, O(n) time, O(1) extra space.
Alternative approaches: you could count consecutive zeros after each 1, or use a queue to store last 1s, but those are no simpler or not more efficient in this problem.

Edge cases:
- All zeros -> True.
- Single 1 -> True.
- k = 0 -> True.
- Adjacent 1s -> must be k = 0 to be valid.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def kLengthApart(self, nums: List[int], k: int) -> bool:
        prev = None  # index of previous 1
        for i, val in enumerate(nums):
            if val == 1:
                if prev is not None:
                    # number of places between prev and i is (i - prev - 1)
                    if i - prev - 1 < k:
                        return False
                prev = i
        return True
```
- Notes:
  - Approach: single pass keeping the index of the last seen 1 and checking the number of zeros between consecutive 1s.
  - Time complexity: O(n), where n = len(nums), because we examine each element once.
  - Space complexity: O(1) extra space (only an index variable).
  - Implementation detail: the check uses i - prev - 1 < k (equivalently i - prev <= k) to detect a violation.