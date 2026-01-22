# [Problem 860: Lemonade Change](https://leetcode.com/problems/lemonade-change/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem is classic greedy: each lemonade costs $5, customers pay with 5, 10, or 20. We start with no change and must give exact change for each customer in order. We only need to track how many $5 and $10 bills we have (a $20 never used as change). For a $5 payment, we just take it. For a $10 payment, we must give one $5 (so need at least one $5). For a $20 payment, we need to give $15: either one $10 + one $5, or three $5s. Intuitively it's better to give one $10 + one $5 when possible because that preserves more $5 bills (which are most flexible for making change later). So greedily prefer (10+5) for $20, otherwise use three $5s. That should work.

## Refining the problem, round 2 thoughts
- Edge cases: early customers paying with $10 or $20 when we have no $5s should return false.
- Why prefer 10+5 over 3x5? Because $5 bills are required to give change to $10 customers; preserving more $5s increases future feasibility. Using three $5s when there's a $10 available wastes smaller bills.
- Complexity: we process each bill once, O(n) time and O(1) extra space.
- Alternative: simulate with counters for fives and tens only. No need to track $20s.
- Constraints up to 1e5, so the greedy O(n) approach is fast enough.

## Attempted solution(s)
```python
class Solution:
    def lemonadeChange(self, bills: list[int]) -> bool:
        five_count = 0
        ten_count = 0

        for b in bills:
            if b == 5:
                five_count += 1
            elif b == 10:
                if five_count == 0:
                    return False
                five_count -= 1
                ten_count += 1
            else:  # b == 20
                # Prefer to give one 10 and one 5 if possible
                if ten_count > 0 and five_count > 0:
                    ten_count -= 1
                    five_count -= 1
                elif five_count >= 3:
                    five_count -= 3
                else:
                    return False

        return True
```
- Notes:
  - Approach: greedy simulation keeping counts of $5 and $10 bills. For $20 payments, prefer using one $10 and one $5, otherwise use three $5s.
  - Time complexity: O(n), where n = len(bills), because we process each customer once.
  - Space complexity: O(1), only two integer counters are used.
  - Implementation detail: early return False as soon as we cannot make change for a customer. The logic is straightforward and handles all given constraints.