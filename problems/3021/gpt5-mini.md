# [Problem 3021: Alice and Bob Playing Flower Game](https://leetcode.com/problems/alice-and-bob-playing-flower-game/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The game: on each turn a player removes exactly one flower from one of the two lanes. If at the end of a turn both lanes are empty, the player who just moved wins. That is just "last-move-wins". The total number of moves possible is x + y. Alice starts, so if x + y is odd she makes the last move and wins; if x + y is even Bob makes the last move and Alice loses. So the winning condition for Alice is simply (x + y) being odd.

Thus we only need to count pairs (x, y) with x in [1..n], y in [1..m] such that x+y is odd. That happens exactly when one of x,y is even and the other is odd.

## Refining the problem, round 2 thoughts
Count pairs where x odd & y even plus pairs where x even & y odd. Let:
- odd_x = number of odd x in [1..n] = ceil(n/2) = n - n//2
- even_x = number of even x in [1..n] = n//2
(similarly for m).

Answer = odd_x * even_y + even_x * odd_y.

Edge cases: small n,m (like 1) are handled by integer division. Complexity is O(1) time and O(1) space. Values up to 1e5 pose no issue.

## Attempted solution(s)
```python
class Solution:
    def countPairs(self, n: int, m: int) -> int:
        # count odds and evens in each range [1..n], [1..m]
        odd_n = n - n // 2
        even_n = n // 2
        odd_m = m - m // 2
        even_m = m // 2
        # pairs where sum is odd: one odd + one even
        return odd_n * even_m + even_n * odd_m
```
- Notes:
  - Approach: Reduce game to parity of total moves (x+y). Alice wins iff x+y is odd. Count combinations with opposite parity.
  - Time complexity: O(1).
  - Space complexity: O(1).