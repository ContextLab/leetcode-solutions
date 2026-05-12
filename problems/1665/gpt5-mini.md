# [Problem 1665: Minimum Initial Energy to Finish Tasks](https://leetcode.com/problems/minimum-initial-energy-to-finish-tasks/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We must choose an order to do tasks to minimize the initial energy S. For a given order, what's the minimal S? Consider working backwards: for the last task in the order, we need at least its minimum. For the previous task, if we need "need" energy to finish all tasks after it, then before doing that previous task we must have at least max(minimum_prev, actual_prev + need) (because after spending actual_prev we must still have at least need for the remaining tasks). That gives a recurrence to compute minimal S for a fixed order by processing tasks from last to first.

So the problem reduces to finding an order that minimizes the final "need" computed by the backward recurrence. Intuitively, tasks that have a large gap between minimum and actual (i.e., require a lot of upfront padding relative to what they actually consume) should be done earlier so their high minimum can be satisfied while we still have more energy. That suggests sorting by (minimum - actual) descending.

I recall the known greedy: sort tasks by (minimum - actual) descending, then compute need by iterating from last to first and updating need = max(minimum_i, actual_i + need). That yields the minimum initial energy.

## Refining the problem, round 2 thoughts
- Edge cases: single task -> answer is its minimum. Many tasks with identical differences: tie ordering won't change the computed minimal need by the recurrence.
- Complexity: sorting is O(n log n), single pass O(n). Memory O(1) extra aside from sort.
- Correctness sketch: For two tasks a and b, swapping their execution order can be analyzed via the backward recurrence; it's optimal to place the one with larger (min - actual) earlier. This is the standard exchange argument used in greedy proofs for this problem.
- Constraints are up to 1e5 tasks, values up to 1e4, so O(n log n) sorting is fine.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minimumEffort(self, tasks: List[List[int]]) -> int:
        # Sort by (minimum - actual) descending
        tasks.sort(key=lambda t: t[1] - t[0], reverse=True)
        need = 0
        # Process from last executed to first executed
        for actual, minimum in reversed(tasks):
            need = max(minimum, actual + need)
        return need
```
- Notes:
  - Approach: Greedy ordering by (minimum - actual) descending, then compute minimal starting energy via backward recurrence need = max(minimum_i, actual_i + need) processing tasks from last to first in the chosen order.
  - Time complexity: O(n log n) due to sorting, where n = len(tasks).
  - Space complexity: O(1) extra (ignoring input sort in-place) or O(n) if sort copies are counted / if stable copy used.
  - This is the standard greedy solution; exchange-argument proof shows tasks with larger (minimum - actual) should be scheduled earlier to minimize the required initial energy.