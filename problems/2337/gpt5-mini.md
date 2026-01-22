# [Problem 2337: Move Pieces to Obtain a String](https://leetcode.com/problems/move-pieces-to-obtain-a-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have pieces 'L' that can only move left into '_' and 'R' that can only move right into '_'. Intuitively, the relative sequence of pieces (ignoring '_') must be identical in start and target because pieces cannot pass each other (an 'L' can't pass an 'R' or vice-versa by the allowed moves). So first check that the sequence of non-'_' chars matches.

Beyond that, each piece has position constraints: an 'L' in start at index i can only move left to indices <= i, so in target its index j must satisfy j <= i (equivalently i >= j). An 'R' in start at i can only move right, so j must satisfy j >= i (i <= j). If any piece violates this, it's impossible. So iterate through both strings skipping '_' and check type and index constraints.

This suggests a two-pointer O(n) scan.

## Refining the problem, round 2 thoughts
Edge cases: different counts of 'L'/'R' obviously false. A scenario where one string has extra pieces unmatched will be caught by pointer end-checks. Careful with the inequality directions for 'L' and 'R' (they're opposite). Also ensure we handle the case when one pointer reaches end earlier.

Time complexity is O(n) because we do a single pass and skip underscores quickly. Space complexity O(1) extra (aside from input).

Alternative approaches like building lists of positions of L/R are equivalent; two-pointer is memory-light and simple.

## Attempted solution(s)
```python
class Solution:
    def canChange(self, start: str, target: str) -> bool:
        n = len(start)
        i = 0  # pointer for start
        j = 0  # pointer for target

        while i < n or j < n:
            # move i to next non-'_'
            while i < n and start[i] == '_':
                i += 1
            # move j to next non-'_'
            while j < n and target[j] == '_':
                j += 1

            # if both reached the end, success
            if i == n and j == n:
                return True
            # if only one reached the end, mismatch counts/types
            if i == n or j == n:
                return False

            # now both are on a piece
            if start[i] != target[j]:
                return False

            if start[i] == 'L':
                # L can only move left: start index must be >= target index
                if i < j:
                    return False
            else:  # 'R'
                # R can only move right: start index must be <= target index
                if i > j:
                    return False

            i += 1
            j += 1

        return True
```
- Notes: We run two pointers i and j scanning for the next non-'_' char in start and target. If the types differ, return False. For 'L', ensure start index i >= target index j; for 'R', ensure i <= j. If any of these constraints is violated, return False. If both pointers reach the end together, return True. Time complexity O(n), space complexity O(1).