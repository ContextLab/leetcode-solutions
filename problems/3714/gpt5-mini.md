# [Problem 3714: Longest Balanced Substring II](https://leetcode.com/problems/longest-balanced-substring-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share private chain-of-thought, but here is a concise summary of the high-level idea:
- Because the alphabet is only {'a','b','c'}, consider each non-empty subset of characters that might be the distinct characters of a balanced substring (7 subsets).
- For a given subset T, valid substrings must contain only characters from T and each character in T must appear the same number of times.
- Split the string into segments that contain only characters from T (characters not in T act as separators). Within each segment use prefix-difference hashing:
  - For |T|=1: longest run of that character.
  - For |T|=2: map one char to +1 the other to -1 and find longest subarray with sum 0 (prefix sum first-seen map).
  - For |T|=3: use two differences (count_a-count_b, count_a-count_c) and find longest subarray where the pair repeats.

This yields an O(n) scan per subset → overall O(7n) time, O(n) space worst-case.

## Refining the problem, round 2 thoughts
Refinements and edge considerations:
- Substrings with a single distinct character are balanced (all distinct characters—just one—appear the same number of times).
- For two-character subsets, equality reduces to zero net difference; prefix-sum + hashmap finds maximum length efficiently.
- For three-character subset, two independent differences fully characterize equality; use a 2D key in a hashmap.
- We must reset prefix bookkeeping whenever we hit a character not in the current subset (segment boundary).
- Complexity: For each of 7 subsets we scan s once, so time O(7n) = O(n). Space is O(n) in worst-case for hashmaps used inside segments.

## Attempted solution(s)
```python
from typing import Dict, Tuple

class Solution:
    def longestBalanced(self, s: str) -> int:
        n = len(s)
        if n == 0:
            return 0
        chars = ['a', 'b', 'c']
        ans = 1  # at least one char substring is balanced if s is non-empty

        # iterate all non-empty subsets of {'a','b','c'} via bitmask 1..7
        for mask in range(1, 1 << 3):
            T = {chars[i] for i in range(3) if (mask >> i) & 1}
            d = len(T)
            if d == 1:
                # longest run of the single character
                target = next(iter(T))
                cur = 0
                for ch in s:
                    if ch == target:
                        cur += 1
                        if cur > ans:
                            ans = cur
                    else:
                        cur = 0
                continue

            # For d == 2 or d == 3 we process contiguous segments consisting only of chars in T
            i = 0
            while i < n:
                # skip until a char in T
                if s[i] not in T:
                    i += 1
                    continue
                j = i
                while j < n and s[j] in T:
                    j += 1
                seg = s[i:j]
                seg_len = j - i

                if d == 2:
                    # pick two chars in deterministic order
                    a, b = sorted(T)
                    prefix = 0
                    first_seen: Dict[int, int] = {0: -1}
                    for idx, ch in enumerate(seg):
                        if ch == a:
                            prefix += 1
                        else:
                            prefix -= 1
                        if prefix in first_seen:
                            length = idx - first_seen[prefix]
                            if length > ans:
                                ans = length
                        else:
                            first_seen[prefix] = idx
                else:  # d == 3
                    a, b, c = sorted(T)
                    ca = cb = cc = 0
                    first_seen: Dict[Tuple[int,int], int] = {(0, 0): -1}
                    for idx, ch in enumerate(seg):
                        if ch == a:
                            ca += 1
                        elif ch == b:
                            cb += 1
                        else:
                            cc += 1
                        key = (ca - cb, ca - cc)
                        if key in first_seen:
                            length = idx - first_seen[key]
                            if length > ans:
                                ans = length
                        else:
                            first_seen[key] = idx

                i = j

        return ans
```
- Notes:
  - We consider all 7 non-empty subsets of {'a','b','c'}. For each subset we only allow segments composed solely of those characters (others break segments).
  - For 1 character: longest run is the answer for that subset.
  - For 2 characters: convert to +1/-1 prefix sum and track earliest occurrence of each prefix sum to get max zero-sum subarray length.
  - For 3 characters: track two differences (count_a - count_b, count_a - count_c); repeating the same pair of differences indicates equal per-character counts in the subarray.
  - Time complexity: O(7 * n) = O(n). Space: O(n) worst-case for the hashmaps used per segment.