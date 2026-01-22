# [Problem 3201: Find the Maximum Length of Valid Subsequence I](https://leetcode.com/problems/find-the-maximum-length-of-valid-subsequence-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I notice the condition (sub[i] + sub[i+1]) % 2 is equal for all adjacent pairs. Sum parity of two numbers is 0 iff they have the same parity, and 1 iff they have opposite parity. So there are two classes of valid subsequences:
- All adjacent sums even => every pair of adjacent elements has same parity => the whole subsequence must be all even or all odd.
- All adjacent sums odd => adjacent elements must alternate parity.

So the answer is the maximum of:
- The longest subsequence where every element has the same parity (simply count evens and odds; take the larger count).
- The longest subsequence where parities strictly alternate (order matters, so we need to compute the longest alternating-parity subsequence respecting indices).

For alternation, we can scan and keep two DP states: longest alt-subsequence ending with an even, and ending with an odd. Each element can extend the opposite-parity state.

## Refining the problem, round 2 thoughts
Edge cases:
- A sequence of all evens or all odds: the "all-same-parity" option wins.
- Mixed but grouped (e.g., all evens then all odds): alternating subsequence may be short (order matters), so counting alone is not enough for alternation.
- Single elements are valid (but problem constraints n >= 2); DP initialization should allow starting new subsequences.

Algorithm:
- Count evens and odds (O(n)).
- Compute longest alternating-parity subsequence by scanning once:
  - dp_even = longest alternating subsequence length that ends with an even number
  - dp_odd  = longest alternating subsequence length that ends with an odd number
  - when we see an even: dp_even = max(dp_even, dp_odd + 1)
  - when we see an odd: dp_odd = max(dp_odd, dp_even + 1)
  Use temp variables for updates to avoid immediate overwrites causing incorrect extension.
- Answer = max(count_even, count_odd, dp_even, dp_odd)

Time: O(n). Space: O(1).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def longestValidSubsequence(self, nums: List[int]) -> int:
        # Count same-parity subsequences
        count_even = 0
        count_odd = 0
        for x in nums:
            if x & 1:
                count_odd += 1
            else:
                count_even += 1

        # Compute longest alternating-parity subsequence (respecting order)
        dp_even = 0  # longest alternating subsequence ending with an even number
        dp_odd = 0   # longest alternating subsequence ending with an odd number

        for x in nums:
            if x & 1:
                # x is odd: can extend any sequence that ended with even
                # use previous dp_even to update dp_odd
                dp_odd = max(dp_odd, dp_even + 1)
            else:
                # x is even: can extend any sequence that ended with odd
                dp_even = max(dp_even, dp_odd + 1)

        return max(count_even, count_odd, dp_even, dp_odd)
```
- Notes:
  - The solution exploits parity properties: same-parity subsequences correspond to adjacent sums even; alternating-parity subsequences correspond to adjacent sums odd.
  - Counting evens/odds gives the best "all-same-parity" subsequence in O(n).
  - The DP computes the best alternating-parity subsequence in a single pass, O(n) time and O(1) extra space.
  - Overall time complexity: O(n). Space complexity: O(1).