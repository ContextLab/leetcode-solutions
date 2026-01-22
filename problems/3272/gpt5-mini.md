# [Problem 3272: Find the Count of Good Integers](https://leetcode.com/problems/find-the-count-of-good-integers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the count of n-digit integers whose digits can be rearranged to form a palindrome divisible by k (a k-palindromic integer). A key observation: "can be rearranged to form a palindrome" depends only on the multiset of digit counts (c0..c9). For a multiset, there may be zero, one or many palindromes that can be built from it; the multiset is "good" if any palindrome built from it is (1) an n-digit number (no leading zero) and (2) divisible by k.

So we can iterate over every digit-count multiset (counts sum to n). For each multiset:
- Check whether it can form any palindrome at all (parity constraints: at most one digit with odd count for odd n, none for even n).
- Generate the palindromes (or rather, enumerate possible first-halves of palindromes) consistent with the multiset and test divisibility by k, making sure the palindrome doesn't start with 0.
If any valid palindrome for the multiset is divisible by k, the multiset is good; then we add the number of n-digit permutations (distinct integers) that realize this multiset and do not have leading zero.

Because n ≤ 10, enumerating all multisets is feasible: number of multisets C(n+9,9) ≤ C(19,9)=92378. The half-length of a palindrome is ≤5, so enumerating half-permutations is small (≤120 permutations in worst case). This yields an algorithm that is comfortably fast.

## Refining the problem, round 2 thoughts
Important details / edge cases:
- A palindrome used to test divisibility must not have leading zero. For palindromes, the first digit equals the first digit of the half; therefore when enumerating half permutations we must ensure the first chosen digit is not 0. For n=1 (half length 0) the center digit is the leading digit and must be nonzero.
- When counting how many n-digit integers correspond to a "good" multiset, we must count ALL distinct permutations of digits that are n-digit (i.e., leading digit ≠ 0). So count = total permutations (n! / prod(c[i]!)) minus permutations with leading zero ((n-1)! / ((c0-1)! * prod_{i>0} c[i]!)) when c0>0.
- Divisibility checks can be done modulo k; build weights for each half position: for a digit placed at half position pos (0-based from left in half), its contribution modulo k to the full palindrome equals (10^{n-1-pos} + 10^{pos}) * digit (and if n odd, a center digit contributes 10^{mid} * digit). Precompute powers of 10 modulo k.
- For odd n the center digit is forced (the unique digit with odd count), simplifying the check.

Algorithm complexity:
- Enumerate all multisets: O(C(n+9,9))
- For each, check half-permutations: worst-case factorial of half length but half_len ≤ 5 => small constant.
Overall manageable.

