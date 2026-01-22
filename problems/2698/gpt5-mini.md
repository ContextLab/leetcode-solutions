# [Problem 2698: Find the Punishment Number of an Integer](https://leetcode.com/problems/find-the-punishment-number-of-an-integer/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to check, for every i from 1 to n, whether the decimal string of i*i can be partitioned into contiguous substrings whose integer sum equals i. This is a partition / backtracking problem on the string of digits of i*i. For each square string, try all places to cut and accumulate the sum. If at any point the running sum exceeds i we can prune. The squares have limited length since n <= 1000 (i*i <= 1e6 so length <= 7), so brute-force backtracking over partitions is fine.

I also note that substrings like "00" are allowed and evaluate to integer 0; there's no explicit prohibition of leading zeros in substrings in the statement, so we should parse substrings normally (int of substring). Use DFS (or recursion) to try partitions; use simple memoization (idx, remaining) to avoid rechecking equivalent states.

## Refining the problem, round 2 thoughts
We will:
- Convert s = str(i*i).
- Run dfs(index, remaining) returning True if s[index:] can be partitioned to sum to remaining.
- At each index, try taking substring s[index:j] for j in range(index+1, len(s)+1), compute val = int(s[index:j]). If val > remaining we can break because extending the substring will only increase (or stay same in the rare leading-zero case, but practically increasing), so further j won't help — it's still safe since digits appended make number non-decreasing.
- Base case: index == len(s) -> return remaining == 0.
- Use lru_cache to avoid repeated work: cache (index, remaining).
- For each i that passes, add i*i to the total.

Complexity: each square string length L <= 7, backtracking over partitions yields at most O(2^L) partition patterns, so per i it's small. Overall complexity O(n * 2^L) which is fine for n <= 1000. With memoization complexity is even smaller in practice.

Edge cases: i=1 should work; substrings with zeros handled by int parsing; remaining becomes 0 only at exact partition finish.

## Attempted solution(s)
```python
from functools import lru_cache

class Solution:
    def punishmentNumber(self, n: int) -> int:
        def valid(i: int) -> bool:
            s = str(i * i)
            L = len(s)

            @lru_cache(None)
            def dfs(idx: int, rem: int) -> bool:
                if idx == L:
                    return rem == 0
                # If remaining is negative, impossible
                if rem < 0:
                    return False
                val = 0
                # try all substrings starting at idx
                for j in range(idx, L):
                    # build number incrementally to avoid repeated int() cost
                    val = val * 10 + (ord(s[j]) - 48)
                    if val > rem:
                        break
                    if dfs(j + 1, rem - val):
                        return True
                return False

            return dfs(0, i)

        total = 0
        for i in range(1, n + 1):
            if valid(i):
                total += i * i
        return total
```
- Notes:
  - Approach: For each i, backtrack over partitions of the string of i*i, checking if parts sum to i. We incrementally construct substring integers to avoid repeated conversions.
  - Memoization with lru_cache on (idx, rem) avoids redundant exploration.
  - Time complexity: For each i the DFS explores partitions of a string of length L = O(log10(i*i)) (<= 7 for i <= 1000), worst-case O(2^L) states; overall O(n * 2^L) which is tiny for constraints. Space complexity: recursion depth O(L) and memo table O(L * i) in the worst case of distinct remaining values (but small in practice).