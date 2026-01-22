# [Problem 3337: Total Characters in String After Transformations II](https://leetcode.com/problems/total-characters-in-string-after-transformations-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We replace every character by a fixed sequence of next nums[c] letters (wrapping mod 26). Each transformation is linear: the count of each output letter after one transformation is a linear combination of the counts of input letters. That suggests modeling the process with a 26x26 integer matrix M where column x describes how a single character x contributes to output letters. After t transformations the resulting counts vector is M^t times the initial counts vector. We only need the total length (sum of all letter counts), so we can compute M^t, apply it to the initial frequency vector, and sum entries modulo 1e9+7. Matrix exponentiation by fast exponentiation (log t) is feasible because 26 is small.

## Refining the problem, round 2 thoughts
- Build M where M[y][x] = 1 if y is among the next nums[x] letters from x (with wrap), else 0.
- Compute M^t using fast exponentiation with matrix multiplication mod MOD (MOD = 10**9 + 7).
- Compute final_counts = M^t * initial_counts and return sum(final_counts) % MOD.
- Complexity: matrix multiplication is O(26^3) ~ constant; exponentiation adds a factor of log t (~30). Counting initial frequencies is O(len(s)).
- Edge cases: t >= 1 guaranteed by constraints, but algorithm handles any t >= 0 (t == 0 -> identity, length = len(s)). Ensure modulo at every accumulation to avoid overflow.

## Attempted solution(s)
```python
MOD = 10**9 + 7

class Solution:
    def totalCharacters(self, s: str, t: int, nums: list[int]) -> int:
        # Build transition matrix M of size 26x26: M[row][col]
        # A single character 'col' (0..25) transforms into nums[col] letters:
        # for j in 1..nums[col]: row = (col + j) % 26; M[row][col] += 1
        M = [[0] * 26 for _ in range(26)]
        for x in range(26):
            k = nums[x]
            for j in range(1, k + 1):
                y = (x + j) % 26
                M[y][x] += 1

        # Matrix multiplication: A * B (26x26 matrices)
        def mat_mul(A, B):
            n = 26
            C = [[0] * n for _ in range(n)]
            for i in range(n):
                Ai = A[i]
                Ci = C[i]
                for k in range(n):
                    aik = Ai[k]
                    if aik:
                        Bk = B[k]
                        # unroll accumulation
                        for j in range(n):
                            Ci[j] = (Ci[j] + aik * Bk[j]) % MOD
            return C

        # Matrix-vector multiplication: A (26x26) * v (26) => vector (26)
        def mat_vec_mul(A, v):
            n = 26
            res = [0] * n
            for i in range(n):
                ssum = 0
                Ai = A[i]
                for j in range(n):
                    if Ai[j]:
                        ssum += Ai[j] * v[j]
                res[i] = ssum % MOD
            return res

        # Fast exponentiation of matrix
        def mat_pow(mat, exp):
            n = 26
            # identity
            res = [[0] * n for _ in range(n)]
            for i in range(n):
                res[i][i] = 1
            base = mat
            while exp > 0:
                if exp & 1:
                    res = mat_mul(res, base)
                base = mat_mul(base, base)
                exp >>= 1
            return res

        # initial counts vector
        init = [0] * 26
        for ch in s:
            init[ord(ch) - 97] += 1

        # if t == 0: length is len(s) (algorithm handles it via identity)
        Mt = mat_pow(M, t)
        final_counts = mat_vec_mul(Mt, init)
        ans = sum(final_counts) % MOD
        return ans
```
- Approach notes: Represented the transformation as a linear 26x26 matrix and used fast exponentiation to compute M^t. Multiplying M^t by the initial frequency vector gives final frequencies; summing them yields the final string length.
- Time complexity: O(26^3 * log t + 26 + len(s)) which is effectively O(log t) with a small constant (26^3 ~ 17576). Space complexity: O(26^2) for matrices and O(26) for vectors.