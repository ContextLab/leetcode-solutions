# [Problem 1823: Find the Winner of the Circular Game](https://leetcode.com/problems/find-the-winner-of-the-circular-game/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The description is a classic elimination-in-a-circle problem. My first instinct is to simulate the process (e.g., with a list or deque) removing every k-th counted friend until one remains. Simulation is straightforward but can be inefficient if done naively (removing from the middle of a list repeatedly is O(n) per removal).

I recall this is the Josephus problem. There is a well-known recurrence for Josephus: if f(n) is the 0-based index of the survivor when counting by k, then f(1)=0 and
    f(n) = (f(n-1) + k) % n.
So we can compute the answer iteratively in O(n) time and O(1) extra space, and return f(n)+1 to convert to 1-based indexing.

## Refining the problem, round 2 thoughts
Edge cases: n = 1 should return 1. k can equal n, but the recurrence handles that naturally because of the modulo. Simulation would work for small n (n ≤ 500 per constraints), but the recurrence is simpler and meets the follow-up (linear time and constant space).

Time/space:
- Using the iterative Josephus recurrence: O(n) time, O(1) extra space.
- Simulation with a deque/list: O(n) removals; if rotation/removal is done carefully (deque.rotate), still O(n*k) in worst naive approaches or O(n^2) depending on operations. Since n ≤ 500, simulation would pass, but recurrence is cleaner and optimal.

I'll implement the iterative recurrence.

## Attempted solution(s)
```python
class Solution:
    def findTheWinner(self, n: int, k: int) -> int:
        # f is the 0-based index of the winner for current number of people
        f = 0  # f(1) = 0
        for i in range(2, n + 1):
            f = (f + k) % i
        return f + 1  # convert to 1-based indexing
```
- Notes:
  - This uses the Josephus recurrence: f(1)=0, f(i)=(f(i-1)+k) % i.
  - Time complexity: O(n) (loop from 2..n).
  - Space complexity: O(1) extra space.
  - Works for all 1 <= k <= n <= 500.