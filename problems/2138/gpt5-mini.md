# [Problem 2138: Divide a String Into Groups of Size k](https://leetcode.com/problems/divide-a-string-into-groups-of-size-k/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to split s into contiguous groups of length k. That's essentially chunking the string by k. For the last chunk, if it's shorter than k, pad with the fill character until length k. The simplest approach is to iterate over s in steps of k, take s[i:i+k], and if its length < k, append fill*(k-len(part)). Another idea is to compute the number of groups needed (ceil(len(s)/k)) and build each group using slicing or using itertools.zip_longest to fill, but slicing is straightforward and clear.

## Refining the problem, round 2 thoughts
Edge cases:
- s length is exactly divisible by k -> no fill needed.
- s length less than k -> single group, fully filled with fill characters after the existing prefix.
- k up to 100, s length up to 100 -> trivial memory/time limits.
Alternative solutions:
- Use for i in range(0, len(s), k).
- Or compute total_groups = math.ceil(len(s)/k) and build each group from s[i*k:(i+1)*k] with padding.
Time/space:
- We process each character once and may add at most (k-1) fill characters. So time O(n + k) and space O(n + k) where n = len(s). For constraints this is optimal and trivial.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def divideString(self, s: str, k: int, fill: str) -> List[str]:
        res = []
        n = len(s)
        for i in range(0, n, k):
            part = s[i:i+k]
            if len(part) < k:
                part += fill * (k - len(part))
            res.append(part)
        # If s is empty it's not possible by constraints, but code handles it.
        return res
```
- Approach: iterate in steps of k, slice each group, pad the final slice if shorter than k with the fill character repeated the required number of times.
- Time complexity: O(n + k) — we visit each character of s once and may add up to k-1 fill characters once. With n = len(s), this is effectively O(n).
- Space complexity: O(n + k) for the output list (stores all original characters plus possible padding up to k-1).
- Implementation details: simple slicing and string multiplication for padding keeps the code concise and clear.