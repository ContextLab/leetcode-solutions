# [Problem 1394: Find Lucky Integer in an Array](https://leetcode.com/problems/find-lucky-integer-in-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to find integers whose frequency equals their value. The straightforward way is to count frequencies first, then check which values satisfy value == frequency. Since we want the largest lucky integer, I should return the maximum such value or -1 if none. Counting can be done with a dictionary (Counter) or a fixed-size list because values are bounded (1..500). Complexity should be linear in the array length.

## Refining the problem, round 2 thoughts
- Use collections.Counter for clarity and simplicity.
- After counting, iterate through the items and keep track of the largest number where count == number.
- Edge cases: no lucky integer -> return -1. If multiple lucky integers exist, return the largest.
- Constraints are small (n <= 500, values <= 500), so both Counter and an array of size 501 are fine.
- Time complexity: O(n). Space complexity: O(m) where m is number of distinct values (<= 500).

## Attempted solution(s)
```python
from collections import Counter

class Solution:
    def findLucky(self, arr: list[int]) -> int:
        """
        Return the largest integer x such that the frequency of x in arr is x.
        If none exists, return -1.
        """
        freq = Counter(arr)
        result = -1
        for num, cnt in freq.items():
            if num == cnt and num > result:
                result = num
        return result
```
- Notes:
  - Approach: Count frequencies, then find the maximum number whose frequency equals itself.
  - Time complexity: O(n) to build the Counter plus O(m) to scan distinct values (m <= 500), so overall O(n).
  - Space complexity: O(m) for the Counter (m distinct values, at most 500).
  - Implementation detail: Using Counter simplifies counting; using a fixed-size list of length 501 would also work and is equally efficient given constraints.