# [Problem 1007: Minimum Domino Rotations For Equal Row](https://leetcode.com/problems/minimum-domino-rotations-for-equal-row/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the minimum rotations so that either the entire top row or entire bottom row is the same number. Each domino can be rotated (swap top and bottom). A naive thought: try every possible value 1..6 and see if we can make all tops or all bottoms equal to that value, counting rotations. But we can do even less work: any feasible final value must appear in the first domino (either tops[0] or bottoms[0]). If a value doesn't appear in the first domino, it's impossible to make every position that value for both rows because at index 0 you can't create that value by rotation. So candidates are just tops[0] and bottoms[0] (possibly the same). For each candidate v, iterate through all dominoes: if neither top nor bottom is v for some i, v is impossible; otherwise count how many rotations needed to make tops all v (rotations when tops[i] != v but bottoms[i] == v) and similarly for bottoms. Take minimum across candidates and targets (tops or bottoms). This is linear O(n) time and O(1) extra space.

## Refining the problem, round 2 thoughts
Edge cases:
- tops[0] == bottoms[0] gives only one candidate (avoid duplicate work).
- If both candidates fail, answer is -1.
- Input sizes up to 2e4 — O(n) is fine.
Alternative: brute-force over values 1..6 (still O(6n)) — acceptable, but checking only two candidates is slightly faster.
Be careful to count rotations correctly: there are two different rotation targets (make all tops equal to v OR make all bottoms equal to v). For each candidate v we should compute the rotations required to make tops all v and separately the rotations required to make bottoms all v; either is acceptable and we take the minimum.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minDominoRotations(self, tops: List[int], bottoms: List[int]) -> int:
        if not tops:
            return -1
        
        n = len(tops)
        candidates = {tops[0], bottoms[0]}
        
        def rotations_to_make(target: int) -> int:
            # Compute min rotations to make either tops all target or bottoms all target.
            rot_top = 0    # rotations to make tops all == target
            rot_bottom = 0 # rotations to make bottoms all == target
            for i in range(n):
                t, b = tops[i], bottoms[i]
                # If neither side has target, impossible
                if t != target and b != target:
                    return float('inf')
                # If top is not target but bottom is, we'd need to rotate to fix top
                if t != target and b == target:
                    rot_top += 1
                # If bottom is not target but top is, we'd need to rotate to fix bottom
                if b != target and t == target:
                    rot_bottom += 1
                # If both are target (t == target and b == target), no rotation needed for either
            return min(rot_top, rot_bottom)
        
        ans = float('inf')
        for cand in candidates:
            ans = min(ans, rotations_to_make(cand))
        
        return -1 if ans == float('inf') else ans
```
- Approach: Try only the values from the first domino as possible targets. For each target value, iterate through all dominoes: if neither side equals the target at some position, that target is impossible. Otherwise count rotations required to make all tops equal to target and rotations required to make all bottoms equal to target; take the smaller. Finally take the minimum across both candidates.
- Time complexity: O(n) where n = len(tops) because we check at most two candidates and each requires a single pass over the arrays.
- Space complexity: O(1) extra space (ignoring input storage).
- Important detail: Using float('inf') as sentinel for impossible target; if both candidates are impossible we return -1.