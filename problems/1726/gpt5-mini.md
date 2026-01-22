# [Problem 1726: Tuple with Same Product](https://leetcode.com/problems/tuple-with-same-product/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem asks for the number of 4-tuples (a, b, c, d) from distinct elements of nums such that a*b = c*d and all four entries are distinct. The array nums has distinct positive integers.

First thought: pairs of numbers produce products. If two different pairs produce the same product, we can form tuples by taking one pair as (a,b) and the other as (c,d). So I should count how many pairs produce each product, then combine pair counts for the same product.

I need to be careful about ordering: the tuple (a,b,c,d) is ordered, and within a pair the elements can be swapped. Also the two selected pairs can be assigned to (a,b) and (c,d) in two ways. So for each unordered pair-of-pairs there are multiple ordered 4-tuples.

Also ensure the four elements are distinct — but since nums has distinct values, two different pairs that share an element would imply equality of the other two (from product equality) and that can't happen with distinct numbers. So any two different pairs with the same product are disjoint.

Hence: count unordered pairs (i<j) by product. For a product with m pairs, number of ordered 4-tuples is 8 * C(m,2) = 4 * m * (m-1).

This suggests a straightforward O(n^2) solution: enumerate all pairs, count product frequencies, then sum the contribution for each product.

## Refining the problem, round 2 thoughts
- Confirm overlapping pairs: if pairs (x,y) and (x,z) had same product, then x*y = x*z -> y = z, but that would be the same pair, so different pairs with equal product must be disjoint. So no need to explicitly check disjointness.
- Implementation detail: iterate i from 0..n-1, j from i+1..n-1, update map[nums[i]*nums[j]].
- For each product with count m >= 2, add 8 * C(m,2) (or equivalently 4*m*(m-1)) to answer.
- Complexity: there are O(n^2) pairs, so time O(n^2). Space can be O(n^2) in worst case (distinct products for every pair), but typically smaller. For n up to 1000 this is fine (~500k pairs).

Edge cases:
- n < 4 -> result is 0.
- Large product up to 1e8 fits in Python int.

## Attempted solution(s)
```python
from collections import defaultdict
from typing import List

class Solution:
    def tupleSameProduct(self, nums: List[int]) -> int:
        n = len(nums)
        if n < 4:
            return 0

        prod_count = defaultdict(int)
        # Count products for all unordered pairs (i < j)
        for i in range(n):
            a = nums[i]
            for j in range(i+1, n):
                prod = a * nums[j]
                prod_count[prod] += 1

        ans = 0
        # For each product with m pairs, number of ordered tuples is 8 * C(m,2) = 4 * m * (m-1)
        for m in prod_count.values():
            if m > 1:
                ans += 4 * m * (m - 1)

        return ans
```
- Notes:
  - We iterate all unordered pairs (i < j) so each pair counted once.
  - For a product with m unordered pairs, choose any two distinct pairs in C(m,2) ways. For each such unordered choice, we can:
    - assign one pair to (a,b) and the other to (c,d) in 2 ways,
    - order the two elements inside each pair in 2 ways each (so 2 * 2 = 4),
    - total per unordered pair-of-pairs = 2 * 4 = 8 permutations.
    - So total = 8 * C(m,2) = 4 * m * (m - 1).
  - Time complexity: O(n^2) to enumerate pairs.
  - Space complexity: O(n^2) in worst-case to store product counts (number of distinct pair products).