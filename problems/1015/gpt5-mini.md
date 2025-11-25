# [Problem 1015: Smallest Integer Divisible by K](https://leetcode.com/problems/smallest-integer-divisible-by-k/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the smallest positive integer n made only of digit '1' that is divisible by k, and return its length. Directly constructing the integer will quickly overflow, so I should work with remainders modulo k. If I build numbers 1, 11, 111, ... I can update the remainder r <- (r*10 + 1) % k each step and check when r == 0.

I recall that if k is divisible by 2 or 5, such a number can't exist because a decimal number composed only of 1s is odd (not divisible by 2) and its last digit is 1 (not divisible by 5). Also by pigeonhole principle, remainders repeat within k steps, so I only need to try at most k times; if I don't hit remainder 0 within k iterations it's impossible.

So algorithm: handle k%2==0 or k%5==0 -> -1; then iterate up to k times computing remainders, return index when remainder zero.

## Refining the problem, round 2 thoughts
Edge cases:
- k = 1 -> answer 1 (first remainder 1%1 == 0).
- Very large k up to 1e5; O(k) loop is fine.
- No extra memory needed beyond a few ints.

Alternative detection of impossibility: instead of special-casing 2 and 5, I could run the loop and rely on the k-iteration bound; but short-circuiting for 2 and 5 is a quick check and common observation.

Time complexity O(k), space O(1). Implementation straightforward in Python.

## Attempted solution(s)
```python
class Solution:
    def smallestRepunitDivByK(self, k: int) -> int:
        """
        Return the length of the smallest positive integer consisting only of '1's
        that is divisible by k, or -1 if none exists.
        """
        # Quick impossibility check: any number consisting only of 1's is odd and
        # ends with digit 1, so it cannot be divisible by 2 or 5.
        if k % 2 == 0 or k % 5 == 0:
            return -1

        remainder = 0
        # Try lengths from 1 to k (pigeonhole: if no remainder 0 in k steps, it won't appear)
        for length in range(1, k + 1):
            remainder = (remainder * 10 + 1) % k
            if remainder == 0:
                return length
        return -1
```
- Notes:
  - Approach: iterate building the remainder of 1, 11, 111, ... modulo k using remainder = (remainder*10 + 1) % k. Return the first length where remainder == 0.
  - Time complexity: O(k) in the worst case (at most k iterations).
  - Space complexity: O(1) extra space.
  - Important implementation details: avoid constructing the large integer itself; only track remainder. Early return for k divisible by 2 or 5 to handle impossibility quickly.