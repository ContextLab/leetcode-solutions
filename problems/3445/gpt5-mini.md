# [Problem 3445: Maximum Difference Between Even and Odd Frequency II](https://leetcode.com/problems/maximum-difference-between-even-and-odd-frequency-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the maximum freq[a] - freq[b] over substrings of length >= k, where a appears an odd number of times and b appears a non-zero even number of times. s only contains digits '0'..'4' so alphabet size is 5 — small. That suggests we can afford an approach that tries all ordered pairs (a, b) (a != b) and solves for each pair efficiently.

For a fixed pair (a, b) consider an array delta: +1 for a, -1 for b, 0 otherwise. Then for any substring the difference freq[a] - freq[b] equals the sum of delta over that substring. Sum over substring l..r = prefDiff[r+1] - prefDiff[l], where prefDiff is prefix of delta. So maximizing this over valid l with constraints is like choosing the minimum prefDiff[l] among l allowed.

We also have parity constraints:
- freq[a] odd => (prefA[r+1] - prefA[l]) is odd => parity(prefA[r+1]) != parity(prefA[l]).
- freq[b] even => parity(prefB[r+1]) == parity(prefB[l]), and non-zero even means prefB[r+1] - prefB[l] >= 2.

We can iterate r (end index) and maintain eligible l positions (those with l <= r-k+1) in some data structure keyed by (parityA_l, parityB_l, prefB[l]) holding minimal prefDiff[l]. For a given r we need min prefDiff[l] among items with parityA_l != parityA_r, parityB_l == parityB_r, and prefB[l] <= prefB[r+1] - 2. That's a prefix-min query on prefB dimension. So for each (pA, pB) parity pair we can maintain a Fenwick/BIT that supports point update of min and prefix-min query. Alphabet is small so doing this for each (a,b) pair is fine.

This leads to O(alphabet^2 * n log n) which is acceptable: 25 * 3e4 * log(3e4) ~ around 1e7 operations.

## Refining the problem, round 2 thoughts
Refinements/edge cases:
- Use prefix arrays of length n+1: pref counts for a and b, prefDiff = prefA - prefB, parity arrays pa, pb.
- For substring l..r length >= k, when we iterate r from 0..n-1, allowed l indices to be considered are 0..(r-k+1). We'll add prefix index j = r-k+1 into DS as r grows.
- For each r, the right prefix index is R = r+1. We need parity condition pa[l] != pa[R] and pb[l] == pb[R]. We also need prefB[l] <= prefB[R] - 2.
- For correct BIT indexing map prefB value (0..n) to 1..n+1 indices.
- For each pair (a,b) create 4 Fenwick trees (for parity combinations) of size n+1 and update/query as we go; reuse and discard per pair to save memory.
- Complexity: O(25 * n * log n) time and O(n) extra memory per pair (Fenwicks), overall good.

Now produce a clean implementation.

