# [Problem 2211: Count Collisions on a Road](https://leetcode.com/problems/count-collisions-on-a-road/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The cars move at the same speed; collisions only happen when paths cross. Cars that go left from the far left never meet anyone (they run away), and cars that go right from the far right never meet anyone. Any car that is moving and is not in those "escape" groups will eventually be involved in a collision (either head-on with another moving car or into a stationary car created by previous collisions). Each moving car that ends up stopped contributes one collision to the total count, and when two moving cars meet head-on both are counted — that gives 2 collisions for that event, but counting stopped moving cars captures that naturally. So maybe we can ignore the leading 'L's and trailing 'R's and count the rest of moving cars.

## Refining the problem, round 2 thoughts
Refinement:
- Remove (ignore) all leading 'L' characters because they move left off to infinity and never collide.
- Remove (ignore) all trailing 'R' characters because they move right off to infinity and never collide.
- For the remaining segment, every 'L' or 'R' will eventually be involved in a collision and thus contributes 1 to the collision count. 'S' contributes 0.
- Answer = count of characters in the middle segment that are not 'S'.
Edge cases:
- If all characters are leading L or trailing R (or both), the remaining segment may be empty -> return 0.
Time/space:
- Single pass to find boundaries and then a pass to count -> O(n) time, O(1) extra space.

## Attempted solution(s)
```python
class Solution:
    def countCollisions(self, directions: str) -> int:
        n = len(directions)
        i = 0
        # skip leading L (they go off to left)
        while i < n and directions[i] == 'L':
            i += 1
        j = n - 1
        # skip trailing R (they go off to right)
        while j >= 0 and directions[j] == 'R':
            j -= 1
        if i > j:
            return 0
        # count non-'S' in the remaining segment
        cnt = 0
        for k in range(i, j + 1):
            if directions[k] != 'S':
                cnt += 1
        return cnt
```
- Notes:
  - Approach: skip cars that will never collide (leading 'L's and trailing 'R's), then every remaining moving car ('L' or 'R') will eventually stop due to collisions, so count them.
  - Time complexity: O(n) where n = len(directions) (two pointer scans and one pass in worst case).
  - Space complexity: O(1) extra space.
  - Implementation detail: handle the case i > j (empty middle segment) to return 0.