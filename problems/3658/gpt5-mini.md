# [Problem 3658: GCD of Odd and Even Sums](https://leetcode.com/problems/gcd-of-odd-and-even-sums/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see we need the GCD of two sums: sum of first n odd numbers and sum of first n even numbers. First thought: I could compute the sums directly and call math.gcd on them. But there's a known formula: sum of first n odd numbers is n^2, and sum of first n even numbers is 2*(1+...+n) = n*(n+1). So gcd(n^2, n*(n+1)) simplifies. Use gcd properties: gcd(n^2, n(n+1)) = n * gcd(n, n+1). And gcd(n, n+1) is always 1 because consecutive integers are coprime. So the result should simply be n. That is much simpler and O(1).

## Refining the problem, round 2 thoughts
Edge cases: n = 1 gives gcd(1,2) = 1 which matches n. For any n >= 1 the reasoning holds. Alternative approach (less optimal) is computing sums explicitly and using math.gcd — still fine given constraints (n up to 1000), but unnecessary. Time complexity with the derived formula is O(1) and space O(1). No overflow concerns for given constraints, but even for much larger n Python handles big integers.

## Attempted solution(s)
```python
# LeetCode style solution
class Solution:
    def gcdOfOddAndEvenSums(self, n: int) -> int:
        # Derived result: sumOdd = n^2, sumEven = n*(n+1)
        # gcd(n^2, n*(n+1)) = n * gcd(n, n+1) = n * 1 = n
        return n
```
- Notes:
  - Approach: Use closed-form sums and properties of gcd to simplify; consecutive integers are coprime.
  - Time complexity: O(1).
  - Space complexity: O(0) / O(1) (constant extra space).