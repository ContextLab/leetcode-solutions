# [Problem 838: Push Dominoes](https://leetcode.com/problems/push-dominoes/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I recall a common approach where you treat contiguous stretches of '.' between forces ('L' or 'R') and decide how those dots resolve based on the forces at the ends. One trick is to add sentinel forces at both ends so you don't have to treat edges specially. Another approach is to simulate forces with left-to-right and right-to-left passes computing "force" magnitudes, but that's a bit more mechanical. The segment-based approach is O(n) and intuitive: if both ends are the same force, fill all with that; if left is 'R' and right is 'L', fill from both ends toward the middle; if ends are 'L' and 'R', leave as dots.

## Refining the problem, round 2 thoughts
Refine to the sentinel technique: build a new string s = 'L' + dominoes + 'R' so the edges behave like having an outside force and we can handle every segment uniformly. Iterate over s, tracking the index prev of the last non-dot. Whenever we hit another non-dot at index i, process the interval (prev, i). Cases:
- same char on both ends (both 'L' or both 'R'): fill entire interval with that char.
- left 'L' and right 'R': leave interval as '.' (they push away from each other).
- left 'R' and right 'L': fill from both sides inward; if interval length is odd, the middle remains '.'.

Time complexity: O(n) since each position is processed a constant number of times. Space complexity: O(n) to store the modified array (we need mutable structure and sentinels).

Edge cases:
- All dots => sentinel handling will make them all 'L' then 'R' which results in leaving them '.' correctly.
- Already filled (no dots) => code should return same layout (ignoring sentinels).
- Single character string.

## Attempted solution(s)
```python
class Solution:
    def pushDominoes(self, dominoes: str) -> str:
        # Add sentinels to avoid edge-case handling
        s = 'L' + dominoes + 'R'
        res = list(s)
        prev = 0  # index of last non-dot (starts at the sentinel 'L' at index 0)
        n = len(s)
        
        for i in range(1, n):
            if s[i] == '.':
                continue
            # Now s[i] is either 'L' or 'R' and s[prev] is too
            if s[prev] == s[i]:
                # Same force on both ends -> fill all in-between with that force
                for k in range(prev + 1, i):
                    res[k] = s[i]
            elif s[prev] == 'R' and s[i] == 'L':
                # Opposing forces -> fill from both ends inward
                left, right = prev + 1, i - 1
                while left < right:
                    res[left] = 'R'
                    res[right] = 'L'
                    left += 1
                    right -= 1
                # If left == right (odd number), it remains '.' which is already set
            # else: prev is 'L' and current is 'R' -> forces away from each other; keep dots
            prev = i
        
        # strip added sentinels
        return ''.join(res[1:-1])
```
- Notes:
  - Approach: sentinel-based segment processing. Add 'L' at front and 'R' at end so all segments between non-dot characters can be handled uniformly.
  - Time complexity: O(n) where n = len(dominoes). Each position is written at most once in the loops.
  - Space complexity: O(n) for the working list (and the sentinel-augmented string).
  - Implementation detail: use a list for mutable assignments. The final answer excludes the two sentinel characters.