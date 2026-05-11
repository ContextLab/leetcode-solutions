# [Problem 2553: Separate the Digits in an Array](https://leetcode.com/problems/separate-the-digits-in-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem asks to take each integer in nums and break it into its digits in the same order, concatenating all these digits into one array. My first thought is to convert each number to a string and iterate over characters, converting each character back to an int — that's simple and preserves order. Another approach is to extract digits using modulo/division (collect digits in reverse and then reverse them), which avoids string conversion but is slightly more code. Constraints are small (nums.length up to 1000 and nums[i] up to 1e5), so either approach will be fast enough.

## Refining the problem, round 2 thoughts
- Edge cases: single-digit numbers (just append the number), numbers with zeros (e.g., 100 -> [1,0,0]) — string approach handles zeros naturally.
- Performance: total output size is sum of digits of all numbers; converting to string is O(digits) time per number, overall O(total digits). Space is O(total digits) for the answer.
- Simpler implementation and readability favor the string approach. The numeric approach avoids string allocations but is unnecessary given constraints.
- No tricky ordering concerns — digits must appear in the same left-to-right order as the original number.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def separateDigits(self, nums: List[int]) -> List[int]:
        ans: List[int] = []
        for num in nums:
            for ch in str(num):
                ans.append(ord(ch) - ord('0'))  # slightly faster than int(ch) in some cases
        return ans
```
- Notes:
  - Approach: convert each number to its string representation, iterate characters, convert to digit, and append to the result list. This preserves digit order and handles zeros correctly.
  - Time complexity: O(T) where T is the total number of digits across all numbers in nums (since each digit is processed once). Given nums.length ≤ 1000 and nums[i] ≤ 10^5, T is at most 6 * 1000 in practice.
  - Space complexity: O(T) for the output list (plus O(1) additional overhead, ignoring temporary string representation).
  - Implementation detail: used ord(ch) - ord('0') to convert char to int; int(ch) is equally correct and perhaps clearer — either is fine.