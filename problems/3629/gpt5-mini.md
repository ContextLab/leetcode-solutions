# [Problem 3629: Minimum Jumps to Reach End via Prime Teleportation](https://leetcode.com/problems/minimum-jumps-to-reach-end-via-prime-teleportation/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the minimum number of jumps from index 0 to n-1. Moves are adjacent steps or a teleport when the current number is a prime p to any index whose value is divisible by p. This suggests BFS on indices because each move has equal cost (1). The tricky part is efficiently handling teleports: when at a prime p, we should quickly find all indices j where nums[j] % p == 0.

Brute forcing divisibility checks for every teleport would be too slow (n per teleport in worst case). Instead, precompute for each prime p which indices have values divisible by p. To build that mapping, factor each nums[j] into distinct prime factors and add j to each prime's list. Then when a BFS node has a prime value p, we iterate the precomputed list map[p] and enqueue those indices (and clear map[p] afterwards to avoid reprocessing). We'll also use a sieve (smallest prime factor array) for fast factorization and prime checks.

Edge cases: n == 1 -> 0 jumps. nums values = 1 (not prime). Avoid teleporting to the same index (skip j == i) and ensure we don't reprocess a prime's list multiple times.

## Refining the problem, round 2 thoughts
- Build SPF (smallest prime factor) up to max(nums) with a standard sieve (max value up to 1e6 -> fine).
- For each index j, factor nums[j] into distinct primes using SPF; append j to mapping for each prime factor.
- BFS from index 0 with a visited array and distance. For each node i:
  - try i-1 and i+1,
  - if nums[i] is prime p (check using SPF), iterate mapping[p] and visit every index there, then clear mapping[p] to O(1) future cost.
- Complexity: sieve O(M) where M = max(nums) (<=1e6). Factorizing all numbers is sum of O(number of prime factors) per number, negligible overall. BFS visits each index at most once and processes each mapping list at most once (we clear after use). Overall near O(M + n * small_factor_count).
- Memory: SPF array size M + mapping with total entries ~ sum of distinct prime factors across nums (<= n * small constant).
- Implementation detail: when we process mapping[p], skip the current index i if present and ensure we mark indices visited when enqueuing them.

## Attempted solution(s)
```python
from collections import defaultdict, deque
import sys

class Solution:
    def minJumps(self, nums):
        n = len(nums)
        if n <= 1:
            return 0

        maxv = max(nums)

        # Build smallest prime factor (spf) array up to maxv
        spf = list(range(maxv + 1))
        spf[0] = 0
        if maxv >= 1:
            spf[1] = 1
        p = 2
        while p * p <= maxv:
            if spf[p] == p:
                step = p
                start = p * p
                for x in range(start, maxv + 1, step):
                    if spf[x] == x:
                        spf[x] = p
            p += 1

        def factor_primes(x):
            """Return distinct prime factors of x using spf"""
            res = set()
            while x > 1:
                f = spf[x]
                res.add(f)
                while x % f == 0:
                    x //= f
            return res

        # Build mapping: prime p -> list of indices j where nums[j] % p == 0
        div_map = defaultdict(list)
        for idx, val in enumerate(nums):
            # factor val into distinct prime factors and add idx to each
            if val > 1:
                for prime in factor_primes(val):
                    div_map[prime].append(idx)
            # val == 1 has no prime factors, no entries

        # BFS
        q = deque([0])
        visited = [False] * n
        visited[0] = True
        dist = 0

        while q:
            for _ in range(len(q)):
                i = q.popleft()
                if i == n - 1:
                    return dist

                # adjacent steps
                for ni in (i - 1, i + 1):
                    if 0 <= ni < n and not visited[ni]:
                        visited[ni] = True
                        q.append(ni)

                # prime teleportation: only if nums[i] is prime
                val = nums[i]
                if val > 1 and spf[val] == val:  # val is prime
                    p = val
                    # visit all indices divisible by this prime p
                    lst = div_map.get(p, [])
                    for j in lst:
                        if not visited[j]:
                            visited[j] = True
                            q.append(j)
                    # clear to avoid reprocessing this prime later
                    if p in div_map:
                        del div_map[p]
            dist += 1

        # If unreachable (shouldn't happen since adjacent steps always connect),
        # but return -1 defensively
        return -1

# For quick local testing:
if __name__ == "__main__":
    sol = Solution()
    print(sol.minJumps([1,2,4,6]))  # expected 2
    print(sol.minJumps([2,3,4,7,9]))  # expected 2
    print(sol.minJumps([4,6,5,8]))  # expected 3
```

- Notes about the solution:
  - We precompute smallest prime factors (spf) to both test primality quickly (spf[x] == x means x is prime for x > 1) and to factorize numbers into prime divisors efficiently.
  - The div_map maps a prime p to all indices j such that p divides nums[j]. We only need these lists for primes that actually appear as nums[i] (possible teleport sources), but building for all prime factors of all numbers is straightforward and efficient.
  - In BFS, once we use a prime p for teleportation, we delete its mapping (del div_map[p]) to avoid processing the same list repeatedly; that guarantees each mapping list is iterated at most once.
  - Time complexity:
    - Sieve SPF: O(M) where M = max(nums) (<= 1e6).
    - Factorization of all nums: sum of O(number of distinct prime factors per number) ~ O(n * small_constant).
    - BFS: each index visited once, and each div_map list processed at most once. Overall near O(M + n * log V) but practically O(M + n).
  - Space complexity:
    - SPF array O(M), div_map total entries O(sum distinct prime factors) which is O(n * small_constant), visited/dist arrays O(n).