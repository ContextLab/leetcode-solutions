# [Problem 1888: Minimum Number of Flips to Make the Binary String Alternating](https://leetcode.com/problems/minimum-number-of-flips-to-make-the-binary-string-alternating/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can perform arbitrary rotations (taking first char to end) and flip arbitrary characters. Rotations allow us to consider every cyclic shift of s; for each rotation we want the minimum flips required to make it alternating. A brute force that rotates and counts flips for each rotation would be O(n^2) if done naively.

Observations:
- An alternating string has only two possible patterns for a given length: "0101..." (start with '0') or "1010..." (start with '1').
- Considering rotations is equivalent to checking all length-n substrings of the doubled string s+s.
- So if we build s2 = s + s and slide a window of length n across s2, we can count mismatches to the two alternating templates for each window in O(1) amortized time using a sliding-window mismatch count.

This suggests an O(n) time, O(1) extra space solution.

## Refining the problem, round 2 thoughts
Edge cases:
- n = 1: string is already alternating, answer is 0.
- The sliding-window approach must carefully add the contribution of the incoming character and remove the outgoing one (when window exceeds size n).
- For each index i in s2 we can determine the expected char for both templates by parity: for template0 (start with '0') expected is '0' if i%2==0 else '1'; for template1 it's the opposite.
- Maintain two counters: mismatches to template0 and mismatches to template1 in the current window. When the window size reaches n, update the answer with the minimum of the two counters.
- Complexity: O(n) time (we iterate over 2n chars once, with O(1) updates each step) and O(1) extra space (only counters and indices).

Alternative solutions:
- For even n there's a small optimization: rotation parity doesn't change counts in some way, but the sliding-window approach is simple and uniform for both even and odd n.

## Attempted solution(s)
```python
class Solution:
    def minFlips(self, s: str) -> int:
        n = len(s)
        # If length 1, already alternating
        if n == 1:
            return 0

        s2 = s + s
        # mismatch counts for templates starting with '0' and starting with '1'
        mismatch0 = 0  # mismatches to pattern "0101..."
        mismatch1 = 0  # mismatches to pattern "1010..."
        ans = float('inf')

        for i, ch in enumerate(s2):
            # expected characters for index i for both patterns
            if i % 2 == 0:
                expected0 = '0'
                expected1 = '1'
            else:
                expected0 = '1'
                expected1 = '0'

            if ch != expected0:
                mismatch0 += 1
            if ch != expected1:
                mismatch1 += 1

            # once we have more than n characters in window, remove the leftmost
            if i >= n:
                left = s2[i - n]
                j = i - n
                # expected chars at position j
                if j % 2 == 0:
                    left_expected0 = '0'
                    left_expected1 = '1'
                else:
                    left_expected0 = '1'
                    left_expected1 = '0'

                if left != left_expected0:
                    mismatch0 -= 1
                if left != left_expected1:
                    mismatch1 -= 1

            # when window size is exactly n, update answer
            if i >= n - 1:
                ans = min(ans, mismatch0, mismatch1)

        return ans if ans != float('inf') else 0
```
- Approach: Duplicate the string to consider all rotations as length-n windows of s+s. Maintain mismatch counts to the two alternating templates while sliding a window of size n. For each window compute the minimal flips needed (the fewer mismatches between the two templates).
- Time complexity: O(n) — we scan 2n characters and perform O(1) work per character.
- Space complexity: O(1) extra space (only counters and indices, plus the doubled string s2 which is O(n) but can be considered input-expanded; if strict extra-space counting excludes s2, then O(1)).
- Important detail: computing expected characters by parity avoids building full pattern strings and keeps checks constant-time.