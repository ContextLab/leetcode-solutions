# [Problem 1718: Construct the Lexicographically Largest Valid Sequence](https://leetcode.com/problems/construct-the-lexicographically-largest-valid-sequence/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share internal stream-of-consciousness, but here is a concise summary of the approach:

- We must produce a sequence of length 2*n - 1 where 1 appears once and each i in [2..n] appears twice with distance i between occurrences.
- To get the lexicographically largest sequence, we should try to place larger numbers as early as possible.
- Use backtracking: iterate positions from left to right, and at each empty position try placing numbers from n down to 1 (for i>=2 place at pos and pos+i when available; for 1 place only at pos). Track used numbers and backtrack when a placement leads to a dead end.

## Refining the problem, round 2 thoughts
Refinements and important details:
- Sequence length is 2*n - 1. We maintain an array res of that length filled with zeros initially.
- Keep a used array to avoid placing a number more than required.
- When scanning positions, if current position is already filled skip to next.
- For each empty position, try numbers in descending order to enforce lexicographic maximality.
- For number i >= 2, check that pos + i < length and res[pos] and res[pos+i] are empty.
- For number 1, only a single empty slot is needed.
- As soon as a full valid sequence is constructed, stop and return it (we can return True up the recursion).
- Edge cases: n = 1 (length 1) handled naturally by the algorithm.
- Complexity: this is a backtracking solution. Worst-case time is exponential in n, but n ≤ 20 as constrained by the problem, and pruning + greedy placement order (trying larger numbers first) performs well in practice.

## Attempted solution(s)
```python
class Solution:
    def constructDistancedSequence(self, n: int) -> list:
        length = 2 * n - 1
        res = [0] * length
        used = [False] * (n + 1)

        def backtrack(pos: int) -> bool:
            # find next empty position
            while pos < length and res[pos] != 0:
                pos += 1
            if pos == length:
                return True  # filled all positions successfully

            # try numbers from n down to 1 to get lexicographically largest
            for num in range(n, 0, -1):
                if used[num]:
                    continue
                if num == 1:
                    # place 1 at pos
                    res[pos] = 1
                    used[1] = True
                    if backtrack(pos + 1):
                        return True
                    res[pos] = 0
                    used[1] = False
                else:
                    j = pos + num
                    if j < length and res[j] == 0:
                        # place num at pos and pos + num
                        res[pos] = num
                        res[j] = num
                        used[num] = True
                        if backtrack(pos + 1):
                            return True
                        # backtrack
                        res[pos] = 0
                        res[j] = 0
                        used[num] = False
            return False

        backtrack(0)
        return res
```
- Notes:
  - Approach: backtracking with greedy ordering (try larger numbers first) to produce the lexicographically largest valid sequence.
  - Time complexity: exponential in n in the worst case (backtracking). Practical performance is acceptable for n ≤ 20 due to pruning and the greedy trial order.
  - Space complexity: O(n) extra space for the result array and the used array plus recursion stack (O(n)).