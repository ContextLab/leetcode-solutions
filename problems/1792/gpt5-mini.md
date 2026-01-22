# [Problem 1792: Maximum Average Pass Ratio](https://leetcode.com/problems/maximum-average-pass-ratio/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We want to maximize average pass ratio across all classes after assigning extra students that always pass. Intuitively, each extra student should be assigned where they produce the largest increase in the total sum of pass ratios. That suggests a greedy approach: at every step, place an extra student in the class that yields the maximal marginal gain in that class's pass ratio. The marginal gain for adding one student to class (p, t) is (p+1)/(t+1) - p/t. We can pick the class with the largest gain using a max-heap (priority queue). After assigning all extraStudents, compute average = sum(p/t) / n.

## Refining the problem, round 2 thoughts
- Implement a max-heap by pushing negative gains into Python's heapq (a min-heap).
- Each time we assign one extra student to a class, p and t both increase by 1; we must recompute that class's new marginal gain and push it back.
- Edge cases: if p == t (class already all passing), the marginal gain is 0; algorithm will simply avoid wasting students there unless no better option exists.
- Complexity: pushing and popping from the heap extraStudents times gives O((n + extraStudents) log n) time; space O(n).
- Floating point precision: computing gains as floats is fine; required precision is 1e-5.

## Attempted solution(s)
```python
import heapq
from typing import List

class Solution:
    def maxAverageRatio(self, classes: List[List[int]], extraStudents: int) -> float:
        # helper to compute marginal gain of adding one student to (p, t)
        def gain(p: int, t: int) -> float:
            return (p + 1) / (t + 1) - p / t

        heap = []
        n = len(classes)
        # build max-heap via negative gains
        for p, t in classes:
            heapq.heappush(heap, (-gain(p, t), p, t))

        # assign each extra student greedily
        for _ in range(extraStudents):
            neg_g, p, t = heapq.heappop(heap)
            p += 1
            t += 1
            heapq.heappush(heap, (-gain(p, t), p, t))

        # compute final average pass ratio
        total_ratio = 0.0
        while heap:
            _, p, t = heapq.heappop(heap)
            total_ratio += p / t

        return total_ratio / n
```
- Notes about the solution:
  - Approach: greedy selection based on marginal gain using a max-heap (implemented with negative values in Python's heapq).
  - Time complexity: O((n + extraStudents) * log n). We push n items initially, then for each extra student we pop and push one item (log n each).
  - Space complexity: O(n) for the heap.
  - Implementation details: recompute gain after each assignment; use floats for gain and final ratio. This meets the required precision (1e-5).