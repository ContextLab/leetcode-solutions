# [Problem 2348: Number of Zero-Filled Subarrays](https://leetcode.com/problems/number-of-zero-filled-subarrays/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see we need the number of contiguous subarrays consisting only of 0. Immediately I recall that consecutive zero runs contribute many subarrays: a run of length k yields k + (k-1) + ... + 1 = k*(k+1)/2 zero-only subarrays. So one pass scanning for consecutive zeros and adding that formula when a run ends should work. I should be careful about large counts (though Python int is unbounded, this is fine). Time O(n), space O(1). Also could do incremental counting: whenever we see a zero we extend the current run and add its length to the total (because new subarrays ending at current index equal current run length).

## Refining the problem, round 2 thoughts
Edge cases: all non-zero → answer 0; all zeros → n*(n+1)/2 possibly large but safe in Python. Alternative solutions: use two-pointers or accumulate lengths and sum formula later; or an incremental online addition: when we see a zero, current_run += 1 and result += current_run, else reset run. That incremental method avoids computing k*(k+1)/2 separately and is elegant. Complexity: single pass O(n) time, O(1) extra space. n up to 1e5, so fine. Implementation detail: ensure to use integer arithmetic. Return integer.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def zeroFilledSubarray(self, nums: List[int]) -> int:
        # Use incremental counting: for each zero, the number of zero-only subarrays
        # that end at that position equals the length of the current consecutive zero run.
        total = 0
        run = 0
        for x in nums:
            if x == 0:
                run += 1
                total += run
            else:
                run = 0
        return total
```
- Notes:
  - Approach: single pass; maintain current consecutive-zero run length `run`. Each time we see a zero, all subarrays ending at that index that are zero-only are exactly of sizes 1..run, so add `run` to the total.
  - Time complexity: O(n), where n = len(nums).
  - Space complexity: O(1) extra space.
  - Works for edge cases (no zeros => 0, all zeros => n*(n+1)/2).