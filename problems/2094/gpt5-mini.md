# [Problem 2094: Finding 3-Digit Even Numbers](https://leetcode.com/problems/finding-3-digit-even-numbers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to form all unique 3-digit even numbers using elements from the given digits array, respecting the multiplicity of digits in the array. Requirements: no leading zero (hundreds digit != 0), and last digit must be even. The array can contain duplicates, and I can use the same digit multiple times only if it appears multiple times. 

Brute force idea: try every triple of indices (i, j, k) with i, j, k distinct, build the number digits[i]*100 + digits[j]*10 + digits[k], check even and hundreds != 0, and collect unique results in a set. That would be O(n^3) over indices, but n ≤ 100 so 1e6 iterations — acceptable. But there's a simpler and faster constant-time approach by using counts of digits (0..9) and trying hundreds in 1..9, tens in 0..9, units among even digits, checking counts constraints. That reduces checks to at most 9*10*5 = 450 combinations.

I should be careful to decrement/restore counts when reusing digits to simulate taking distinct elements respecting multiplicity.

## Refining the problem, round 2 thoughts
Refinement:
- Use a frequency array counts[0..9] = number of occurrences in input.
- Loop hundreds digit h from 1..9 where counts[h] > 0 (no leading zero).
- Decrement counts[h], then loop tens digit t from 0..9 where counts[t] > 0, decrement counts[t], then loop units u over even digits (0,2,4,6,8) where counts[u] > 0. If available, form number and add to result.
- Restore counts after each nested loop level.
- This ensures we never use a digit more times than it appears.
- Finally return sorted list of unique numbers.

Edge cases:
- If there are no even digits in the input -> empty result.
- If all candidates would require using a digit more times than available (e.g., only one '2' but trying to make 222) will be naturally avoided by counts checks.
- Duplicates in input handled by counts.

Complexity:
- Time: O(1) with small constant (max 9*10*5 iterations) — effectively O(1) relative to input size but O(1) with respect to digits values; building counts is O(n).
- Space: O(1) extra (counts of size 10) plus output size.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findEvenNumbers(self, digits: List[int]) -> List[int]:
        # Build frequency count of digits 0..9
        counts = [0] * 10
        for d in digits:
            counts[d] += 1

        result = []
        # hundreds digit: 1..9 (no leading zero)
        for h in range(1, 10):
            if counts[h] == 0:
                continue
            counts[h] -= 1
            # tens digit: 0..9
            for t in range(0, 10):
                if counts[t] == 0:
                    continue
                counts[t] -= 1
                # units digit must be even
                for u in (0, 2, 4, 6, 8):
                    if counts[u] > 0:
                        num = h * 100 + t * 10 + u
                        result.append(num)
                counts[t] += 1
            counts[h] += 1

        result.sort()
        return result
```
- Notes:
  - Approach: use frequency counts and try all valid (hundreds, tens, units) combinations while respecting counts by decrementing/restoring.
  - Time complexity: O(n) to build counts + O(1) fixed nested loops (at most 9*10*5 checks) = effectively O(n). Space complexity: O(1) extra (counts array of size 10) plus output list.
  - Implementation details: careful decrementing/restoring of counts ensures digits are not reused beyond their multiplicity. The final result is sorted to meet the problem requirement.