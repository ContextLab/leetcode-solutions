# [Problem 2833: Furthest Point From Origin](https://leetcode.com/problems/furthest-point-from-origin/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have moves consisting of 'L', 'R', and '_' where '_' can be chosen as either left or right. The final position after n moves is (#R chosen) - (#L chosen). To maximize the distance from origin (absolute value), we should orient every flexible move '_' in the same direction we want to push (either all right or all left). So we only need counts of L, R, and '_' to decide the maximum possible distance.

## Refining the problem, round 2 thoughts
- Let countL, countR, countUnders be counts of 'L', 'R', and '_' respectively.
- If we push all flexible moves to the right, position = countR + countUnders - countL.
- If we push all flexible moves to the left, position = countL + countUnders - countR (which is negative if countR > countL).
- The maximum absolute distance is the max of those two values, which simplifies to:
  answer = countUnders + abs(countR - countL).
- Time complexity: O(n) to count characters; space: O(1).
- Edge cases: none special given constraints (n between 1 and 50).

## Attempted solution(s)
```python
class Solution:
    def furthestDistanceFromOrigin(self, moves: str) -> int:
        countL = moves.count('L')
        countR = moves.count('R')
        countUnders = moves.count('_')
        return countUnders + abs(countR - countL)
```
- Notes:
  - Approach: count occurrences and use the derived formula: answer = count('_') + abs(count('R') - count('L')).
  - Time complexity: O(n), where n = len(moves) (counting characters).
  - Space complexity: O(1) (only a few integer counters).
  - This is straightforward and handles all allowed inputs per the problem constraints.