# [Problem 628: Maximum Product of Three Numbers](https://leetcode.com/problems/maximum-product-of-three-numbers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share my stream-of-consciousness. Here's a concise summary instead:

Key observation: the maximum product of three numbers is either the product of the three largest numbers, or the product of the largest number and the two smallest numbers (because two negative numbers can make a positive). So track the top three maximums and the bottom two minimums (or sort the array) and compute the maximum of those two candidate products.

## Refining the problem, round 2 thoughts
Refinement and considerations:
- Two main approaches:
  - Sort the array and compare product of last three vs product of first two and last one. Sorting is simple: O(n log n) time, O(1) extra space (or O(n) depending on sort).
  - Single-pass scan to track max1, max2, max3 and min1, min2: O(n) time and O(1) space. This is optimal.
- Edge cases:
  - All negatives (e.g., [-1, -2, -3]) — the three largest (i.e., least negative) could be the maximum or the product of largest and two smallest may produce correct result; the formula covers this.
  - Zeros included — handled naturally by comparisons.
- Complexity:
  - Single-pass solution: O(n) time, O(1) space.

## Attempted solution(s)
```python
class Solution:
    def maximumProduct(self, nums: list[int]) -> int:
        # Track the three largest and two smallest values
        max1 = max2 = max3 = -float('inf')
        min1 = min2 = float('inf')
        
        for x in nums:
            # update maxima
            if x > max1:
                max3 = max2
                max2 = max1
                max1 = x
            elif x > max2:
                max3 = max2
                max2 = x
            elif x > max3:
                max3 = x
            
            # update minima
            if x < min1:
                min2 = min1
                min1 = x
            elif x < min2:
                min2 = x
        
        # compare product of three largest vs largest and two smallest
        return int(max(max1 * max2 * max3, max1 * min1 * min2))
```
- Notes:
  - This solution performs a single pass over nums and keeps constant extra state: the three largest and two smallest values.
  - Time complexity: O(n). Space complexity: O(1).
  - The final result is the maximum of product(max1, max2, max3) and product(max1, min1, min2), covering cases where two negatives produce a large positive product.