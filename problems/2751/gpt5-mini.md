# [Problem 2751: Robot Collisions](https://leetcode.com/problems/robot-collisions/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Robots move at the same speed; collisions only happen when a right-moving robot (R) is to the left of a left-moving robot (L). Sorting robots by position turns the problem into a left-to-right sweep where R robots can "wait" on a stack and L robots collide with the stacked R robots from the top. This resembles the classic asteroid-collision / parentheses-matching pattern. For each L we simulate collisions with the most recent R; health comparisons determine who dies or has its health decremented and whether collisions continue. We must return surviving robots' healths in the original input order.

## Refining the problem, round 2 thoughts
- Sort robots by position while keeping original indices, healths, and directions.
- Use a stack to store right-moving robots (their original index and current health).
- When we encounter a left-moving robot, simulate collisions against the stack top until the L dies or the stack is empty:
  - If R.health < L.health: R dies (pop), L.health -= 1, continue.
  - If R.health == L.health: both die (pop R, L becomes dead), stop.
  - If R.health > L.health: R.health -= 1 (update top), L dies, stop.
- After processing all robots, any R robots left on the stack survive with their current health. Any L that survived (stack empty when processed) also survive with its remaining health.
- Output survivors' healths in the input order (skip dead robots).
- Time: O(n) amortized since each robot is pushed/popped at most once. Space: O(n).

Edge cases: unsorted positions (handled by sorting), ties in health (both removed), many consecutive collisions causing health decrements.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def survivedRobotsHealths(self, positions: List[int], healths: List[int], directions: str) -> List[int]:
        n = len(positions)
        # Build list of robots sorted by position
        robots = sorted(((positions[i], i, healths[i], directions[i]) for i in range(n)), key=lambda x: x[0])
        # stack holds tuples (original_index, current_health) for right-moving robots
        stack = []
        # result placeholder: -1 means dead; otherwise final health
        res = [-1] * n

        for _, idx, h, d in robots:
            if d == 'R':
                stack.append((idx, h))
            else:  # d == 'L'
                cur_h = h
                # collide with right-moving robots on the stack
                while cur_h > 0 and stack:
                    r_idx, r_h = stack[-1]
                    if r_h < cur_h:
                        # right robot dies, left robot loses 1 health and continues
                        stack.pop()
                        cur_h -= 1
                    elif r_h == cur_h:
                        # both die
                        stack.pop()
                        cur_h = 0
                    else:  # r_h > cur_h
                        # left robot dies, right robot loses 1 health and stays
                        stack[-1] = (r_idx, r_h - 1)
                        cur_h = 0
                # if left robot survived (no more R to collide), record its remaining health
                if cur_h > 0:
                    res[idx] = cur_h

        # Any remaining right-moving robots in stack survive with their current health
        for r_idx, r_h in stack:
            res[r_idx] = r_h

        # Return survivors' healths in original order (skip dead robots)
        return [res[i] for i in range(n) if res[i] != -1]
```
- Notes:
  - Approach: sort by position and simulate pairwise collisions using a stack for R robots; L robots collide with the nearest R on the left (stack top).
  - Complexity: O(n) time (each robot is pushed/popped at most once) and O(n) extra space for sorting + stack + result array.
  - Implementation details: we track current healths in the stack to account for reductions after collisions; original indices are preserved to produce output in input order.