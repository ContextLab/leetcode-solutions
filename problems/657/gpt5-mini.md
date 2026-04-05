# [Problem 657: Robot Return to Origin](https://leetcode.com/problems/robot-return-to-origin/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share raw stream-of-consciousness, but here is a concise summary of the approach: track the robot's net displacement. The robot returns to origin iff the number of 'U' moves equals 'D' moves and the number of 'L' moves equals 'R' moves. This can be checked by counting characters or by simulating x/y coordinates.

## Refining the problem, round 2 thoughts
- Edge cases: constraints guarantee at least one move and only valid characters, so no extra validation needed.
- Two straightforward implementations:
  - Use counts: O(n) time and O(1) extra space.
  - Simulate coordinates (x,y) and update per move: O(n) time and O(1) space.
- Both are simple, efficient, and clear. Using str.count calls is concise but may scan the string multiple times (still O(n) total since four counts). A single-pass simulation also yields O(n) with one pass.

## Attempted solution(s)
```python
class Solution:
    def judgeCircle(self, moves: str) -> bool:
        # Simple and clear: count matching opposite moves
        return moves.count('U') == moves.count('D') and moves.count('L') == moves.count('R')
```
- Notes:
  - Approach: Compare counts of opposite directions; if both vertical and horizontal pairs match, robot returns to origin.
  - Time complexity: O(n), where n = len(moves). (Counting each of the four characters scans the string; overall still linear.)
  - Space complexity: O(1) extra space.
  - Alternative: single-pass coordinate simulation:
    - x,y = 0,0; update for each char; return x==0 and y==0. Also O(n) time, O(1) space.