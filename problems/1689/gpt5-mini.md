# [Problem 1689: Partitioning Into Minimum Number Of Deci-Binary Numbers](https://leetcode.com/problems/partitioning-into-minimum-number-of-deci-binary-numbers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
If each deci-binary number's digits are only 0 or 1, summing k such numbers column-wise (digit-wise) yields in each digit position a value between 0 and k (inclusive). To form the input number n, for every digit d in n we need k >= d (because the sum of the bits in that column must equal the digit d). That suggests the minimum k must be at least the maximum digit in n. Can we always achieve k equal to that maximum digit? Intuitively yes: we can construct max_digit deci-binary numbers by distributing 1s across them so each column sums to the required digit. So the answer should be the maximum digit in the string. No need for complicated DP or greedy construction beyond this observation.

## Refining the problem, round 2 thoughts
Refined approach: scan the string n and find the largest character (digit) and convert to int; that's the result. Edge cases: n length up to 1e5, but a single pass is O(n) and memory O(1). n has no leading zeros and is non-empty, so max digit is at least 1. Alternative (less efficient/unnecessary) approaches could build the actual deci-binary numbers; not needed for just the count. Time complexity: O(len(n)). Space: O(1) extra. Implementation detail: get max of characters then subtract '0' or map to int.

## Attempted solution(s)
```python
class Solution:
    def minPartitions(self, n: str) -> int:
        # The minimum number of deci-binary numbers required is the maximum digit in n.
        # Because each deci-binary number contributes at most 1 to any digit position,
        # to form a digit d we need at least d such numbers. Taking the maximum digit
        # across all positions yields the minimum required count.
        return max(map(int, n))
```
- Notes:
  - Approach: return the maximum digit in the string n.
  - Correctness: For any digit d in n, at least d deci-binary numbers are required (since each contributes at most 1 in that position). Construction achieving k = max_digit is possible by distributing 1s across k deci-binary numbers for each column.
  - Time complexity: O(len(n)) — single pass to find max.
  - Space complexity: O(1) extra (excluding input), or O(len(n)) if map produces an iterator depending on implementation; practically constant additional memory.