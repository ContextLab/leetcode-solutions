# [Problem 2126: Destroying Asteroids](https://leetcode.com/problems/destroying-asteroids/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can pick any order to collide with asteroids. If the planet's current mass is >= an asteroid's mass, the planet absorbs it and gains mass. Intuitively, to maximize chances of absorbing everything, we should always take the smallest asteroid that we can — absorbing smaller asteroids earlier increases our mass and makes it easier to absorb larger ones later. This suggests a greedy approach: sort asteroids ascending and try to absorb in that order. If at any point mass < asteroid[i], we fail and return False. If we finish the list, return True.

I should consider whether there exists a counterexample where absorbing a larger asteroid first (when possible) helps later — but absorbing a larger one only increases mass by a larger amount, and if you can absorb the larger one, you could also absorb the smaller one first; taking the smaller one first never reduces future capability. So sorting ascending is safe.

## Refining the problem, round 2 thoughts
- Edge cases:
  - If any asteroid > sum(mass + all other asteroids reachable) we might fail; sorting will detect this when reaching it.
  - Large input sizes: up to 1e5 asteroids, so O(n log n) sorting is fine.
  - Values up to 1e5 each; total sum up to 1e10 but Python integers handle this easily (no overflow).
- Alternative: using a min-heap and repeatedly popping the smallest gives the same complexity (heapify is O(n), then O(n log n) overall if pushing), but sorting is simpler and slightly faster in practice.
- Complexity:
  - Time: O(n log n) due to sorting.
  - Space: O(1) extra (or O(n) if counting sort or if sort is not in-place) beyond input.

Proof sketch for greedy correctness: suppose there exists a valid order that destroys all asteroids. Consider first asteroid in that order that is not the smallest available at that time — swapping with any smaller one earlier cannot make it impossible (because smaller asteroid is <= the currently chosen one and so was also destroyable), and increases or preserves mass progression; repeating swaps yields the sorted order. Thus sorted ascending order works when any order works.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def asteroidsDestroyed(self, mass: int, asteroids: List[int]) -> bool:
        asteroids.sort()
        cur = mass
        for a in asteroids:
            if cur < a:
                return False
            cur += a
        return True
```
- Notes:
  - Approach: sort asteroids ascending and greedily absorb each if possible.
  - Time complexity: O(n log n) due to sorting (n = len(asteroids)).
  - Space complexity: O(1) extra (in-place sort), or O(n) if counting the sort's auxiliary space. Python's sort is Timsort and uses O(n) worst-case auxiliary but typical is in-place.
  - Implementation detail: use Python's arbitrary-precision integers so the running sum won't overflow.