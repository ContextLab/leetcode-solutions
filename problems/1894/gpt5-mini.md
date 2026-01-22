# [Problem 1894: Find the Student that Will Replace the Chalk](https://leetcode.com/problems/find-the-student-that-will-replace-the-chalk/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem describes students repeatedly consuming chalk in order; if remaining chalk is strictly less than the current student's requirement, that student must replace the chalk. A straightforward simulation would repeatedly subtract chalk[i] from k while cycling through students until k < chalk[i]. But k can be large (up to 1e9) and would cause many full cycles if done naively.

I notice the process is periodic: one full round uses sum(chalk) pieces. After as many full rounds as possible, only the remainder matters. So taking k modulo total_sum should reduce the problem to at most one pass over the array. Another approach is to build prefix sums and do a binary search for the first prefix > k (after modulo) which gives O(n) preprocessing and O(log n) search — but for a single query the simple one-pass after modulo is optimal and simple.

Also be careful about the case where k % total_sum == 0: then the remainder is 0, and the first student with chalk[i] > 0 (which is always student 0 because chalk[i] >=1) will be the replacer — this follows naturally from the modulo approach.

## Refining the problem, round 2 thoughts
Refinements / edge cases:
- If sum(chalk) > k originally, modulo leaves k unchanged and we still just find the first i with chalk[i] > k.
- If sum(chalk) divides k exactly, k % sum = 0 and we'll return the first index whose chalk requirement is > 0 (student 0), which matches the specification.
- Watch out for large sums (sum can be up to ~1e10 in worst case), but Python handles big ints; in languages with fixed-width ints use 64-bit.
- Time complexity target: O(n) and O(1) extra space (besides input). Alternative prefix-sum + binary search yields O(n) time and O(n) space but is not necessary for a single query.

Approach: compute total = sum(chalk), reduce k = k % total, iterate through chalk subtracting until chalk[i] > k, return i.

## Attempted solution(s)
```python
class Solution:
    def chalkReplacer(self, chalk: list[int], k: int) -> int:
        total = sum(chalk)
        k %= total  # only the remainder after full cycles matters
        for i, c in enumerate(chalk):
            if k < c:
                return i
            k -= c
        # In theory we should always return inside the loop because k < total
        # and sum(chalk) == total, but include a fallback.
        return -1
```
- Notes:
  - Approach: compute total sum and reduce k by modulo; then perform a single pass to find the first student whose requirement exceeds the remaining k.
  - Time complexity: O(n) where n = len(chalk) (summing and one pass).
  - Space complexity: O(1) extra space.
  - This handles all edge cases including k >= sum(chalk) and k % sum(chalk) == 0.