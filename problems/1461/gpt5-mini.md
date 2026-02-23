# [Problem 1461: Check If a String Contains All Binary Codes of Size K](https://leetcode.com/problems/check-if-a-string-contains-all-binary-codes-of-size-k/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share internal stream-of-consciousness. Brief summary instead: the natural approach is to treat each length-k substring as a k-bit integer and track which integers appear. Use a rolling bitmask to compute each substring's integer value in O(1) per step and record seen codes in a boolean array (or set). Return true once all 2^k codes are seen, or false if we finish without seeing them all.

## Refining the problem, round 2 thoughts
- If k > len(s), immediately return False.
- There are 2^k possible binary codes. If the number of k-length substrings (n - k + 1) is less than 2^k, it's impossible to have all codes — can return False early (optional).
- Use a rolling integer "window" of the last k bits:
  - shift left, add current bit, mask with (1<<k)-1 to keep only k bits.
  - Start recording only after we've read k characters (i >= k-1).
- Use a boolean list of size 2^k (faster and lower overhead than a Python set when k <= 20).
- Time complexity: O(n). Space complexity: O(2^k).

## Attempted solution(s)
```python
class Solution:
    def hasAllCodes(self, s: str, k: int) -> bool:
        n = len(s)
        if k > n:
            return False

        total = 1 << k
        # Optional early exit: if there aren't enough substrings to cover all codes
        if n - k + 1 < total:
            return False

        seen = [False] * total
        mask = total - 1
        cur = 0
        count = 0

        for i, ch in enumerate(s):
            # add current bit
            cur = ((cur << 1) & mask) | (1 if ch == '1' else 0)
            if i >= k - 1:
                if not seen[cur]:
                    seen[cur] = True
                    count += 1
                    if count == total:
                        return True

        return False
```
- Notes:
  - Approach: rolling window as integer; mark seen codes in a boolean array sized 2^k.
  - Time complexity: O(n) where n = len(s) since each character is processed once.
  - Space complexity: O(2^k) for the seen array (k <= 20 so at most ~1,048,576 entries).
  - This is efficient and fits within constraints (n up to 5e5, k up to 20). Alternative (simpler) solution: collect all substrings of length k in a set and check its size, but that uses more memory and string slicing overhead.