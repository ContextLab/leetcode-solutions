# [Problem 1399: Count Largest Group](https://leetcode.com/problems/count-largest-group/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to group numbers 1..n by the sum of their digits and find how many groups have the maximum size. The simplest approach is to compute the digit sum for each number and count how many numbers map to each sum. Use a hash map (or Python's Counter) keyed by digit sum. After counting all numbers, find the largest count and then count how many keys have that count.

Computing digit sum can be done either by converting to string and summing characters or by repeated division/modulo. n <= 10^4, so either method is fine. The number of possible digit sums is small (for n up to 10^4, max sum is 1+0+0+0+... = up to 36 for 9999), so space usage is trivial.

Edge cases: small n like 1 or 2; groups with equal sizes. Ensure correctness when multiple groups tie for the maximum.

## Refining the problem, round 2 thoughts
- Use a dictionary to accumulate counts of digit sums.
- Iterate from 1 to n inclusive, compute digit sum with a small helper (while loop avoids allocations).
- After building the counts, find max_count = max(counts.values()), then return sum(1 for v in counts.values() if v == max_count).
- Complexity: O(n * d) where d is number of digits (<=5 for n<=10^4), effectively O(n). Space is O(S) where S is number of distinct digit sums (small, bounded by 9*d).
- Alternative: using math to compute digit sum incrementally when incrementing i, but unnecessary given constraints.
- Confirm handle n=1 and other small values.

## Attempted solution(s)
```python
from collections import defaultdict

class Solution:
    def countLargestGroup(self, n: int) -> int:
        def digit_sum(x: int) -> int:
            s = 0
            while x:
                s += x % 10
                x //= 10
            return s

        counts = defaultdict(int)
        for i in range(1, n + 1):
            counts[digit_sum(i)] += 1

        if not counts:
            return 0

        max_count = max(counts.values())
        return sum(1 for v in counts.values() if v == max_count)
```
- Notes:
  - Approach: count numbers by their digit-sum group using a dictionary, then count how many groups reach the maximum size.
  - Time complexity: O(n * d) where d is number of digits in n (d <= 5 here), effectively O(n).
  - Space complexity: O(S) where S is number of distinct digit sums (small, bounded by 9 * number_of_digits).
  - Implementation detail: digit_sum uses integer arithmetic to avoid string conversions; this is simple and efficient for the input limits.