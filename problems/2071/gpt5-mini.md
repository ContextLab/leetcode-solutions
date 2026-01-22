# [Problem 2071: Maximum Number of Tasks You Can Assign](https://leetcode.com/problems/maximum-number-of-tasks-you-can-assign/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to maximize how many tasks can be completed given worker strengths, a limited number of pills that add a fixed strength, and each worker can take at most one task and at most one pill. This screams "binary search on answer" because the question asks for the maximum count and we can check feasibility for a given k. For a feasibility check we should use a greedy approach: if we try to complete k tasks, it makes sense to pick the k easiest tasks and try to match them to available workers. For assigning those k tasks greedily, we should try to assign the hardest among them first to the strongest available worker (to avoid wasting strong workers on easier tasks). If the strongest remaining worker can't do a task, we might try to use a pill on the weakest remaining worker if that lets them reach the task. Two-pointer approach on sorted arrays seems appropriate (workers sorted ascending, tasks sorted ascending), scanning tasks from largest to smallest and deciding to use either the strongest worker without pill or the weakest worker with a pill.

## Refining the problem, round 2 thoughts
- Sort tasks and workers ascending.
- For a candidate k (0 <= k <= min(n, m)), consider the k smallest tasks (most feasible set). Process those k tasks from largest to smallest.
  - Maintain two pointers on workers: l (weakest available), r (strongest available).
  - For current task t:
    - If workers[r] >= t: assign that worker (r--).
    - Else if we have pills remaining and workers[l] + strength >= t: use a pill on weakest worker (l++, pills--).
    - Else: cannot assign this task set -> k is infeasible.
- Binary search k to find maximum feasible value.
- Complexity: Sorting O(n log n + m log m). Each feasibility check costs O(k) with simple pointer moves; binary search does O(log(min(n,m))) checks, so total approx O((n+m) log(n+m) + min(n,m) * log(min(n,m))). Memory O(1) extra aside from sorts.

Edge cases:
- If m < k, impossible.
- strength = 0 reduces to simple matching without pills (but algorithm handles it).
- tasks or workers could be zero-valued (handled).
- Large values up to 1e9, but only comparisons and additions.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxTaskAssign(self, tasks: List[int], workers: List[int], pills: int, strength: int) -> int:
        tasks.sort()
        workers.sort()
        n = len(tasks)
        m = len(workers)

        # Check if we can assign k tasks (the k smallest tasks)
        def can_assign(k: int) -> bool:
            if k == 0:
                return True
            if k > m:
                return False
            l = 0
            r = m - 1
            pills_left = pills
            # iterate tasks[0..k-1] from largest to smallest
            for i in range(k - 1, -1, -1):
                t = tasks[i]
                # If the strongest remaining worker can handle without pill
                if workers[r] >= t:
                    r -= 1
                else:
                    # Try to use a pill on the weakest remaining worker
                    if pills_left > 0 and workers[l] + strength >= t:
                        l += 1
                        pills_left -= 1
                    else:
                        return False
            return True

        # Binary search the maximum k in [0, min(n,m)]
        lo = 0
        hi = min(n, m)
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if can_assign(mid):
                lo = mid
            else:
                hi = mid - 1
        return lo
```
- Approach: Binary search on the number of tasks k. For each k, greedily try to assign the k smallest tasks by scanning them from largest to smallest and using two pointers on the sorted workers array: use the strongest worker if possible; otherwise use a pill on the weakest worker if that suffices. This preserves resources (strong workers and pills) optimally for remaining tasks.
- Time complexity: O((n + m) log(n + m)) for sorting plus O(min(n, m) * log(min(n,m))) for the binary-search feasibility checks (each check is O(k) and there are O(log min(n,m)) checks). Overall dominated by sorting and checks: roughly O((n + m) log(n + m) + min(n,m) * log(min(n,m))). With n,m up to 5e4 this is efficient.
- Space complexity: O(1) extra beyond input and sorting (in-place sorts).