# [Problem 1518: Water Bottles](https://leetcode.com/problems/water-bottles/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can drink the initial full bottles and each drunk bottle becomes an empty. With enough empties I can exchange them for additional full bottles. This feels like a straightforward simulation: keep track of how many full bottles I currently have and how many empties I have; drink the full ones, convert them to empties, then exchange empties for new full bottles, repeat until I can't exchange anymore. There's also a known math/tricky closed form for some cases, but simulation is simple, clear, and efficient given the small input bounds.

## Refining the problem, round 2 thoughts
Refine to a loop that in each iteration drinks all current full bottles at once: add them to the total drunk, add them to empties, then compute how many new full bottles we get by exchanging empties (empties // numExchange) and update empties to the remainder (empties % numExchange). Continue while we have any full bottles to drink. Edge cases: numExchange >= 2 by constraints, so no infinite loop. Complexity: each loop reduces empties or produces progressively fewer new bottles, so the number of iterations is small — effectively proportional to the number of times we can perform an exchange, bounded by the final answer. Space O(1).

## Attempted solution(s)
```python
class Solution:
    def numWaterBottles(self, numBottles: int, numExchange: int) -> int:
        total_drunk = 0
        empties = 0
        full = numBottles

        while full > 0:
            # Drink all current full bottles
            total_drunk += full
            empties += full
            # Exchange empties for new full bottles
            full = empties // numExchange
            empties = empties % numExchange

        return total_drunk
```
- Notes:
  - Approach: Greedy simulation loop: drink all available full bottles, convert to empties, exchange empties for new full bottles, repeat until none left.
  - Time complexity: O(k) where k is the number of iterations (each iteration consumes all current full bottles and reduces the system). In practice k is at most proportional to the total number of bottles drunk (which is small given constraints), so this runs very fast for numBottles <= 100.
  - Space complexity: O(1) using a few integer counters.
  - Implementation detail: Constraints guarantee numExchange >= 2, so no infinite exchanges.