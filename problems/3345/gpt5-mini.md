# [Problem 3345: Smallest Divisible Digit Product I](https://leetcode.com/problems/smallest-divisible-digit-product-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the smallest number >= n whose digits' product is divisible by t. First observations:
- If any digit is 0 then the product is 0, and 0 is divisible by any t > 0, so any number containing 0 is always valid.
- If t == 1 then every product is divisible by 1, so answer is n.
- A brute-force check starting from n and incrementing by 1, computing digit product and checking divisibility, seems straightforward. Given t is at most 10 and the constraints shown are small, this should be fine.
- Could consider constructing numbers greedily, but brute force is simplest and safe here.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- Handle t == 1 quickly (return n).
- When computing digit product, short-circuit on encountering a digit 0 (product becomes 0 -> divisible).
- Complexity: brute force in the worst case increments until we find a number with required property. With small n constraints this is fine. If n were huge one might need a constructive approach, but not required for current constraints.
- Ensure integer overflow isn't an issue in Python (not a problem).
- Stop when we find the first valid number since we search in increasing order.

## Attempted solution(s)
```python
class Solution:
    def smallestNumber(self, n: int, t: int) -> int:
        # Quick answer for t == 1
        if t == 1:
            return n

        def product_of_digits(x: int) -> int:
            prod = 1
            for ch in str(x):
                d = ord(ch) - 48
                if d == 0:
                    return 0
                prod *= d
            return prod

        x = n
        while True:
            prod = product_of_digits(x)
            if prod % t == 0:
                return x
            x += 1
```
- Notes:
  - Approach: simple brute-force search starting from n, compute digit product (with early return on digit 0) and check divisibility by t. Return the first valid number.
  - Time complexity: Let K be the number of integers checked until a valid one is found and let d be the number of digits of inspected numbers. Each check costs O(d) to compute the product, so O(K * d) time. Given the problem constraints (small n and t ≤ 10), this is efficient in practice.
  - Space complexity: O(1) extra space (ignoring input/output).