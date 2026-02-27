# [Problem 3666: Minimum Operations to Equalize Binary String](https://leetcode.com/problems/minimum-operations-to-equalize-binary-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to turn a binary string s into all '1's by performing operations that flip exactly k distinct indices each time. Each operation is a k-sized subset of indices; the overall effect is the XOR (symmetric difference) of the chosen subsets over GF(2). The target flip-vector t has 1s where s has '0'. So the problem becomes: represent t as the XOR of m vectors each of Hamming weight exactly k, minimizing m. 

Immediate necessary conditions:
- Parity: sum(t) (number of zeros) ≡ m*k (mod 2).
- Trivial cases: if no zeros -> 0 operations. If k == n then each operation flips all bits; only two possible outcomes (no-op or global flip), so only z==0 or z==n can be achieved.
- For k = 1: each operation flips one bit, so answer is number of zeros.

But parity conditions are not sufficient — for example, one operation of k=3 produces exactly 3 ones (positions flipped), so you cannot obtain 1 flipped bit with a single k=3 operation even if parity allows it. So we need a more precise feasibility condition for a given m: whether we can assign for each index i the number c_i (0..m) of operations that include i so sum c_i = m*k and the number of indices with c_i odd equals z. That leads to integer constraints to check feasibility for given m.

## Refining the problem, round 2 thoughts
Model counts c_i ∈ [0, m] for all n positions. Let T = m*k, r = z (number of indices that must be odd). For indices with odd c_i write c_i = 2a_i + 1, for even indices c_i = 2b_i. Then
T = r + 2 * S where S = sum a_i + sum b_i  (so (T - r) must be even).
Also a_i ≤ (m-1)//2 and b_i ≤ m//2 because c_i ≤ m.
Hence feasibility for given m requires:
- T ≥ r (sum picks at least #odd indices because each odd index needs ≥1 pick),
- (T - r) % 2 == 0,
- Let S = (T - r)//2, then S ≤ r * ((m-1)//2) + (n-r) * (m//2).

So for minimal m we can iterate m from 1..n (0 handled earlier) and test these conditions. If none works return -1.

Time complexity: O(n) iterations with O(1) checks each = O(n). n up to 1e5 fits.

Edge cases handled explicitly:
- z == 0 -> return 0
- k == n -> only z==0 -> 0 or z==n -> 1 else -1

This approach is simple, robust and matches the combinatorial feasibility constraints.

## Attempted solution(s)
```python
class Solution:
    def minOperations(self, s: str, k: int) -> int:
        n = len(s)
        z = s.count('0')
        if z == 0:
            return 0
        # Special case: k == n -> each operation flips all bits.
        if k == n:
            # Only possible to make all ones if s already all ones (z==0) or s all zeros (one flip)
            return 1 if z == n else -1

        # Try m from 1..n (0 already handled). For each m check feasibility.
        for m in range(1, n + 1):
            T = m * k
            # must have at least one pick per odd-index (each odd c_i >= 1)
            if T < z:
                continue
            # parity constraint: T and z must have same parity
            if (T - z) & 1:
                continue
            S = (T - z) // 2
            # capacity is how many pairs (2 picks) we can allocate across indices given upper bounds
            cap = z * ((m - 1) // 2) + (n - z) * (m // 2)
            if S <= cap:
                return m
        return -1
```
- Notes about the solution approach:
  - We convert the problem into a feasibility check for counts c_i ∈ [0, m] that sum to T = m*k and have exactly z indices with odd c_i.
  - The algebraic reduction leads to checking parity, minimum total picks, and whether the remainder S = (T - z)/2 can be distributed within per-index pair capacities ((m-1)//2 for odd indices, m//2 for even indices).
  - We handle k == n explicitly because all operations are identical in that case.
  - Complexity: O(n) time and O(1) extra space (beyond input).