# [Problem 2657: Find the Prefix Common Array of Two Arrays](https://leetcode.com/problems/find-the-prefix-common-array-of-two-arrays/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need C[i] = count of numbers that appear in A[0..i] and also in B[0..i]. A and B are permutations of 1..n. A straightforward approach is to maintain sets of seen elements for A and B as we sweep i from 0..n-1 and compute the intersection size each time. That would be simple and correct. Because n ≤ 50, recomputing the intersection every step is acceptable.

But we can do even better: maintain a running count of "common" elements and update it incrementally. When we see a new element in A's prefix, if that element was already seen in B's prefix we increment the common count. Similarly for a new element seen in B, if it was already seen in A we increment. Careful: if both A[i] and B[i] are the same value or if one of them was already seen in the other prefix, we must avoid double counting — so check whether the occurrence is newly added to that prefix before using it to increment the count.

## Refining the problem, round 2 thoughts
Refinement: track two boolean arrays (or sets) seenA and seenB. For each index i:
- Let x = A[i]. If x was not seen in A before and x is already seen in B, increment common_count. Then mark x seen in A.
- Let y = B[i]. If y was not seen in B before and y is already seen in A, increment common_count. Then mark y seen in B.

This handles A[i] == B[i] correctly and avoids double counting because we only increment when the element is newly introduced into that prefix. Time complexity O(n), space O(n). Edge cases: n=1 works fine. Since A and B are permutations, we don't need to handle duplicates other than the same value at the same index.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findPrefixCommonArray(self, A: List[int], B: List[int]) -> List[int]:
        n = len(A)
        seenA = [False] * (n + 1)  # values are 1..n
        seenB = [False] * (n + 1)
        common = 0
        res = [0] * n

        for i in range(n):
            a = A[i]
            b = B[i]

            # If a is newly seen in A and was already seen in B, it becomes a common element.
            if not seenA[a]:
                if seenB[a]:
                    common += 1
                seenA[a] = True

            # If b is newly seen in B and was already seen in A, it becomes a common element.
            # Note: this check uses the state after we may have updated seenA above, which is correct.
            if not seenB[b]:
                if seenA[b]:
                    common += 1
                seenB[b] = True

            res[i] = common

        return res
```
- Notes on solution approach:
  - We sweep once from left to right, updating seen sets/arrays and a running common count.
  - The order of processing A[i] first then B[i] is fine; because we only increment when an element is newly added to its prefix, we avoid double counting even when A[i] == B[i].
- Complexity:
  - Time: O(n) — single pass over the arrays with O(1) work per index.
  - Space: O(n) — two boolean arrays of size n+1 and the output array of size n.