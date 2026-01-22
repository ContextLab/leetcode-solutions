# [Problem 3477: Fruits Into Baskets II](https://leetcode.com/problems/fruits-into-baskets-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to simulate placing fruit types left-to-right into the leftmost available basket whose capacity >= that fruit's quantity. "Leftmost available" implies we cannot reorder baskets or fruits; for each fruit we must scan baskets from the left and pick the first unused basket that fits. The simplest approach is to keep an array of bools marking used baskets and for each fruit scan baskets from index 0 to n-1 until a fit is found. n is at most 100, so an O(n^2) scan is fine. No need for complicated data structures.

Potential pitfalls: ensure once a basket is used it is not reused; ensure we look for leftmost available (so we cannot skip earlier baskets even if they were too small for earlier fruits — only "available" and capacity >= needed matters). Also consider all fruits placed, none placed, duplicates, equal sizes.

## Refining the problem, round 2 thoughts
- The greedy simulation is straightforward and correct: processing fruits in order and assigning the first unused basket with sufficient capacity follows the problem statement exactly.
- Edge cases:
  - If baskets have capacity less than the fruit quantity, skip them.
  - Multiple fruits may be identical; each requires its own basket.
  - If no basket fits, increment the unplaced count.
- Time complexity: scanning for each fruit over all baskets yields O(n^2) time, with n ≤ 100 this is trivial.
- Space complexity: O(n) extra for the used array.
- No better asymptotic complexity is needed given constraints; an index tree or specialized structure is unnecessary.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countUnplaced(self, fruits: List[int], baskets: List[int]) -> int:
        """
        Simulate placing fruits from left to right. For each fruit, find the
        leftmost basket that is unused and has capacity >= fruit quantity.
        If none found, it's unplaced.
        """
        n = len(fruits)
        used = [False] * n
        unplaced = 0

        for f in fruits:
            placed = False
            for j in range(n):
                if not used[j] and baskets[j] >= f:
                    used[j] = True
                    placed = True
                    break
            if not placed:
                unplaced += 1

        return unplaced

# Example usage / quick tests
if __name__ == "__main__":
    sol = Solution()
    print(sol.countUnplaced([4,2,5], [3,5,4]))  # Expected 1
    print(sol.countUnplaced([3,6,1], [6,4,7]))  # Expected 0
```
- Approach: Greedy simulation following the exact left-to-right placement rule. Maintain a boolean used array to mark baskets already occupied. For each fruit, scan baskets from leftmost to rightmost and assign the first unused basket whose capacity is sufficient.
- Time complexity: O(n^2) in the worst case (n fruits × up to n baskets scanned per fruit). With n ≤ 100 this is perfectly acceptable.
- Space complexity: O(n) extra for the used array.
- Implementation details: The code is straightforward and robust to edge cases (all placed, none placed, duplicates).