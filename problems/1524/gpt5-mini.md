# [Problem 1524: Number of Sub-arrays With Odd Sum](https://leetcode.com/problems/number-of-sub-arrays-with-odd-sum/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t provide a stream-of-consciousness internal monologue, but here is a concise, high-level summary of the initial idea:

- Parity (odd/even) of sums is all that matters. We can use prefix-sum parity rather than full sums.
- Count how many prefix sums seen so far are even and odd. A subarray sum is odd when the parity of the current prefix sum differs from the parity of a previous prefix sum.
- Iterate once, maintain counts of even/odd prefixes, and accumulate the number of subarrays ending at the current position that are odd.

## Refining the problem, round 2 thoughts
High-level refinement and edge cases (concise):
- Initialize even_count = 1 because prefix sum 0 (before any element) is even. odd_count = 0.
- For each element, update current prefix parity (flip if element is odd). If current prefix is even, the number of odd-sum subarrays ending here equals odd_count (previous odd prefixes). If current prefix is odd, add even_count.
- Increment the appropriate prefix count after using it.
- Take result modulo 10^9+7 as required.
- Edge cases: all evens -> result 0; single element (odd/even) handled naturally.
- Complexity: O(n) time, O(1) extra space. This is optimal.

## Attempted solution(s)
```python
class Solution:
    def numOfSubarrays(self, arr: list[int]) -> int:
        MOD = 10**9 + 7
        even_count = 1  # prefix sum 0 is even
        odd_count = 0
        res = 0
        curr_parity = 0  # 0 for even, 1 for odd prefix sum

        for x in arr:
            if x % 2 == 1:
                curr_parity ^= 1  # flip parity when adding an odd number

            if curr_parity == 0:
                # current prefix even -> odd subarrays come from previous odd prefixes
                res = (res + odd_count) % MOD
                even_count += 1
            else:
                # current prefix odd -> odd subarrays come from previous even prefixes
                res = (res + even_count) % MOD
                odd_count += 1

        return res
```
- Notes:
  - Approach: Use parity of prefix sums and counts of previous prefixes by parity. For each prefix, the number of odd-sum subarrays ending at current index equals the number of previous prefixes with opposite parity.
  - Time complexity: O(n), where n = len(arr).
  - Space complexity: O(1) extra space (only counters and a few variables).
  - Implementation detail: start even_count = 1 to account for the empty prefix (sum 0). Result is kept modulo 10^9+7 throughout.