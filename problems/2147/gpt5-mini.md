# [Problem 2147: Number of Ways to Divide a Long Corridor](https://leetcode.com/problems/number-of-ways-to-divide-a-long-corridor/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see a string of 'S' and 'P'. We need to place dividers (between characters) so that each resulting section contains exactly two 'S' (seats). Two fixed dividers exist at the ends. Essentially we want to partition the seats into groups of two consecutive seats (by seat order, not necessarily adjacent indices because plants can lie between). If the total number of 'S' is not even (or zero), it's impossible. If there are 2*k seats, we must make k sections each containing two seats: seats number (1,2), (3,4), ..., (2k-1,2k). The only freedom is where to place dividers between these groups — specifically between the second seat of one section and the first seat of the next — and we can place the divider in any gap between those two seats (the gap length equals number of characters between those two seats, including plants). So count seats indices, pair them, and multiply the number of possible divider positions between each pair of adjacent sections.

## Refining the problem, round 2 thoughts
- Edge cases: total S == 0 -> no valid division (must return 0). Total S odd -> 0. If total S == 2 -> there's exactly one section and no internal divider positions -> only 1 way (do nothing).
- For general case, if seats indices are s0, s1, s2, ..., s_{m-1} where m is total seats and m is even. For adjacent sections, consider gap between s_{2i+1} and s_{2i+2}. The number of valid positions to put a divider in that gap equals (s_{2i+2} - s_{2i+1}) because dividers can be placed at any of the positions between characters; if there are x characters between them (plants count), there are x+1 possible divider positions? Need to double-check: indexes s_a and s_b (s_b > s_a). The positions between s_a and s_b are (s_a+1, s_a+2, ..., s_b). That's s_b-(s_a+1)+1 = s_b - s_a positions. So formula s_{2i+2} - s_{2i+1} is correct.
- Multiply all these gaps modulo 10^9+7.
- Time O(n), space O(number of seats) which is O(n) worst-case; can be optimized to O(1) by single pass recording only last seat positions, but storing indices is simple and safe.

## Attempted solution(s)
```python
class Solution:
    def waysToDivide(self, corridor: str) -> int:
        MOD = 10**9 + 7
        seats = [i for i, ch in enumerate(corridor) if ch == 'S']
        total = len(seats)
        if total == 0 or total % 2 == 1:
            return 0
        if total == 2:
            return 1  # only one section, no internal divider choices

        res = 1
        # For each boundary between sections: between seats[2*i+1] and seats[2*i+2]
        for i in range(1, total // 2):
            left_last = seats[2*i - 1]   # end seat of previous section
            right_first = seats[2*i]     # start seat of next section
            gap_positions = right_first - left_last
            res = (res * gap_positions) % MOD

        return res
```
- Notes:
  - The solution first collects indices of all seats. If the total number of seats is 0 or odd, return 0 because it's impossible to partition into sections of exactly two seats. If exactly 2 seats, there's exactly one way.
  - For each boundary between sections (between the second seat of one section and the first seat of the next), the number of valid divider positions equals the distance in indices between those two seats (right_first - left_last). Multiply those counts modulo 10^9+7.
  - Time complexity: O(n) to scan the string and O(total_seats/2) to compute the product; overall O(n).
  - Space complexity: O(total_seats) to store seat indices (worst-case O(n)). This can be reduced to O(1) by streaming and only keeping the positions of the last seen seats for each pair, but the indexed approach is clear and efficient for constraints (n <= 1e5).