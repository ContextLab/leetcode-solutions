# [Problem 40: Combination Sum II](https://leetcode.com/problems/combination-sum-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see this is a classic backtracking / combination generation problem where each candidate can be used at most once and we must avoid duplicate combinations. The immediate idea: sort the candidates so equal numbers are adjacent; then do a DFS/backtracking that picks or skips each candidate, but when iterating in one recursion level skip duplicates (i > start and candidates[i] == candidates[i-1]) to avoid generating identical combinations. Also, sorting allows pruning: once a candidate exceeds the remaining target, break the loop. Because target is small (<= 30) and candidates are small (<= 50), pruning will be effective. Need to ensure we pass i+1 when recursing since each number can be used only once.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- If candidates list is empty (not in constraints, but handle gracefully) -> return [].
- If target is 0 (not in constraints either) -> return [[]] if allowed; for this problem target >=1 so not a concern.
- Duplicates in candidates are the main complication; sorting + skipping duplicates at the same recursion level (i > start and candidates[i] == candidates[i-1]) handles that.
- Complexity: worst-case exponential because we explore subsets. Sorting costs O(n log n). Backtracking generates combinations with pruning; worst-case ~O(2^n) time, but practical cost is much lower given target bounds.
- Alternative approaches: using counting of values (value->count) and choosing how many of each to include; that can also avoid duplicates but is more work and unnecessary here.

I'll implement a standard sorted backtracking solution with early pruning and duplicate skipping.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        res = []
        path = []
        n = len(candidates)
        
        def backtrack(start: int, remain: int):
            if remain == 0:
                res.append(path.copy())
                return
            # iterate candidates starting from 'start'
            for i in range(start, n):
                # skip duplicates at the same recursion level
                if i > start and candidates[i] == candidates[i - 1]:
                    continue
                val = candidates[i]
                # pruning: if current value exceeds remaining target, no need to proceed further
                if val > remain:
                    break
                # choose candidates[i]
                path.append(val)
                backtrack(i + 1, remain - val)  # i+1 because each number can be used only once
                path.pop()
        
        backtrack(0, target)
        return res
```
- Notes about the solution approach:
  - We sort the input to make it easy to skip duplicates and to prune the search early.
  - The recursion explores combinations by choosing each candidate at most once (hence backtrack(i+1, ...)).
  - The check "if i > start and candidates[i] == candidates[i-1]" ensures we don't start a branch with the same number multiple times at the same recursion depth, which removes duplicate combinations.
  - Complexity:
    - Time: O(n log n) for sorting plus the backtracking exploration. The backtracking is exponential in the worst case — roughly O(2^n) subsets — but pruning (value > remaining target) and the small target bound often reduce actual work significantly.
    - Space: O(n) recursion depth (plus O(k) for each combination stored in the worst case), so O(n) auxiliary space aside from the output.