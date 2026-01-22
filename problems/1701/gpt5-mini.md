# [Problem 1701: Average Waiting Time](https://leetcode.com/problems/average-waiting-time/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have a single chef, customers arrive sorted by time, and chef serves in the given order. This is a straightforward simulation: maintain the current time when the chef becomes free. For each customer, if the chef is free at or before the arrival, the chef starts immediately; otherwise the customer waits until the chef finishes the current job. Waiting time for a customer = finish_time - arrival_time. Sum these and divide by the number of customers. No need for a heap or queue because arrival order is fixed and sorted.

## Refining the problem, round 2 thoughts
Edge cases:
- When chef is idle and next customer arrives later (current_time < arrival): chef starts at arrival, waiting time equals service time.
- When chef is busy (current_time > arrival): customer waits until current_time, finish = current_time + service_time.
- The sums can grow up to ~1e9 which fits in Python int; final average should be returned as float. Precision within 1e-5 is acceptable.

Time complexity: O(n) where n = number of customers (single pass).
Space complexity: O(1) extra space.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def averageWaitingTime(self, customers: List[List[int]]) -> float:
        total_wait = 0
        current_time = 0
        
        for arrival, time in customers:
            if current_time <= arrival:
                # chef idle, start at arrival
                current_time = arrival + time
                total_wait += time  # finish - arrival = (arrival+time) - arrival = time
            else:
                # chef busy, customer waits until current_time
                current_time += time  # finish = current_time + time (where current_time was the start)
                total_wait += current_time - arrival
        
        return total_wait / len(customers)
```
- Notes: We iterate once over customers, updating current_time to the finish time after each customer and accumulating waiting times. The conditional handles whether the chef is idle at arrival or not.
- Time complexity: O(n). Space complexity: O(1).
- Implementation detail: Using Python ints for sums and returning a float (division) yields the required precision (solutions within 1e-5 accepted).