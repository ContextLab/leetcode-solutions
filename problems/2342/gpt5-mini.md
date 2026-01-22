# [Problem 2342: Max Sum of a Pair With Equal Sum of Digits](https://leetcode.com/problems/max-sum-of-a-pair-with-equal-sum-of-digits/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need two numbers with equal sum-of-digits and want the maximum sum of such a pair. That suggests grouping numbers by their digit-sum. For each digit-sum group, the best pair is simply the two largest numbers in that group. So as I scan nums I can compute digit-sum and maintain the top two values for that sum. Then compute candidate sums from those top-two values and take the maximum. No need to keep entire lists or sort groups — just track two largest per key.

Edge-case: if a group has fewer than two elements, ignore it. Since nums length up to 1e5 and values up to 1e9, digit-sum computation is cheap (<=10 digits). Use a dictionary mapping digit-sum -> (largest, second_largest) or a small list.

## Refining the problem, round 2 thoughts
Alternative: collect values per digit-sum into lists and sort each list descending, but that costs extra memory and sorting time (though bounded by small number of possible digit-sums ~ 90). Better approach: single pass, update top two per sum in O(1) per number. Complexity will be O(n * digits-per-number) ~ O(n).

Corner cases:
- If a digit-sum occurs only once, skip it.
- If same number appears multiple times, that's fine — indices are distinct.
- All numbers positive so we can initialize top-two to -inf or None.

Time complexity: O(n * D) where D ~ 10 (digits) -> effectively O(n). Space complexity: O(K) where K is number of possible digit-sums (<= 9*10 = 90) or O(min(n,90)).

## Attempted solution(s)
```python
from typing import List
import collections

class Solution:
    def maximumSum(self, nums: List[int]) -> int:
        def digit_sum(x: int) -> int:
            s = 0
            while x:
                s += x % 10
                x //= 10
            return s
        
        # map digit_sum -> tuple (largest, second_largest)
        top_two = {}  # int -> [largest, second]
        ans = -1
        
        for num in nums:
            s = digit_sum(num)
            if s not in top_two:
                top_two[s] = [num, -1]  # second initialized to -1 (no value)
            else:
                a, b = top_two[s]
                # Insert num into top two if appropriate
                if num >= a:
                    top_two[s] = [num, a]
                elif num > b:
                    top_two[s][1] = num
        
        # Compute best sum among groups that have two valid entries
        for a, b in top_two.values():
            if b != -1:
                ans = max(ans, a + b)
        
        return ans
```
- Notes about the solution:
  - Approach: single pass grouping by digit-sum, maintaining the two largest values for each digit-sum. After the pass, compute the maximum sum among groups that have at least two numbers.
  - Time complexity: O(n * D) where D is number of digits per number (<= 10) — effectively O(n).
  - Space complexity: O(K) where K is number of distinct digit-sums (bounded, <= 90 for given constraints), plus O(1) extra.
  - Implementation details: digit_sum is implemented with a while loop (no string conversion) for slightly better performance. top_two stores [largest, second_largest] with second_largest = -1 marking absence.