## Attempted solution(s)
```python
from typing import List
import math

class FenwickMin:
    """Fenwick / BIT for prefix-min queries with point 'min' updates.
    Indices are 1-based inside. Size is n (number of distinct prefB values).
    """
    def __init__(self, n: int):
        self.n = n
        INF = 10**9
        self.tree = [INF] * (n + 1)

    def update_min(self, idx: int, val: int):
        # idx: 1-based
        n = self.n
        tree = self.tree
        while idx <= n:
            if val < tree[idx]:
                tree[idx] = val
            else:
                # if current stored is smaller, future indices won't be improved by this val,
                # but still other branches might need it; we can early exit only if val >= tree[idx]
                # but standard approach continues; early exit is optional.
                pass
            idx += idx & -idx

    def query_min(self, idx: int) -> int:
        # min over [1..idx], idx: 1-based
        INF = 10**9
        res = INF
        tree = self.tree
        while idx > 0:
            if tree[idx] < res:
                res = tree[idx]
            idx -= idx & -idx
        return res

class Solution:
    def maxDifference(self, s: str, k: int) -> int:
        n = len(s)
        # convert characters '0'..'4' to ints 0..4
        arr = [ord(c) - ord('0') for c in s]
        ALPH = 5
        INF = 10**9
        ans = -10**9  # will take max; problem ensures at least one valid substring exists globally
        
        # for each ordered pair (a, b), a != b
        for a in range(ALPH):
            for b in range(ALPH):
                if a == b:
                    continue
                # build prefix arrays for a and b and prefDiff
                prefA = [0] * (n + 1)
                prefB = [0] * (n + 1)
                prefDiff = [0] * (n + 1)  # prefA - prefB
                for i in range(n):
                    prefA[i+1] = prefA[i] + (1 if arr[i] == a else 0)
                    prefB[i+1] = prefB[i] + (1 if arr[i] == b else 0)
                    prefDiff[i+1] = prefA[i+1] - prefB[i+1]
                # parity arrays
                pa = [x & 1 for x in prefA]
                pb = [x & 1 for x in prefB]

                # Fenwick trees for four parity pairs (pa_l, pb_l): index by prefB value (0..n) -> 1..n+1
                size = n + 1
                # mapping (pA, pB) -> FenwickMin
                fens = {}
                for pA in (0,1):
                    for pB in (0,1):
                        fens[(pA,pB)] = FenwickMin(size)

                # We'll add prefix index j when it becomes eligible: j <= r-k+1 -> j = r-k+1 as r increases
                # iterate r from 0..n-1
                # initially no l added
                for r in range(n):
                    j = r - k + 1
                    if j >= 0:
                        # add prefix index j (which corresponds to substring start l=j)
                        pA_j = pa[j]
                        pB_j = pb[j]
                        prefB_j = prefB[j]
                        val_j = prefDiff[j]
                        fen = fens[(pA_j, pB_j)]
                        fen.update_min(prefB_j + 1, val_j)  # +1 for 1-based index

                    # Now consider right prefix R = r+1
                    R = r + 1
                    pA_R = pa[R]
                    pB_R = pb[R]
                    prefB_R = prefB[R]
                    prefDiff_R = prefDiff[R]
                    # need pa_l != pA_R and pb_l == pB_R
                    need_pA = 1 - pA_R
                    need_pB = pB_R
                    fen_need = fens[(need_pA, need_pB)]
                    # require prefB[l] <= prefB[R] - 2  -> limit = prefB_R - 2
                    limit = prefB_R - 2
                    if limit >= 0:
                        # query prefix min upto limit (map to 1-based index)
                        best = fen_need.query_min(limit + 1)
                        if best < INF:
                            cand = prefDiff_R - best
                            if cand > ans:
                                ans = cand
                # done pair

        # If ans remained very small, return something (though constraints say at least one substring has valid a and b)
        return ans if ans != -10**9 else -10**9
```
- Notes:
  - Approach: iterate all ordered pairs (a, b), build prefix counts prefA, prefB and prefDiff. For each ending index r consider all eligible starting prefix indices l (we add them as r grows) that satisfy substring length >= k. For parity and b-frequency constraints we maintain four Fenwick trees keyed by prefB[l], storing minimal prefDiff[l]. For a given r we query the tree corresponding to parity constraints and take prefix-min up to prefB[r+1]-2 to ensure freq_b >= 2 (even and non-zero).
  - Time complexity: O(ALPH^2 * n * log n) where ALPH = 5. With n up to 3e4 this is fine. More concretely ~25 * n * log n operations.
  - Space complexity: O(n) extra per pair (Fenwick arrays of size n+1). We reuse per pair so peak extra memory is O(n).
  - Important details:
    - Use prefix indices (0..n) so substring l..r corresponds to prefix indices l and r+1.
    - Map prefB values 0..n to Fenwick indices 1..n+1.
    - Parity constraints are checked by comparing prefix parities at endpoints.
    - We require freq_b to be a non-zero even integer, ensured by prefB[r+1] - prefB[l] >= 2 and parity equality (so difference is even).