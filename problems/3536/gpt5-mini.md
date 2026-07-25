# [Problem 3536: Maximum Product of Two Digits](https://leetcode.com/problems/maximum-product-of-two-digits/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the maximum product of any two digits in a positive integer n. The digits are 0-9, and n has at least two digits (n >= 10). The naive way is to enumerate all pairs of digits and compute products, but since digits count is small (<= 10 for n up to 1e9), that's fine. A simpler and optimal approach is to just find the two largest digits and multiply them. Careful about duplicates — if the largest digit appears twice, using it twice is allowed. So I can scan digits once and keep the top two values.

## Refining the problem, round 2 thoughts
- Scanning digits as integers (n % 10) is straightforward and avoids string conversion, though string method is also fine.
- Maintain two variables max1 and max2 for the largest and second largest digits. On seeing digit d:
  - if d >= max1: set max2 = max1; max1 = d
  - else if d > max2: set max2 = d
- After scanning, return max1 * max2.
- Complexity: O(number of digits) time, O(1) space. For constraints, that's essentially constant time.

## Attempted solution(s)
```python
class Solution:
    def maxProduct(self, n: int) -> int:
        # Keep track of the largest and second largest digit
        max1 = -1
        max2 = -1
        while n > 0:
            d = n % 10
            n //= 10
            if d >= max1:
                max2 = max1
                max1 = d
            elif d > max2:
                max2 = d
        return max1 * max2
```
- Notes:
  - We scan digits using modulo and integer division, updating the top two digits seen.
  - The comparison uses >= for the first branch so duplicates of the largest digit correctly fill both max1 and max2 (e.g., n = 22).
  - Time complexity: O(d) where d is the number of digits in n (d <= 10 here), effectively O(1).
  - Space complexity: O(1).