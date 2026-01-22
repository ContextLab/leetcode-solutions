# [Problem 1593: Split a String Into the Max Number of Unique Substrings](https://leetcode.com/problems/split-a-string-into-the-max-number-of-unique-substrings/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to split the string into non-empty contiguous substrings so that all substrings are unique and the number of pieces is maximized. This smells like backtracking / DFS over possible cut positions: at each index choose an end for the next substring, skip it if that substring has already been used, otherwise recurse. The string length limit is 16, which is small enough for an exponential/backtracking approach.

Potential pruning: each remaining character can be at best its own substring (length 1), so the maximum extra pieces from position i is (n - i). If current_count + (n - i) <= best_answer so far, we can prune that branch. Also using a set to track used substrings is straightforward.

Edge cases: all same characters => only 1 piece. Unique characters => can split into n pieces.

## Refining the problem, round 2 thoughts
Refinements:
- Use recursion with a set of used substrings and an index start.
- For each recursive call, try substrings s[start:i] for i in range(start+1, n+1). If substring not in used, add and recurse.
- Maintain a global or nonlocal best (max count).
- Add pruning: if current_count + (n - start) <= best, then even in the best-case we cannot beat best so stop.
- Complexity: worst-case branching can be large, but n <= 16 keeps this acceptable.

Alternative ideas: bitmasking or dynamic programming are possible, but the straightforward backtracking with the simple prune is clean and efficient for n <= 16.

Corner cases to consider: repeated substrings, overlapping choices, correctness of prune (must be safe).

## Attempted solution(s)
```python
class Solution:
    def maxUniqueSplit(self, s: str) -> int:
        n = len(s)
        best = 0
        
        def dfs(start: int, used: set, count: int):
            nonlocal best
            # prune: even if we split every remaining char individually,
            # if we can't beat best, stop
            if count + (n - start) <= best:
                return
            if start == n:
                best = max(best, count)
                return
            for end in range(start + 1, n + 1):
                sub = s[start:end]
                if sub in used:
                    continue
                used.add(sub)
                dfs(end, used, count + 1)
                used.remove(sub)
        
        dfs(0, set(), 0)
        return best
```
- Approach: depth-first search trying all possible next substrings, tracking used substrings in a set to ensure uniqueness. Pruning uses the fact that at most (n - start) one-character substrings can be added.
- Time complexity: exponential in n in the worst case; an upper-bound is roughly O(n * 2^n) due to exploring many partitionings (but n <= 16 makes this feasible). The pruning reduces many branches in practice.
- Space complexity: O(n^2) for the set of substrings in worst case (sum of lengths of stored substrings) and O(n) recursion depth.