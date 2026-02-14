# [Problem 799: Champagne Tower](https://leetcode.com/problems/champagne-tower/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is a classic DP / simulation problem: we pour some amount into the top glass, each glass can hold 1 cup, and any excess splits equally to the two glasses below. The structure is triangular and small (query_row < 100), so simulating the flow row by row is straightforward. I can model amounts in each glass as floats and propagate overflow downwards. I should be careful to only propagate the amount above 1 (the capacity). A 1D DP per row (creating a new array for the next row) is enough; no need for a full 2D table. Edge cases: poured < 1 (top not full), poured huge (many glasses full, but we clamp answer to 1), query indices on bounds.

## Refining the problem, round 2 thoughts
Refinement: initialize an array dp where dp[j] is current amount in glass j at the current row. Start dp[0] = poured. For each row r from 0 to query_row-1, compute next row's amounts by iterating j from 0..r: if dp[j] > 1, overflow = (dp[j] - 1) / 2, add overflow to next[j] and next[j+1]. After processing up to query_row, dp will represent amounts in that query_row; answer is min(1, dp[query_glass]). Time complexity is O(query_row^2) (<= 100^2), space O(query_row). This is fast enough for constraints. One could also derive a combinatorial formula using binomial coefficients to compute contribution from the top to a specific glass, but DP is simpler and robust.

Corner cases: poured = 0, query_row = 0, query_glass = 0. Large poured (up to 1e9) is fine with float accumulation here; final value clamped to 1. Floating precision is adequate for LeetCode's checking tolerance.

## Attempted solution(s)
```python
class Solution:
    def champagneTower(self, poured: int, query_row: int, query_glass: int) -> float:
        # dp[j] = amount in glass j at the current row
        dp = [0.0] * (query_row + 1)
        dp[0] = float(poured)
        
        for r in range(query_row):
            next_row = [0.0] * (query_row + 1)
            for j in range(r + 1):
                if dp[j] > 1.0:
                    overflow = (dp[j] - 1.0) / 2.0
                    next_row[j] += overflow
                    next_row[j + 1] += overflow
            dp = next_row
        
        return min(1.0, dp[query_glass])
```
- Notes:
  - Approach: row-by-row simulation of overflow using a 1D DP array; each glass passes only the amount above 1 equally to its two children.
  - Time complexity: O(query_row^2) because we iterate rows up to query_row and each row processes up to r+1 glasses. With query_row < 100 this is trivial.
  - Space complexity: O(query_row) for the DP arrays.
  - Implementation details: we use a fresh next_row for each row to avoid overwriting amounts that still need processing in the same row. The final returned value is clamped with min(1.0, ...) since a glass cannot hold more than 1 cup. Floating-point precision is sufficient for the problem's tolerance.