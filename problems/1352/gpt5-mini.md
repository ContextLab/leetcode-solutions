# [Problem 1352: Product of the Last K Numbers](https://leetcode.com/problems/product-of-the-last-k-numbers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to support two operations: add(num) and getProduct(k). A naive getProduct(k) would multiply the last k numbers each time, which would be O(k) and could be too slow if k is large and many queries. Observing that products of contiguous suffixes can be computed quickly if we maintain prefix products: product(i...j) = pref[j] / pref[i-1]. But zeros break multiplicative inverses (division by zero) and reset the product state. So handle zeros by resetting prefix-products after each zero. That suggests keeping a list of prefix products where we start with 1; on add(num) if num == 0 we reset the list to [1]; otherwise append pref[-1] * num. For getProduct(k), if k is more than current length-1 (meaning a zero exists within the last k numbers), return 0; otherwise return pref[-1] // pref[-1-k].

## Refining the problem, round 2 thoughts
Confirm edge cases: many zeros interspersed — resetting prefix on zero is correct. Using integer division (//) is safe because prefixes are exact integer products and input numbers are ints (0..100). Complexity: both operations are O(1) time. Space is O(n) where n is number of adds since last zero (we only keep prefixes since last zero); worst-case O(total adds) without zeros. Alternative solutions include segment trees or maintaining a sliding window of last k numbers, but prefix-products with reset on zero is simplest and gives O(1) ops.

## Attempted solution(s)
```python
class ProductOfNumbers:
    def __init__(self):
        # prefix[i] = product of all numbers added since the last zero, up to i (prefix[0] = 1)
        self.prefix = [1]

    def add(self, num: int) -> None:
        if num == 0:
            # reset when zero is added; any product that spans this zero should be zero
            self.prefix = [1]
        else:
            self.prefix.append(self.prefix[-1] * num)

    def getProduct(self, k: int) -> int:
        # if k is larger than number of stored numbers since last zero, there was a zero inside last k numbers
        if k >= len(self.prefix):
            return 0
        # product of last k numbers = prefix[-1] // prefix[-1-k]
        return self.prefix[-1] // self.prefix[-1 - k]
```
- Notes about the solution:
  - Approach: Maintain a running list of prefix products since the last zero. Reset the list when a zero is added. Use integer division of two prefix products to get product of last k numbers in O(1).
  - Time complexity: add — O(1), getProduct — O(1).
  - Space complexity: O(n) in the worst case where n is the number of add calls since the last zero (overall O(total adds) across the lifetime, as previous prefixes before zeros are discarded).
  - Implementation details: prefix[0] = 1 simplifies computation. When k >= len(prefix) it implies a zero occurred within the last k numbers so return 0. Integer division // is exact here because prefix values are integer products.