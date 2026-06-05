# [Problem 3753: Total Waviness of Numbers in Range II](https://leetcode.com/problems/total-waviness-of-numbers-in-range-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the total number of peaks+valleys across all numbers in [num1, num2]. A naive loop would be impossible because num2 can be up to 1e15. Waviness is local to each triple of adjacent digits: a middle digit is a peak/valley if it is strictly greater/less than both neighbors. That suggests a digit-DP approach: for each number we can look at each time we place a new digit we can decide whether the previous digit (the middle of a triple) was a peak/valley. So I can build a DP over positions that carries the last two digits (or sentinels if not present), a started/leading-zero flag, and tight. The DP should return both count of numbers and total waviness sum so we can accumulate contributions when a peak/valley is determined.

I must be careful with leading zeros and numbers shorter than 3 digits (they contribute 0 waviness). Also need inclusive range so compute f(n) = total waviness for [0, n] and return f(num2) - f(num1-1).

## Refining the problem, round 2 thoughts
State: position index, prev2, prev1, started (whether we've seen a non-leading-zero digit), tight flag. prev2 and prev1 can be -1 when undefined. Transition: try digit d up to limit; update started and prevs; when prev2 != -1 (meaning we already had at least two digits) then adding digit d lets us check whether prev1 is peak or valley using prev2, prev1, d. If yes, we add 1 to the waviness count for every number in the subtree where this choice is made. Use memoization to avoid recomputing subproblems. Base case: when we've processed all digits, return count = 1 (we count the formed number, including 0) and total waviness 0 for this leaf. Final answer is f(num2) - f(num1-1).

Complexity: positions ~ up to 16 (since n <= 1e15), prev2/prev1 values 11 each (-1..9) → ~11*11 states, started 2, tight 2 → fairly small. Each state loops digits 0..9 at most. So approx 16*11*11*2*2*10 ~ tens of thousands ops → fast.

Edge cases: num1 could be 1; compute f(0) works because base counts include 0, but waviness for numbers with <3 digits is 0 anyway. If num1==0 we'd still handle. Ensure correct handling of leading zeros so short numbers don't produce spurious peaks/valleys.

## Attempted solution(s)
```python
import functools
import sys

sys.setrecursionlimit(10000)

class Solution:
    def totalWaviness(self, num1: int, num2: int) -> int:
        # Helper: compute total waviness for all numbers in [0, n]
        def f(n: int) -> int:
            if n < 0:
                return 0
            digits = list(map(int, str(n)))
            L = len(digits)

            @functools.lru_cache(None)
            def dfs(pos: int, prev2: int, prev1: int, started: int, tight: int):
                # returns (count_of_numbers, total_waviness_sum) for suffix starting at pos
                if pos == L:
                    # one formed number (including zero); waviness sum 0 at leaf
                    return (1, 0)
                limit = digits[pos] if tight else 9
                total_count = 0
                total_wav = 0
                for d in range(0, limit + 1):
                    next_tight = tight and (d == limit)
                    next_started = started or (d != 0)
                    # determine next prevs
                    if not started:
                        # no previous digits yet
                        if d == 0:
                            # still leading zeros
                            n_prev2, n_prev1 = -1, -1
                        else:
                            # first non-zero digit -> prev1 becomes d, prev2 undefined
                            n_prev2, n_prev1 = -1, d
                    else:
                        # already started -> shift prevs; prev1 could be 0..9 even if d==0
                        n_prev2, n_prev1 = prev1, d
                    # compute add: does this placement make prev1 a peak/valley?
                    add = 0
                    # prev2 must be defined to have a triple prev2, prev1, d
                    if prev2 != -1:
                        # prev1 and prev2 defined (prev1 is guaranteed defined if prev2 != -1)
                        if (prev1 > prev2 and prev1 > d) or (prev1 < prev2 and prev1 < d):
                            add = 1
                    child_count, child_wav = dfs(pos + 1, n_prev2, n_prev1, 1 if next_started else 0, 1 if next_tight else 0)
                    total_count += child_count
                    total_wav += child_wav + add * child_count
                return (total_count, total_wav)

            # initial prevs are undefined (-1), started flag 0, tight 1
            return dfs(0, -1, -1, 0, 1)[1]

        return f(num2) - f(num1 - 1)


# Example usage to integrate with typical LeetCode style:
if __name__ == "__main__":
    sol = Solution()
    # Sample tests
    print(sol.totalWaviness(120, 130))  # expected 3
    print(sol.totalWaviness(198, 202))  # expected 3
    print(sol.totalWaviness(4848, 4848))  # expected 2
```

- Notes about the solution:
  - We use digit dynamic programming (top-down with memoization). The DFS state tracks position, prev2, prev1 (digits or -1 if undefined), whether we've started the number (to handle leading zeros), and tightness to the upper bound digits.
  - When we place a digit d, if there are already two previous digits (prev2 != -1), we can determine whether prev1 is a peak or valley by comparing prev2, prev1, and d. If so, we add 1 to waviness for every number in that subtree, which is accounted by child_count.
  - f(n) computes total waviness for [0, n]. The final answer is f(num2) - f(num1 - 1).
  - Time complexity: O(L * 11 * 11 * 2 * 2 * 10) roughly, where L is number of digits (~16), so very fast. Space complexity: memoization table size proportional to states: O(L * 11 * 11 * 2 * 2).
  - Careful handling of leading zeros ensures numbers with <3 digits never produce peaks/valleys.