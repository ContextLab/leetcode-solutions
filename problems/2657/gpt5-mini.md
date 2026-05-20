# [Problem 2657: Find the Prefix Common Array of Two Arrays](https://leetcode.com/problems/find-the-prefix-common-array-of-two-arrays/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to compute for each index i how many numbers among 1..n appear in both A[0..i] and B[0..i]. Since A and B are permutations, each value appears exactly once overall, so I can track whether a value has appeared in the prefix of A and whether it has appeared in the prefix of B. A straightforward approach is to maintain two sets (or boolean arrays) seenA and seenB and update them as i increases; whenever a newly seen element in one array was already seen in the other array, the prefix-common count should increase by one. This avoids re-scanning prefixes for each i and will be linear time.

## Refining the problem, round 2 thoughts
- Using boolean arrays of size n+1 is slightly faster and simpler than sets because values range 1..n.
- For each i, I should mark A[i] and B[i] as seen. To avoid double counting when A[i] == B[i] or when both new, I should increment the common count only when marking an element that was unseen in that array but already seen in the other array.
- Edge cases: n = 1 should work; permutations guarantee no duplicates across positions so logic simplifies.
- Time complexity: O(n). Space complexity: O(n) for the seen arrays and result.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findPrefixCommonArray(self, A: List[int], B: List[int]) -> List[int]:
        n = len(A)
        seenA = [False] * (n + 1)
        seenB = [False] * (n + 1)
        res = []
        common = 0

        for i in range(n):
            a = A[i]
            b = B[i]
            # Mark a in A if not seen before; if it was already seen in B, it becomes common now
            if not seenA[a]:
                seenA[a] = True
                if seenB[a]:
                    common += 1
            # Mark b in B if not seen before; if it was already seen in A, it becomes common now
            if not seenB[b]:
                seenB[b] = True
                if seenA[b]:
                    common += 1

            res.append(common)

        return res
```
- Notes:
  - We use two boolean arrays seenA and seenB to record which values have appeared in the prefixes so far.
  - For each index i, when we first mark a value in one array, we check whether it was already seen in the other array; if so, the number of common elements increases by 1.
  - This avoids double-counting (handles A[i] == B[i] correctly).
  - Time complexity: O(n) where n = len(A).
  - Space complexity: O(n) for the seen arrays and the result list.