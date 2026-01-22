# [Problem 1963: Minimum Number of Swaps to Make the String Balanced](https://leetcode.com/problems/minimum-number-of-swaps-to-make-the-string-balanced/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the minimum number of swaps of any two indices to make the bracket string balanced. Since number of '[' equals number of ']', a solution always exists. Swapping arbitrary positions means we can move any '[' leftwards (or any ']' rightwards) as needed. I remember that the important metric is how far the prefix balance goes negative — that is, how many more ']' than '[' we have at worst. Intuitively each swap can fix two unmatched brackets in the worst prefix deficiency (you swap a '[' from the right into earlier position to pair with a pending ']'), so the answer should be ceil(max deficit / 2). I'll compute a running balance (+1 for '[', -1 for ']') and track the minimum balance (most negative). Convert that to swaps.

## Refining the problem, round 2 thoughts
Edge cases:
- Already balanced string: min balance = 0 -> 0 swaps.
- Example "]]][[[" has max deficit 3 -> ceil(3/2) = 2 swaps (matches examples).
We only need O(n) time and O(1) extra space since n can be up to 1e6. Implementation detail: track balance and min_balance (or track max deficit as -min_balance), then return (deficit + 1) // 2. This is simple and robust.

Alternative approaches:
- Greedy simulation counting unmatched closing brackets and performing swaps when encountering '[' from right; that can be done but reasoning and implementations vary — the min_balance approach is concise and proven.

Time complexity: O(n). Space complexity: O(1).

## Attempted solution(s)
```python
class Solution:
    def minSwaps(self, s: str) -> int:
        # balance: +1 for '[', -1 for ']'
        balance = 0
        min_balance = 0  # most negative balance seen
        for ch in s:
            if ch == '[':
                balance += 1
            else:
                balance -= 1
            if balance < min_balance:
                min_balance = balance

        # If min_balance is >= 0, already balanced -> 0 swaps.
        # Otherwise deficit = -min_balance is the maximum number of extra ']' at some prefix.
        deficit = -min_balance
        # Each swap can fix two of these deficits, so answer = ceil(deficit / 2)
        return (deficit + 1) // 2
```
- Notes:
  - We traverse once maintaining a running balance; min_balance captures the worst (most negative) prefix.
  - deficit = -min_balance is the maximum number of unmatched closing brackets at any point.
  - Minimum swaps = ceil(deficit / 2) = (deficit + 1) // 2 using integer arithmetic.
  - Time complexity: O(n). Space complexity: O(1). This handles n up to 1e6 efficiently.