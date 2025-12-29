# [Problem 756: Pyramid Transition Matrix](https://leetcode.com/problems/pyramid-transition-matrix/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to build a pyramid from a given bottom string up to a single top letter. Each adjacent pair in a row determines (via allowed patterns) what letters can appear above them. That suggests a backtracking / DFS search: given the current row, enumerate all possible rows above it (consistent with allowed patterns), and recursively try to build further until length 1. To make enumeration fast, precompute a mapping from bottom-pair (two letters) to the list of allowed top letters. Since choices multiply, memoization of failed bottoms (or successful ones) will prune repeated work. The bottom length is at most 6, so depth is small (<=5), but branching could be up to 6 per pair (since alphabet size is {A..F}), so worst-case states are manageable with pruning.

## Refining the problem, round 2 thoughts
- Build a dict: key = pair of chars (string of length 2), value = list (or set) of top letters allowed.
- DFS function that takes a current row (string). If length == 1, return True.
- To form the next row, for each adjacent pair in current row, get candidate tops; if any pair has no candidates, this branch is impossible.
- Use a helper to generate all possible next-row strings via backtracking on positions (cartesian product of candidate lists) and for each complete candidate next-row, recurse.
- Memoize bottoms that are proven impossible to reach the top (store them in a set) to avoid re-exploring identical states.
- Edge cases: allowed may be empty -> immediately false unless bottom length == 1 (but constraints say bottom length >=2). Also allowed strings are unique, so no duplicates to worry about.
- Time complexity: worst-case branching roughly O(k^(n)) where n is bottom length, k <= 6 (alphabet size). But with memoization and small n (<=6), it's fine. Space: recursion depth <= 6 and memo stores strings up to length 6.

## Attempted solution(s)
```python
from typing import List, Dict, Set

class Solution:
    def pyramidTransition(self, bottom: str, allowed: List[str]) -> bool:
        # Build mapping from pair -> list of possible tops
        mp: Dict[str, List[str]] = {}
        for s in allowed:
            pair = s[:2]
            top = s[2]
            if pair not in mp:
                mp[pair] = []
            mp[pair].append(top)

        # Memoization for bottoms that cannot reach the top
        failed: Set[str] = set()

        def dfs(curr: str) -> bool:
            # If we've reached the top
            if len(curr) == 1:
                return True
            if curr in failed:
                return False

            # For each adjacent pair, fetch candidate tops
            # If any pair has no candidates, this bottom is impossible
            n = len(curr)
            candidates = []
            for i in range(n - 1):
                pair = curr[i:i+2]
                if pair not in mp:
                    failed.add(curr)
                    return False
                candidates.append(mp[pair])

            # Backtracking to build next row from candidates lists
            next_row_chars = []

            def build_next(pos: int) -> bool:
                if pos == len(candidates):
                    next_row = ''.join(next_row_chars)
                    if dfs(next_row):
                        return True
                    return False
                for ch in candidates[pos]:
                    next_row_chars.append(ch)
                    if build_next(pos + 1):
                        return True
                    next_row_chars.pop()
                return False

            # If no possible construction leads to the top, memoize and return False
            if not build_next(0):
                failed.add(curr)
                return False
            return True

        return dfs(bottom)
```
- Notes:
  - Approach: recursive DFS with backtracking to construct all possible next rows, using a map from pairs to allowed top letters and a memo set to prune failing bottoms.
  - Time complexity: worst-case exponential in bottom length (rough upper bound O(k^(n)) where k <= 6 and n = len(bottom)), but n <= 6 and memoization prunes repeated states. Practically efficient under given constraints.
  - Space complexity: recursion depth O(n), plus memo storing failed bottoms (each <= length 6).