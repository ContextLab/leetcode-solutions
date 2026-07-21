# [Problem 3499: Maximize Active Section with Trade I](https://leetcode.com/problems/maximize-active-section-with-trade-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have a binary string s, and are allowed exactly one two-step "trade": (1) pick a contiguous block of '1's that is surrounded by '0's and turn it to '0's; (2) then pick a contiguous block of '0's that is surrounded by '1's (in the string after step 1) and turn it to '1's. We augment s with '1' at both ends conceptually, but those augmented ones don't count in the result.

The naive thought: final ones count = original_ones - removed_ones_len + added_zero_len. But step (1) may merge adjacent zero blocks with the removed one block, so step (2) could flip a much larger zero-block (the merged one). In particular, if we remove a one-run whose left and right neighbors are zero-runs of lengths L and R, those will merge into a zero-run of length L + removed_len + R, and flipping that merged run adds L + removed_len + R back. The removed_len cancels: net gain = L + R. So one promising candidate for each removable one-run is total_ones + L + R.

We can also consider flipping some other zero-run (not adjacent) after removing a one-run elsewhere; then net gain is total_ones - removed_len + some_zero_len. So for each removable one-run, consider both merged (L + R) and best non-adjacent zero-run (best_zero_len_not_adjacent - removed_len). We also must consider doing no trade.

We need to enumerate runs and analyze efficiently.

## Refining the problem, round 2 thoughts
Plan:
- Build t = '1' + s + '1' and compress into runs (char, length).
- total_ones = s.count('1') (augmented ones should not be counted).
- Identify zero-run entries (length, run_index) in the compressed t.
- Identify removable one-runs in t: a run of '1' that has zeros both sides (i.e., neighbors are '0'). These are valid for step (1).
- For each removable one-run at index i with length A and adjacent zero lengths L (left) and R (right):
  - merged candidate final = total_ones + L + R   (removal merges L + A + R then flipping adds that; A cancels)
  - non-adjacent candidate final = total_ones - A + best_zero_len where best_zero_len is the largest zero-run length whose run index != i-1 and != i+1 (so it wasn't one of the two zeros merged).
- Track maximum among all removable one-runs and also include baseline total_ones (no trade).
- Implementation detail: to find best_zero_len_not_adjacent quickly, get the top-3 zero-runs (by length). For each i, pick the first top-K whose index is not i-1 or i+1. Top-3 suffices because at most two zero-runs are disallowed.
- Complexity: building runs O(n), scanning zeros O(n), sorting zero-runs would be O(m log m) where m<=n, but we can extract top-3 in O(n) too. Overall O(n) time and O(n) memory.

Edge cases:
- No removable one-runs -> cannot trade -> answer = total_ones.
- No zero-runs -> cannot flip any zero block -> no trade -> answer = total_ones.
- Handle small n correctly.

Now implement.

## Attempted solution(s)
```python
class Solution:
    def maximizeActive(self, s: str) -> int:
        # Build augmented string t = '1' + s + '1' and compress into runs
        t = '1' + s + '1'
        runs = []  # list of (char, length)
        cur = t[0]
        cnt = 1
        for ch in t[1:]:
            if ch == cur:
                cnt += 1
            else:
                runs.append((cur, cnt))
                cur = ch
                cnt = 1
        runs.append((cur, cnt))

        n = len(s)
        total_ones = s.count('1')

        # Collect zero runs (length, index in runs)
        zero_runs = []
        for idx, (ch, ln) in enumerate(runs):
            if ch == '0':
                zero_runs.append((ln, idx))

        # If there are no removable one-runs or no zero runs, answer is total_ones
        if not zero_runs:
            return total_ones

        # Get top-3 zero runs by length
        zero_runs_sorted = sorted(zero_runs, key=lambda x: x[0], reverse=True)
        topk = zero_runs_sorted[:3]  # list of (len, idx)

        ans = total_ones

        # For each removable one-run (one-run having zeros both sides)
        m = len(runs)
        for i in range(m):
            ch, one_len = runs[i]
            if ch != '1':
                continue
            # must have neighbors and both zeros
            if i - 1 < 0 or i + 1 >= m:
                continue
            if runs[i - 1][0] != '0' or runs[i + 1][0] != '0':
                continue

            left_zero = runs[i - 1][1]
            right_zero = runs[i + 1][1]

            # Candidate 1: remove this one-run and then flip the merged zero-run (left + one + right)
            # net effect is total_ones + left_zero + right_zero
            ans = max(ans, total_ones + left_zero + right_zero)

            # Candidate 2: remove this one-run and flip the best zero-run that is NOT i-1 or i+1
            banned = {i - 1, i + 1}
            chosen_zero_len = 0
            for zl, zidx in topk:
                if zidx not in banned:
                    chosen_zero_len = zl
                    break
            if chosen_zero_len > 0:
                candidate = total_ones - one_len + chosen_zero_len
                ans = max(ans, candidate)

        return ans

# For compatibility with LeetCode expected class/method naming:
# LeetCode problem provides a function signature maximizeActive(self, s: str) -> int
# If running as Solution().maximizeActive(s) it will work.
```
- Notes:
  - We compress the augmented string t = '1' + s + '1', which naturally handles boundaries (augmented ones merge with edge ones if present).
  - total_ones is counted only from s (augmented ones are ignored in the final count).
  - For each removable one-run (a '1' run with zero neighbors), two main cases are considered:
    - Flipping the merged zero-block formed by removing that one-run → net increase = left_zero + right_zero (removed ones cancel).
    - Flipping some other zero-block not adjacent to the removed one-run → net increase = best_zero_len_not_adjacent - removed_one_len.
  - We take the maximum over all removable one-runs and compare with doing no trade.
  - Time complexity: O(n) to build runs and scan (sorting top zero runs is limited to extracting top-3; implemented as sort on zero runs which is O(m log m) worst-case but m ≤ n). Overall O(n log n) worst-case if sorting used; can be optimized to pure O(n) by scanning to get top-3 zero runs.
  - Space complexity: O(n) to store runs.