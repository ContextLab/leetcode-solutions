# [Problem 1411: Number of Ways to Paint N × 3 Grid](https://leetcode.com/problems/number-of-ways-to-paint-n-3-grid/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the number of ways to paint an n x 3 grid with 3 colors such that adjacent (horizontally or vertically) cells differ. For a single row of 3 cells, count how many valid colorings exists: 3 choices for first cell, 2 for second (different from first), and 2 for third (different from second) -> 3*2*2 = 12. But rows interact via vertical constraints, so we need to account for how one row's pattern restricts the next row.

It makes sense to categorize row patterns into types to simplify transitions. For a row of length 3 with adjacent distinctness, there are two pattern types:
- Type A ("ABA"): first and third cell have the same color (pattern like x,y,x).
- Type B ("ABC"): all three cells are pairwise different (x,y,z).

For n=1 we have 12 total: each of Type A and Type B has 6 patterns (3*2 for ABA and 3*2*1 for ABC). For subsequent rows we can count transitions from a previous row of type A or B to a next row of type A or B, derive recurrence, and iterate.

## Refining the problem, round 2 thoughts
We need to determine transition counts between types. Let A_i be number of ways up to row i ending in type A, and B_i be ways up to row i ending in type B. For i=1: A_1 = 6, B_1 = 6.

We compute how many ways to choose a next-row pattern of type A or B given a previous row of known pattern. Standard combinatorial derivation leads to:
- From previous A: next A choices = 3, next B choices = 2
- From previous B: next A choices = 2, next B choices = 2

Thus recurrences:
A_{i} = 3*A_{i-1} + 2*B_{i-1}
B_{i} = 2*A_{i-1} + 2*B_{i-1}

(Explanation: you can check by fixing previous row colors and counting valid choices for next row respecting vertical and horizontal constraints; these constants are well-known for the 3xN painting problem.)

We iterate for i from 2..n and compute modulo 1e9+7. Complexity O(n) time and O(1) space. n <= 5000 so it's trivial.

## Attempted solution(s)
```python
class Solution:
    def numOfWays(self, n: int) -> int:
        MOD = 10**9 + 7
        # Base counts for first row:
        # A: patterns with first and third equal (ABA) => 6
        # B: patterns with all three different (ABC) => 6
        a = 6  # count of type A after row 1
        b = 6  # count of type B after row 1

        if n == 1:
            return (a + b) % MOD

        for _ in range(2, n + 1):
            new_a = (3 * a + 2 * b) % MOD
            new_b = (2 * a + 2 * b) % MOD
            a, b = new_a, new_b

        return (a + b) % MOD
```
- Notes about the solution:
  - We group row patterns into two types (ABA and ABC) and derive a small-state linear recurrence for transitions between types.
  - Time complexity: O(n) — a simple loop up to n.
  - Space complexity: O(1) — only a few integer variables are maintained.
  - All arithmetic is done modulo 10^9 + 7 to avoid overflow.