# [Problem 1780: Check if Number is a Sum of Powers of Three](https://leetcode.com/problems/check-if-number-is-a-sum-of-powers-of-three/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I recognize the problem: we need to decide whether n can be written as a sum of distinct powers of 3 (each power at most once). That is exactly like representing n in base-3 (ternary): each ternary digit corresponds to how many times that power of 3 is used. If all ternary digits are 0 or 1, we can represent n as a sum of distinct powers of 3; if any digit is 2 (or larger, but base-3 digits are 0..2), it's impossible because that would require using the same power twice. So a direct check of the base-3 representation works. Implementation can be done by repeatedly taking n % 3 and dividing by 3.

Other options: greedy subtract the largest power repeatedly or precompute powers and try subset-sum / bitmasking — but base-3 check is simplest and O(log n).

## Refining the problem, round 2 thoughts
Edge cases: n >= 1 by constraints, so no need to handle zero or negatives specially (if zero appeared, the algorithm would also return True since no powers needed). A subtle thought: could a digit 2 be compensated by carrying (like represent 2*3^k as 3^(k+1) - 3^k etc.)? No — we are restricted to nonnegative distinct powers only, so a digit 2 cannot be realized by other distinct powers without reusing powers or using negative coefficients. Thus checking for any remainder 2 suffices.

Time complexity: number of iterations is O(log_3 n) = O(log n). Space: O(1). This is optimal and trivial to implement.

## Attempted solution(s)
```python
class Solution:
    def checkPowersOfThree(self, n: int) -> bool:
        """
        Return True if n can be represented as a sum of distinct powers of three.
        Equivalent to checking that the base-3 representation of n contains only 0s and 1s.
        """
        while n > 0:
            if n % 3 == 2:
                return False
            n //= 3
        return True
```
- Notes:
  - Approach: check ternary digits by repeated modulo/divide by 3. If any digit equals 2, return False; otherwise True.
  - Time complexity: O(log_3 n) = O(log n).
  - Space complexity: O(1).
  - This is simple, efficient, and handles the problem constraints directly.