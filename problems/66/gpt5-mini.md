# [Problem 66: Plus One](https://leetcode.com/problems/plus-one/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have an array of digits representing a positive integer (no leading zeros). We need to add one and return the resulting digits array. The straightforward approach is to simulate addition from the least significant digit (the end of the list) and propagate carries leftwards. If a digit is less than 9, we can increment it and return immediately. If it's 9, it becomes 0 and we continue carrying to the next more significant digit. If we exhaust all digits and still have a carry (e.g., [9,9,9]), we need to insert a leading 1 to represent the new most-significant digit (making [1,0,0,0]).

This is essentially an in-place modification from the end, with an exceptional case when all digits are 9.

## Refining the problem, round 2 thoughts
- Edge cases:
  - Single digit 9 -> [1,0].
  - Multiple 9s -> add leading 1.
  - No carry required (last digit != 9) -> just increment last and return.
- Alternatives:
  - Convert to integer, add one, convert back — but this is impractical for very large numbers and violates the spirit of the problem (and constraints might allow up to 100 digits; Python handles big ints but converting back and forth is unnecessary).
  - Work in-place from the end and return digits unless we need to prepend a 1 (only when all were 9).
- Complexity:
  - Time: O(n) in the worst case (we might need to visit every digit if they're all 9).
  - Space: O(1) extra space if modifying in-place, plus O(n) output in the worst case when we need to create a new list with an extra leading 1. This is optimal for this problem.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        """
        Increment the large integer represented by digits by one and return the resulting digits.
        """
        n = len(digits)
        # Process from least significant digit to most significant
        for i in range(n - 1, -1, -1):
            if digits[i] < 9:
                digits[i] += 1
                return digits
            # digit is 9 -> becomes 0 and carry continues
            digits[i] = 0
        # If we exit the loop, all digits were 9 and turned to 0. We need a leading 1.
        return [1] + digits
```
- Notes:
  - Approach: Iterate from the end; increment the first non-9 digit and return. If all digits are 9, return [1] + zeros (which is handled by returning [1] + digits after turning all to 0).
  - Time complexity: O(n) in the worst case, where n = len(digits).
  - Space complexity: O(1) extra space (in-place), except when all digits are 9 we construct a new list of size n+1 to represent the result (overall output size is O(n)).