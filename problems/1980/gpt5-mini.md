# [Problem 1980: Find Unique Binary String](https://leetcode.com/problems/find-unique-binary-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I recall this is a classic Cantor-diagonalization style problem: given n unique binary strings of length n, you can construct a new string that differs from the i-th string at position i, so it cannot be equal to any string in the list. The first idea that comes to mind is to flip the diagonal bits: for each i take nums[i][i] and put the opposite bit in the answer. That produces a length-n binary string for sure and guarantees uniqueness. There's also the brute-force option of enumerating all 2^n binary strings and picking one not in the set (works since n ≤ 16), but diagonal method is O(n) and simpler.

## Refining the problem, round 2 thoughts
The diagonal approach needs careful indexing (0-based). Edge cases: n = 1 still works (flip the single bit). Because the strings in nums are unique, we don't need to worry about duplicates. Complexity: we only need to read one character from each string (nums[i][i]), so runtime is O(n) (we produce an output of length n). Space: O(n) for the output string (plus input). Alternative: build a set of nums and iterate all possible bitstrings (2^n) — feasible here (n ≤ 16) but worse asymptotically and unnecessary.

## Attempted solution(s)
```python
class Solution:
    def findDifferentBinaryString(self, nums: list[str]) -> str:
        # Flip the diagonal bit nums[i][i] for each i
        n = len(nums)
        res_chars = []
        for i in range(n):
            # nums[i][i] is either '0' or '1'
            res_chars.append('1' if nums[i][i] == '0' else '0')
        return ''.join(res_chars)
```
- Notes:
  - Approach: Cantor diagonalization — construct string s where s[i] != nums[i][i]. This ensures s differs from every nums[i] at index i, so s is not in nums.
  - Time complexity: O(n), where n = nums.length (we access exactly one character from each string and build an answer of length n).
  - Space complexity: O(n) for the output string (plus input). The algorithm uses O(n) extra space for the result list; no additional data structures required.
  - Alternative: generate all 2^n strings and pick one not in nums (time O(2^n * n) in worst case), which is acceptable for n ≤ 16 but inferior to the diagonal construction.