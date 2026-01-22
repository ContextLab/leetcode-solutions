# [Problem 3516: Find Closest Person](https://leetcode.com/problems/find-closest-person/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have three positions x, y, z on a number line. Persons 1 and 2 move toward Person 3 at the same speed. That means whoever is closer (in absolute distance) to z arrives first. So compute distance from x to z and distance from y to z, compare. If equal, it's a tie. Edge cases: x==z or y==z (one already at z) — distance will be zero and handled naturally. No need to simulate movement step-by-step; absolute difference is sufficient.

## Refining the problem, round 2 thoughts
- Confirm constraints: x,y,z are small (1..100) but that doesn't change the approach.
- Tie handling: if abs(x-z) == abs(y-z) return 0.
- Alternate but unnecessary approaches: simulate simultaneous steps until someone reaches z (would be slower and more complex).
- Complexity: computing two absolute differences and comparing is O(1) time and O(1) space.
- Implementation detail: follow expected LeetCode function signature — I'll implement closestPerson(self, x:int, y:int, z:int) -> int.

## Attempted solution(s)
```python
class Solution:
    def closestPerson(self, x: int, y: int, z: int) -> int:
        dx = abs(x - z)
        dy = abs(y - z)
        if dx < dy:
            return 1
        if dy < dx:
            return 2
        return 0
```
- Notes:
  - Approach: compute absolute distances from Person 1 and Person 2 to Person 3 and compare.
  - Time complexity: O(1) — only a few arithmetic operations and comparisons.
  - Space complexity: O(1) — constant extra space for two variables.