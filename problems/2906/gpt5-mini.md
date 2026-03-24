# [Problem 2906: Construct Product Matrix](https://leetcode.com/problems/construct-product-matrix/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need, for each cell p[i][j], the product of all grid elements except grid[i][j], modulo 12345. A naive approach is to compute the product of all elements then divide by grid[i][j] modulo 12345. But modulo 12345 is composite (12345 = 3 * 5 * 823) so modular inverse of grid[i][j] doesn't always exist. Also the true product of all elements (without modulo) would be astronomically large (up to 1e5 numbers of up to 1e9), so we can't compute it directly in full integer form.

Observation: because the modulus M = 12345 factors into small primes (3, 5, 823), we can separate each element into the part composed of these prime factors and the remaining part that is coprime to M. If we record, for each element, the exponent counts for the primes {3,5,823} and the "remainder" after removing these primes, then:
- The product of all remainders is coprime to M, so we can compute its modular inverse per element reliably (after removing that element's remainder).
- The product of primes can be handled by tracking total exponents and subtracting the exponent of the excluded element.

This avoids needing inverses for values that share factors with M and works with modular arithmetic efficiently.

## Refining the problem, round 2 thoughts
Plan:
- Factor M = 12345 into primes [3, 5, 823].
- For each grid value a:
  - For each prime p in [3,5,823], count how many times p divides a (e_p) and divide it out; store e_p for that element.
  - After removing those factors, what's left (rem) is coprime to M; store rem.
- Maintain total exponent sums E_p for each prime across all elements and rem_prod = product of all rem modulo M.
- For an element a_i, the product of all other elements modulo M equals:
  (rem_prod * inv(rem_i) mod M) * product_over_primes p^(E_p - e_p_i) mod M
  where inv(rem_i) is the modular inverse of rem_i modulo M (exists because rem_i is coprime to M).
- Compute extended gcd based modular inverses for rem_i (or cache inverses for repeated rem values to optimize).
- Reconstruct the answer matrix shape-wise.

Complexity:
- Let N = n*m (<= 1e5). For each element we perform division by at most three primes repeatedly — small cost. Also computing modular inverse (extended gcd) and a few modular exponentiations per element. So overall time O(N * log M + N * small_division_cost). Space O(N) to store exponents/remainders (or we could stream and keep them in arrays).

Edge cases:
- Elements equal to 1 (no prime factors) — handled naturally.
- Elements divisible entirely by M (e.g., 12345) — they will have exponents for all primes, rem becomes 1; the formula still works and may produce 0 modulo M for some outputs.
- No zeros in input (given grid values >= 1), so we don't have to handle zero specially.

## Attempted solution(s)
```python
from typing import List, Tuple

class Solution:
    def productExceptSelf(self, grid: List[List[int]]) -> List[List[int]]:
        M = 12345
        primes = [3, 5, 823]

        # Flatten grid to process easily and map back
        n = len(grid)
        m = len(grid[0])
        flat = []
        for row in grid:
            flat.extend(row)
        N = len(flat)

        # Store exponent counts for each prime for each element and the remainder after removing those primes
        exps = [[0,0,0] for _ in range(N)]
        rems = [0] * N

        # Totals
        total_exp = [0,0,0]
        rem_prod = 1

        for i, val in enumerate(flat):
            x = val
            for pi, p in enumerate(primes):
                cnt = 0
                while x % p == 0:
                    x //= p
                    cnt += 1
                exps[i][pi] = cnt
                total_exp[pi] += cnt
            rems[i] = x  # x is now coprime with M (we removed factors 3,5,823)
            rem_prod = (rem_prod * (x % M)) % M

        # extended gcd for modular inverse
        def egcd(a: int, b: int) -> Tuple[int,int,int]:
            if b == 0:
                return a, 1, 0
            g, x1, y1 = egcd(b, a % b)
            # x1, y1 correspond to solution for b and a % b; update to a,b
            x = y1
            y = x1 - (a // b) * y1
            return g, x, y

        def modinv(a: int, mod: int) -> int:
            g, x, _ = egcd(a, mod)
            if g != 1:
                # inverse doesn't exist, but by construction a should be coprime to mod
                raise ValueError("No modular inverse")
            return x % mod

        # Optional: cache inverses for repeated remainders to speed up
        inv_cache = {}

        # Build answer flattened, then reshape
        ans_flat = [0] * N
        for i in range(N):
            rem_i = rems[i] % M
            if rem_i not in inv_cache:
                inv_cache[rem_i] = modinv(rem_i, M)
            inv_rem_i = inv_cache[rem_i]

            # start with rem_prod / rem_i  (mod M)
            base = rem_prod * inv_rem_i % M

            # multiply by prime powers p^(total_exp - exps[i])
            val = base
            for pi, p in enumerate(primes):
                exp_need = total_exp[pi] - exps[i][pi]
                if exp_need > 0:
                    val = (val * pow(p, exp_need, M)) % M
                # if exp_need == 0 nothing to do; pow(...,0) == 1
            ans_flat[i] = val

        # reshape to n x m
        out = []
        idx = 0
        for _ in range(n):
            out.append(ans_flat[idx: idx + m])
            idx += m
        return out
```
- Notes:
  - We factor modulus M = 12345 into primes [3, 5, 823] and remove those factors from each element.
  - rems[i] is coprime to M, so modular inverse exists; we compute inv(rem_i) using extended gcd.
  - We keep total exponents per prime across all elements; for element i we use exponent total_exp - exps[i] to get the product of primes excluding element i.
  - Time complexity: O(N * (small constant factor for dividing out primes + log M for modexp and extended gcd)). For N <= 1e5 this is efficient.
  - Space complexity: O(N) extra for storing exponents and remainders (could be optimized to streaming but it's fine here).