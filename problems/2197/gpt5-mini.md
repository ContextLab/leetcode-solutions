# [Problem 2197: Replace Non-Coprime Numbers in Array](https://leetcode.com/problems/replace-non-coprime-numbers-in-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to repeatedly replace any two adjacent numbers that are non-coprime (gcd > 1) with their LCM, until no adjacent pair has gcd > 1. This is inherently local but replacements can cascade — when two adjacent numbers are merged into an LCM, that LCM may now be non-coprime with its new neighbor on either side and cause further merges. A straightforward simulation where we search the array for any adjacent non-coprime pair and repeat would be expensive (repeated scanning). A common pattern for problems with repeated adjacent-merging is to use a stack: we process elements left-to-right, push each element, and after pushing attempt to merge the top two while possible. If a merge occurs, the new merged value can further merge with the previous stack element(s), which the while-loop handles. This yields a single pass with possible pop/merge operations.

Key operations: gcd and lcm (lcm = a // gcd(a,b) * b or a*b // gcd(a,b)). Use math.gcd to compute gcd efficiently. Be mindful of overflow, but Python handles big integers; problem guarantees final values ≤ 1e8.

## Refining the problem, round 2 thoughts
- Use a stack to maintain the current array after applying all possible merges for the processed prefix.
- For each number cur, while stack not empty and gcd(stack[-1], cur) > 1:
  - compute g = gcd(stack[-1], cur)
  - cur = lcm(stack[-1], cur) = stack[-1] // g * cur  (or stack[-1] * cur // g)
  - pop stack
  - continue because new cur might merge with new top of stack
- After the while loop, push cur onto the stack.
- After processing all numbers, stack is the answer.

Edge cases:
- Values equal to 1 never merge (gcd(1,x)=1).
- Repeated merges can grow value, but constraints ensure final values ≤ 1e8.
- Complexity: each element is pushed once and popped at most once in the amortized sense; gcd cost dominates in each merge. Using math.gcd is fast.

Time complexity: O(n * cost_gcd), where cost_gcd is roughly logarithmic in value sizes (so practical O(n log M)). Space complexity: O(n) for the stack.

## Attempted solution(s)
```python
from typing import List
import math

class Solution:
    def replaceNonCoprime(self, nums: List[int]) -> List[int]:
        stack: List[int] = []
        for num in nums:
            cur = num
            # Try to merge cur with previous elements while gcd > 1
            while stack:
                g = math.gcd(stack[-1], cur)
                if g == 1:
                    break
                # merge: lcm = stack[-1] // g * cur
                cur = (stack[-1] // g) * cur
                stack.pop()
            stack.append(cur)
        return stack
```
- Notes:
  - Approach: single-pass stack-based merging. For each incoming number, repeatedly merge with the stack top while gcd > 1; push the resulting value when no more merges are possible.
  - Correctness: Every time two adjacent non-coprime numbers must be merged, this process simulates such merges in a left-to-right greedy way, and it handles cascades because after merging we test again with the new neighbor on the left. It's known that the final array is independent of the order of merges.
  - Time complexity: O(n * T_gcd) where T_gcd is the time to compute gcd of two numbers (practically O(log M)), so overall roughly O(n log M). Each element is pushed once and popped at most once amortized.
  - Space complexity: O(n) extra for the stack.