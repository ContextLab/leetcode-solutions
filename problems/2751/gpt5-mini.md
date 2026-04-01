# [Problem 2751: Robot Collisions](https://leetcode.com/problems/robot-collisions/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
[Robots move simultaneously; collisions occur when a right-moving robot to the left meets a left-moving robot to the right. Positions are arbitrary (unsorted), so sort by position to simulate encounters left-to-right. A classic pattern: maintain a stack of right-moving robots (their index and current health). When we encounter a left-moving robot, it will potentially collide with robots on the stack (the right-movers encountered earlier). Simulate pairwise collisions between the current left-moving robot and the top of the stack until either the left robot dies or there are no more right-movers to collide with. Track survivors with their updated healths. Need to return survivors in the original input order.]

## Refining the problem, round 2 thoughts
[Sort robots by position ascending (so collisions happen between an earlier 'R' and a later 'L'). Use a stack to store active 'R' robots with mutable health. For each 'L' robot, while stack non-empty and current L is alive, compare healths:
- If top_R.health < L.health: top_R dies (pop), L.health -= 1, continue (L may hit earlier R).
- If top_R.health == L.health: both die (pop, L dies).
- If top_R.health > L.health: L dies, top_R.health -= 1 (update top on stack).
If an L survives all encounters, it's a survivor (record its health). After processing all robots, remaining R robots on the stack are survivors with their updated healths. Finally, output survivors in original order. Complexity: sorting O(n log n) + simulation O(n) amortized, space O(n). Edge cases: all R or all L (no collisions), robots with large health (decrement count bounded by n since each collision removes at least one robot).]

## Attempted solution(s)
```python
from typing import List

class Solution:
    def survivedRobotsHealths(self, positions: List[int], healths: List[int], directions: str) -> List[int]:
        n = len(positions)
        # Create list of robots sorted by position: (pos, original_index, health, direction)
        robots = sorted(
            [(positions[i], i, healths[i], directions[i]) for i in range(n)],
            key=lambda x: x[0]
        )

        # Stack for right-moving robots: elements are [original_index, current_health]
        stack = []
        survivors = {}  # map original_index -> health for surviving robots

        for _, idx, h, d in robots:
            if d == 'R':
                # Right-moving robot might collide with a future L, so push to stack
                stack.append([idx, h])
            else:
                # Left-moving robot will collide with right-moving robots on the stack
                cur_h = h
                while stack and cur_h > 0:
                    top_idx, top_h = stack[-1]
                    if top_h < cur_h:
                        # top R dies; L loses 1 health and continues
                        stack.pop()
                        cur_h -= 1
                    elif top_h == cur_h:
                        # both die
                        stack.pop()
                        cur_h = 0
                        break
                    else:
                        # top R survives but loses 1 health; L dies
                        stack[-1][1] -= 1
                        cur_h = 0
                        break
                if cur_h > 0:
                    # L survived all collisions
                    survivors[idx] = cur_h

        # Remaining right-moving robots on stack survive
        for idx, h in stack:
            survivors[idx] = h

        # Collect survivors' healths in the original input order
        result = []
        for i in range(n):
            if i in survivors:
                result.append(survivors[i])
        return result
```
- Notes:
  - We sort by position to process collisions in spatial order. The stack stores currently active right-moving robots; left-moving robots resolve collisions against the stack top(s).
  - Each robot is pushed/popped at most once, so the collision simulation is O(n) amortized. Total time complexity is O(n log n) due to initial sorting. Space complexity is O(n) for the stack and survivors map.
  - The survivors dictionary maps original indices to their final health so we can output in the order requested by the problem.