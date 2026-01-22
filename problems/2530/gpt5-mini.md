# [Problem 2530: Maximal Score After Applying K Operations](https://leetcode.com/problems/maximal-score-after-applying-k-operations/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the maximum total after exactly k operations where each operation picks an index i, adds nums[i] to score, and replaces nums[i] with ceil(nums[i]/3). Intuitively this is a greedy problem: each operation we should take the current largest element to maximize the immediate gain. Replacing a large element with ceil(x/3) drastically reduces its future contribution, so picking the largest available at each step seems optimal. A max-heap (priority queue) suits repeated extraction of the current maximum and re-insertion of its reduced value.

Potential pitfalls: repeated small values (1) stay 1 after ceil(1/3) = 1, so if heap top becomes 1 we can short-circuit and add the remaining operations as ones. Need to implement ceil efficiently: (x + 2) // 3.

## Refining the problem, round 2 thoughts
- Prove/justify greedy: picking the largest now never hurts compared to picking a smaller element now and the larger later — immediate gain is higher and the reduction effect is independent per element, so classic greedy / exchange argument holds.
- Data structure: Python heapq is a min-heap; store negatives to simulate a max-heap.
- Complexity: each operation is a pop + push (log n) -> O(k log n). Building heap is O(n).
- Edge cases:
  - If an element becomes 1, it stays 1 — if the max is 1, all subsequent picks will be 1, so we can add the remaining operations in O(1).
  - n and k up to 1e5, nums up to 1e9 — fits well.
- Alternative: balanced BST or sorted container, but heap is simplest and efficient.

## Attempted solution(s)
```python
import heapq
from typing import List

class Solution:
    def maxKelements(self, nums: List[int], k: int) -> int:
        # Use a max-heap via negatives
        heap = [-x for x in nums]
        heapq.heapify(heap)
        score = 0

        for i in range(k):
            # pop largest
            val = -heapq.heappop(heap)
            score += val
            # If val is 1, all future pops will be 1 as well (ceil(1/3)=1)
            if val == 1:
                # Add remaining (k - i - 1) ones and break
                score += (k - i - 1) * 1
                break
            # replace with ceil(val / 3)
            new_val = (val + 2) // 3
            heapq.heappush(heap, -new_val)

        return score
```
- Notes:
  - Approach: greedy choose largest each operation using a max-heap implemented with negatives in Python's heapq.
  - Ceil computation uses integer math: ceil(x/3) = (x + 2) // 3.
  - Optimization: if the popped value is 1, all remaining operations will add 1 each (since ceil(1/3) = 1), so add the remainder directly and terminate early.
  - Time complexity: O(n + k log n) (heapify O(n), each of k iterations does pop/push O(log n)), with an early exit possible when values drop to 1.
  - Space complexity: O(n) for the heap.