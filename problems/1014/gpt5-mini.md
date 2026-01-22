# [Problem 1014: Best Sightseeing Pair](https://leetcode.com/problems/best-sightseeing-pair/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I notice the score for a pair (i < j) is values[i] + values[j] + i - j. That can be rearranged as (values[i] + i) + (values[j] - j). That suggests we can treat the problem as, for each j, we want the maximum possible (values[i] + i) for i < j, then add (values[j] - j). A brute force O(n^2) would check all pairs, but rearranging gives a way to compute the best earlier term incrementally. So a single pass maintaining the best (values[i] + i) seen so far should suffice.

## Refining the problem, round 2 thoughts
We should iterate j from 1 to n-1, maintain best_prefix = max(values[i] + i) for i < j. At each j compute candidate = best_prefix + values[j] - j and update global answer. Then update best_prefix with values[j] + j for future j's. Edge cases: values length >= 2 so loop will run; initialize best_prefix with values[0] + 0. Time complexity O(n), space O(1). Alternative is dynamic programming / segment tree but unnecessary. This is clean and optimal.

## Attempted solution(s)
```python
class Solution:
    def maxScoreSightseeingPair(self, values: list[int]) -> int:
        # Initialize best (values[i] + i) with i = 0
        best_i = values[0] + 0
        # Initialize answer with a very small number
        best_score = float('-inf')
        # Iterate j from 1 to n-1
        for j in range(1, len(values)):
            # Candidate score using the best previous (values[i] + i)
            candidate = best_i + values[j] - j
            if candidate > best_score:
                best_score = candidate
            # Update best_i to consider i = j for future j's
            val_plus_index = values[j] + j
            if val_plus_index > best_i:
                best_i = val_plus_index
        return best_score
```
- Notes:
  - Approach: use the identity values[i] + values[j] + i - j = (values[i] + i) + (values[j] - j). Maintain the maximum (values[i] + i) seen so far while scanning j.
  - Time complexity: O(n), where n = len(values), because we do a single pass.
  - Space complexity: O(1), only constant extra variables used.
  - Implementation detail: initialize best_i = values[0] + 0 and iterate j starting from 1. Initialize best_score to -inf to handle all possible inputs safely.