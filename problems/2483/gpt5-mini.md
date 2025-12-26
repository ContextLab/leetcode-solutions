# [Problem 2483: Minimum Penalty for a Shop](https://leetcode.com/problems/minimum-penalty-for-a-shop/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to find the earliest hour j (0 <= j <= n) to close so that penalty = (# hours open with no customers) + (# hours closed with customers) is minimized. A brute-force would evaluate penalty for each j by counting N in [0..j-1] and Y in [j..n-1], but that would be O(n^2) if done naively. I can precompute prefix/suffix counts to get O(n). There's also a running-update trick: start with closing at 0 (all hours closed) so penalty = total number of 'Y'. Then when I move the closing time from j to j+1, hour j switches from closed→open: if customers[j]=='Y' penalty decreases by 1, if 'N' penalty increases by 1. So a single pass tracking the running penalty and the earliest index giving minimum penalty should work.

## Refining the problem, round 2 thoughts
Edge cases: all 'N' => best close at 0. All 'Y' => best close at n. Need to ensure ties favor earliest index. Implementation detail: initialize penalty = total Ys (closing at 0). Track min_penalty and best_index = 0. Iterate i from 0..n-1, update penalty per character and consider closing at i+1; if penalty < min_penalty, update min and best_index = i+1. Time O(n), space O(1). This is optimal.

## Attempted solution(s)
```python
class Solution:
    def bestClosingTime(self, customers: str) -> int:
        """
        Compute earliest closing hour to minimize penalty.
        Penalty at close time j: (# of 'N' in [0..j-1]) + (# of 'Y' in [j..n-1])
        Use a running update: start with j=0 -> penalty = total Ys.
        For each i in [0..n-1], moving close from i to i+1:
          - if customers[i] == 'Y': penalty -= 1
          - else (customers[i] == 'N'): penalty += 1
        Check penalty for j = i+1 after each update.
        """
        n = len(customers)
        # penalty for closing at 0: all hours closed => penalty = number of 'Y'
        penalty = customers.count('Y')
        min_penalty = penalty
        best_j = 0

        # Consider closing at j = i+1 for i from 0..n-1
        for i, ch in enumerate(customers):
            if ch == 'Y':
                penalty -= 1
            else:  # ch == 'N'
                penalty += 1

            # Now penalty corresponds to closing at i+1
            if penalty < min_penalty:
                min_penalty = penalty
                best_j = i + 1

        return best_j
```
- Notes:
  - Approach: single pass greedy/rolling update tracking penalty when shifting the closing time one hour forward.
  - Time complexity: O(n) where n = len(customers) (one count + one pass).
  - Space complexity: O(1) extra space.
  - Correctness: initial penalty matches closing at 0; updates reflect moving each hour from closed to open and update penalty accordingly. Ties are resolved by updating only on strictly smaller penalty, so earliest index with minimum penalty is returned.