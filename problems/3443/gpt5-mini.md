# [Problem 3443: Maximum Manhattan Distance After K Changes](https://leetcode.com/problems/maximum-manhattan-distance-after-k-changes/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are walking on a grid following string s; at each prefix (after some number of moves) we have position (x,y) and Manhattan distance |x|+|y|. We are allowed to change up to k characters anywhere in the whole string, but if we care about the maximum Manhattan distance achieved "at any time", only changes to moves up to a given prefix affect that prefix's position. So we can consider each prefix independently: given the first m moves, what is the largest Manhattan distance reachable at time m if we can change at most k of those m moves?

Each change replaces one unit vector by another unit vector. Intuitively, a single change can increase the Manhattan distance by at most 2 (flip a move that was moving toward origin to the opposite direction). Also the maximum possible Manhattan after m moves cannot exceed m (all moves in one direction). So for a given prefix m with original current Manhattan D = |x|+|y|, the best possible is at most min(m, D + 2*k). That suggests scanning prefixes, computing D for each, and using min(prefix_length, D + 2*k) as the achievable max at that prefix.

I need to be sure this bound is achievable (not only an upper bound) — but we only need the maximum over prefixes, and constructing changes greedily (flip moves that hurt the most or flip to align directions) can realize increases up to +2 per change until hitting the prefix length limit.

## Refining the problem, round 2 thoughts
- For each prefix i (0-indexed), compute x,y after i+1 moves.
- Original manhattan D = |x| + |y|.
- With up to k changes among those i+1 moves, achievable = min(i+1, D + 2*k).
  - Reasoning: each change can increase D by at most 2; so D + 2*k is an upper bound. Also you can't exceed i+1 since the sum of absolute coordinates with i+1 unit moves is at most i+1. These two bounds yield min(i+1, D + 2*k).
  - Achievability: if D + 2*k >= i+1 then we can (theoretically) make all moves point the same way (or otherwise arrange moves) with ≤ k changes; if not, we can use up to k changes to flip moves that decrease the distance (or to flip in the best way) each giving up to +2, reaching D + 2*k. (This is the core intuitive argument used by accepted solutions.)
- Complexity: single pass over s computing x,y and updating answer O(n) time, O(1) extra space.

Edge cases:
- k = 0 simply returns maximum prefix original manhattan.
- Large k is capped by prefix length; no overflow issues.

I'll implement a straightforward loop.

## Attempted solution(s)
```python
class Solution:
    def maxDistance(self, s: str, k: int) -> int:
        """
        For each prefix, compute the original Manhattan distance D = |x|+|y|.
        With up to k changes among the prefix moves, the maximal reachable Manhattan
        distance at that time is min(prefix_len, D + 2*k).
        Return the maximum over all prefixes.
        """
        x = 0
        y = 0
        ans = 0
        for i, ch in enumerate(s):
            if ch == 'N':
                y += 1
            elif ch == 'S':
                y -= 1
            elif ch == 'E':
                x += 1
            elif ch == 'W':
                x -= 1
            curr = abs(x) + abs(y)
            # prefix length is i+1
            achievable = min(i + 1, curr + 2 * k)
            if achievable > ans:
                ans = achievable
        return ans
```
- Notes about the approach:
  - We iterate once through the string, maintaining current (x,y) for the prefix.
  - For each prefix we compute the best achievable Manhattan distance given k changes as min(length_of_prefix, current_manhattan + 2*k).
  - Time complexity: O(n) where n = len(s).
  - Space complexity: O(1) extra space.
  - This uses the observation that each single-character change can increase the Manhattan distance by at most 2, and the absolute upper bound for m moves is m. Combining those gives the achievable bound used.