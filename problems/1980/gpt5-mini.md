# [Problem 1980: Find Unique Binary String](https://leetcode.com/problems/find-unique-binary-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem gives n unique binary strings each of length n and asks for any binary string of length n not present in the array. My first naive thought is to try generating all 2^n binary strings and check membership (using a set) until I find one missing. That works for small n but is exponential and unnecessary here.

I recall a classic trick (Cantor's diagonal argument): construct a string that differs from the i-th given string at position i. That guarantees the new string differs from every given string in at least one position, so it cannot be any of them. This produces an answer in linear time (in n) relative to the number of output bits.

## Refining the problem, round 2 thoughts
- The diagonal construction is simple and deterministic: for each index i, set result[i] = flip(nums[i][i]) ('0' if '1', else '1').
- Edge cases: n >= 1, and inputs guarantee each string length is n and strings are unique — so diagonalization is safe.
- Alternative: brute-force generate all binaries and check membership (O(n * 2^n) in work) — feasible for n <= 16 but unnecessary with the diagonal method.
- Complexity: building the result requires O(n) steps; note that the input contains n strings of length n (size O(n^2) total stored characters), but the algorithm only inspects one character per string, so additional work is O(n). Space: O(n) for the returned string.

## Attempted solution(s)
```python
class Solution:
    def findDifferentBinaryString(self, nums: List[str]) -> str:
        """
        Diagonalization: construct a string that differs from nums[i] at position i.
        """
        # n = number of strings = length of each string
        n = len(nums)
        # build list of characters by flipping the diagonal bit nums[i][i]
        res_chars = []
        for i, s in enumerate(nums):
            # flip the character at position i
            res_chars.append('0' if s[i] == '1' else '1')
        return ''.join(res_chars)
```
- Notes:
  - Correctness: The constructed string differs from nums[i] at index i for all i, so it cannot match any string in nums.
  - Time complexity: O(n) steps to build the result (plus the input already occupying O(n^2) chars). We only inspect one char per input string.
  - Space complexity: O(n) additional space for the output (res_chars).