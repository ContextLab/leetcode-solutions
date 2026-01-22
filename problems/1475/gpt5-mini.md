# [Problem 1475: Final Prices With a Special Discount in a Shop](https://leetcode.com/problems/final-prices-with-a-special-discount-in-a-shop/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need, for each price at index i, the first later index j > i such that prices[j] <= prices[i]. That is exactly a "next smaller-or-equal element to the right" problem. The naive approach is for each i scan j = i+1..n-1 until finding such a j — that's O(n^2) in worst case. A classic improvement is to use a monotonic stack of indices to find next smaller-or-equal elements in O(n) time: iterate once from left to right, and when you see a price that is <= price at the index on top of the stack, you pop and record the discount for that popped index. Push current index afterward. At the end any index left in the stack has no discount.

## Refining the problem, round 2 thoughts
- Edge cases: length 1 should return the same single price. If array is strictly increasing no discounts apply.
- Using a stack of indices keeps memory O(n) and allows computing discounts on the fly.
- Implementation detail: initialize answer as a copy of prices, then subtract the discount when found.
- Time complexity: O(n) because each index is pushed and popped at most once. Space complexity: O(n) for the stack and answer array.
- Alternative: brute force O(n^2) which is simple but unnecessary given constraints (n up to 500 it's okay but monotonic stack is cleaner and scalable).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def finalPrices(self, prices: List[int]) -> List[int]:
        n = len(prices)
        ans = prices[:]  # start with original prices, will subtract discounts when found
        stack = []  # will store indices whose discount hasn't been found yet

        for i, price in enumerate(prices):
            # While current price is a valid discount for items in stack (prices[i] <= prices[idx])
            while stack and price <= prices[stack[-1]]:
                idx = stack.pop()
                ans[idx] = prices[idx] - price
            stack.append(i)

        # remaining indices in stack have no discount; ans already holds original prices for them
        return ans
```
- Approach: monotonic stack of indices holding items waiting for their first later price <= current. When such a price is found we set ans[idx] = prices[idx] - prices[current].
- Time complexity: O(n) — each index is pushed once and popped at most once.
- Space complexity: O(n) worst-case for the stack and O(n) for the answer (output).
- This is cleaner and faster than the brute-force O(n^2) scan-for-each approach.