## Attempted solution(s)
```python
# Python 3 solution

from typing import List
import sys
sys.setrecursionlimit(10000)

class Solution:
    def countGoodNumbers(self, n: int, k: int) -> int:
        # Precompute factorials up to n
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i-1] * i

        # Precompute powers of 10 modulo k
        pow10 = [1] * (n + 1)
        for i in range(1, n + 1):
            pow10[i] = (pow10[i-1] * 10) % k if k != 0 else 0  # k >=1 by constraints

        half_len = n // 2
        mid_pos = n // 2  # center position if n is odd: index mid_pos

        # Precompute weight for half positions: contribution modulo k of placing digit d at half position pos
        # weight_pos[d] = (10^(n-1-pos) + 10^pos) % k * d
        weight = [[0]*10 for _ in range(half_len)]
        for pos in range(half_len):
            w = (pow10[n-1-pos] + pow10[pos]) % k
            for d in range(10):
                weight[pos][d] = (w * d) % k

        # center contribution (if n odd): pow10[mid_pos] * d % k
        center_weight_digit = [0]*10
        if n % 2 == 1:
            wcenter = pow10[mid_pos] % k
            for d in range(10):
                center_weight_digit[d] = (wcenter * d) % k

        ans = 0

        # Helper: compute permutations count for a multiset counts[]
        def permutations_count(counts: List[int]) -> int:
            denom = 1
            for c in counts:
                denom *= fact[c]
            return fact[n] // denom

        def leading_zero_permutations(counts: List[int]) -> int:
            c0 = counts[0]
            if c0 == 0:
                return 0
            denom = fact[c0 - 1]
            for i in range(1, 10):
                denom *= fact[counts[i]]
            return fact[n-1] // denom

        # For enumerating multisets (counts of digits 0..9 summing to n)
        counts = [0]*10

        # For checking whether a multiset is "good": whether it produces any valid palindrome
        def is_multiset_good(counts: List[int]) -> bool:
            # parity constraint
            odd_digits = [i for i in range(10) if counts[i] % 2 == 1]
            if n % 2 == 0:
                if odd_digits:
                    return False
            else:
                if len(odd_digits) != 1:
                    return False

            # build half_counts
            half_counts = [counts[i] // 2 for i in range(10)]
            # handle n == 1 special / half_len == 0
            if half_len == 0:
                # center digit is the unique odd digit
                center_digit = odd_digits[0]
                # palindrome must be n-digit => leading digit = center digit != 0
                if center_digit == 0:
                    return False
                # check divisibility
                return (center_digit % k) == 0

            # DFS generate half permutations with given half_counts
            # ensure first digit of half is not zero (no leading zero for palindrome)
            cur_mod = 0
            remaining = half_len

            def dfs_half(pos: int) -> bool:
                if pos == half_len:
                    total_mod = cur_mod % k
                    if n % 2 == 1:
                        # add center contribution
                        center_digit = odd_digits[0]
                        total_mod = (total_mod + center_weight_digit[center_digit]) % k
                    return total_mod == 0

                # choose a digit for this position
                for d in range(10):
                    if half_counts[d] == 0:
                        continue
                    # leading digit of full palindrome is half[0]; ensure it's not zero
                    if pos == 0 and d == 0:
                        continue
                    # choose
                    half_counts[d] -= 1
                    nonlocal_saved = cur_mod  # we'll restore cur_mod after recursion
                    # update cur_mod (we mutate outer cur_mod; so manage with closure by using nonlocal)
                    # but python closure restrictions — instead we'll make cur_mod mutable via list.
                    # To avoid complexity, refactor cur_mod into list outside. (See below.)
                    raise RuntimeError("Implementation detail: should not reach here")
                return False

            # To use mutable cur_mod inside nested function, reimplement with list
            cur_mod_list = [0]

            def dfs_half2(pos: int) -> bool:
                if pos == half_len:
                    total_mod = cur_mod_list[0] % k
                    if n % 2 == 1:
                        center_digit = odd_digits[0]
                        total_mod = (total_mod + center_weight_digit[center_digit]) % k
                    return total_mod == 0
                for d in range(10):
                    if half_counts[d] == 0:
                        continue
                    if pos == 0 and d == 0:
                        continue
                    half_counts[d] -= 1
                    cur_mod_list[0] = (cur_mod_list[0] + weight[pos][d]) % k
                    if dfs_half2(pos + 1):
                        # restore and return True
                        cur_mod_list[0] = (cur_mod_list[0] - weight[pos][d]) % k
                        half_counts[d] += 1
                        return True
                    # restore
                    cur_mod_list[0] = (cur_mod_list[0] - weight[pos][d]) % k
                    half_counts[d] += 1
                return False

            return dfs_half2(0)

        # Enumerate count vectors via recursion
        def gen_counts(digit: int, remaining: int):
            nonlocal ans
            if digit == 9:
                counts[9] = remaining
                # process this counts vector
                if is_multiset_good(counts):
                    total = permutations_count(counts)
                    bad = leading_zero_permutations(counts)
                    ans += (total - bad)
                counts[9] = 0
                return
            # try all possibilities for counts[digit]
            for c in range(remaining + 1):
                counts[digit] = c
                gen_counts(digit + 1, remaining - c)
            counts[digit] = 0

        gen_counts(0, n)
        return ans

# To match LeetCode style naming:
def countGoodIntegers(n: int, k: int) -> int:
    sol = Solution()
    return sol.countGoodNumbers(n, k)

# Example tests (uncomment to run locally)
# print(countGoodIntegers(3, 5))  # Expected 27
# print(countGoodIntegers(1, 4))  # Expected 2
# print(countGoodIntegers(5, 6))  # Expected 2468
```

- Notes on the approach:
  - We enumerate all digit-count multisets (counts sum to n). For each:
    - Verify palindromic feasibility (parity constraint).
    - Compute half-counts and enumerate all unique permutations of the half (ensuring half's first digit ≠ 0 so the palindrome has no leading zero). Use precomputed modular weights to evaluate palindrome mod k efficiently; add center contribution when n is odd.
    - If any palindrome built from the multiset is divisible by k, count all distinct n-digit permutations from that multiset (total permutations minus those with leading zero).
  - Complexity:
    - Number of multisets = C(n+9,9) (<= 92378). For each, exploring half permutations (worst-case <= 5! = 120). So worst-case checks ~ millions but acceptable for n ≤ 10.
    - Memory: O(1) extra beyond recursion stack and small tables.
  - Implementation details:
    - Uses integer factorials to count permutations exactly.
    - Uses modulo arithmetic (k ≤ 9) to test divisibility without constructing big integers.
    - Carefully enforces "no leading zero" both for the palindrome check and for counting valid n-digit integers.