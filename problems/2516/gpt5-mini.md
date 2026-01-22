# [Problem 2516: Take K of Each Character From Left and Right](https://leetcode.com/problems/take-k-of-each-character-from-left-and-right/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can take characters only from the two ends. If we take L characters from the left and R characters from the right, that's equivalent to leaving a contiguous middle substring of length n - (L+R). To minimize minutes (L+R) we want to maximize the length of the middle substring we do not take, subject to the constraint that the taken characters contain at least k of each 'a','b','c'.

So think in terms of the middle substring we leave: for each character c, the number of that character inside the middle substring must be <= total_count[c] - k (otherwise the taken characters won't have k of that char). Thus we need the longest contiguous substring whose counts of each char do not exceed allowed[c] = total_count[c] - k. That is a classic "longest subarray with constraints on counts" problem and can be solved with a sliding window.

Edge checks: if any total_count[c] < k then impossible -> return -1. If k==0, zero minutes.

## Refining the problem, round 2 thoughts
Plan:
- Compute total counts for 'a','b','c'.
- If any total < k return -1.
- Compute allowed[c] = total[c] - k.
- Use two pointers (sliding window) to find the maximum-length window where for every character count_in_window[c] <= allowed[c].
  - Expand right pointer, increment counts.
  - While some count exceeds allowed, move left pointer and decrement counts.
  - Track maximum window length.
- Answer = n - max_window_len (minimum number taken).
Time O(n), space O(1) (constant counters). Careful with mapping chars to indices and with k==0.

## Attempted solution(s)
```python
class Solution:
    def takeCharacters(self, s: str, k: int) -> int:
        n = len(s)
        if k == 0:
            return 0

        # total counts
        total = [0, 0, 0]
        for ch in s:
            total[ord(ch) - ord('a')] += 1

        # if any character total < k -> impossible
        for c in total:
            if c < k:
                return -1

        # maximum allowed occurrences inside the middle window (we leave these)
        allowed = [total[i] - k for i in range(3)]

        # sliding window to find longest window with counts <= allowed
        cnt = [0, 0, 0]
        l = 0
        max_len = 0

        for r, ch in enumerate(s):
            idx = ord(ch) - ord('a')
            cnt[idx] += 1

            # if any count exceeds the allowed, move left pointer
            while (cnt[0] > allowed[0]) or (cnt[1] > allowed[1]) or (cnt[2] > allowed[2]):
                cnt[ord(s[l]) - ord('a')] -= 1
                l += 1

            # window [l..r] is valid
            max_len = max(max_len, r - l + 1)

        # minimum number taken = total length - longest valid middle substring
        return n - max_len
```
- Notes:
  - We convert the "take from ends" problem into finding the longest middle substring we can leave so that the taken prefix+suffix together have at least k of each char.
  - Sliding window ensures O(n) time: each index is visited at most twice (entering and leaving the window).
  - Space is O(1) for fixed-size count arrays of length 3.
  - Handles edge cases: returns -1 if impossible; returns 0 if k==0.