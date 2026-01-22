# [Problem 3100: Water Bottles II](https://leetcode.com/problems/water-bottles-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We start with some full bottles. We can drink any number of full bottles to create empties, and we can exchange empty bottles for one full bottle when we have at least numExchange empties — but after each exchange, numExchange increases by 1 and you cannot do more than one exchange with the same value of numExchange. That suggests a straightforward simulation: drink all current full bottles to maximize empties, then repeatedly perform at most one exchange for the current numExchange while empties are sufficient, incrementing numExchange each time we exchange. Repeat drinking the newly acquired full bottles, and continue until no more exchanges are possible and no full bottles remain.

This feels optimal because drinking earlier than "all" only defers empties and doesn't help achieve more exchanges — having all empties available can only increase or maintain the number of exchanges you can perform.

## Refining the problem, round 2 thoughts
- Important to enforce the rule that each value of numExchange can be used at most once: after every exchange increment numExchange by 1 so we never reuse the same exchange threshold.
- Edge cases:
  - numExchange == 1: you can exchange as soon as you have one empty, but after each exchange the requirement increases; simulation still handles it.
  - numExchange > initial empties: you may need to drink more before any exchange is possible.
- Complexity: The simulation runs a small number of steps: each exchange increases numExchange and consumes empties, and total bottles drunk is finite. With constraints (numBottles, numExchange <= 100) this is effectively constant-time, but even generally it's bounded by the total number of bottles you ever drink plus the number of exchanges performed.
- Alternative solutions: one could try to reason mathematically about how many exchanges will be possible in total, but the incremental simulation is simple, easy to reason about, and efficient for given constraints.

## Attempted solution(s)
```python
class Solution:
    def numWaterBottles(self, numBottles: int, numExchange: int) -> int:
        full = numBottles
        empty = 0
        k = numExchange
        drunk = 0

        # Keep drinking all full bottles, then try to exchange (at most once per k,
        # but multiple times overall as k increases).
        while full > 0:
            # Drink all current full bottles
            drunk += full
            empty += full
            full = 0

            # Exchange while we can for the current k (one exchange consumes k empties,
            # then k increments, so this naturally prevents multiple exchanges at the same k)
            while empty >= k:
                empty -= k
                full += 1
                k += 1

        return drunk
```
- Notes about the solution:
  - Approach: simulate drinking all full bottles to collect empties, then repeatedly perform a single exchange for the current required number of empties (k), incrementing k after each exchange. Repeat until no full bottles remain and no further exchanges are possible.
  - Correctness: drinking all full bottles before attempting exchanges is optimal because it maximizes empties available for exchanges; the rule "one exchange per k" is respected by incrementing k after each exchange.
  - Time complexity: O(total number of bottles drunk + number of exchanges). Given problem constraints (numBottles, numExchange ≤ 100), this is effectively O(1). More generally, the process is bounded and will terminate because k strictly increases on each exchange and empties decrease by at least k each exchange.
  - Space complexity: O(1) extra space (a few integer counters).