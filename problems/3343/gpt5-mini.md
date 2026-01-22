# [Problem 3343: Count Number of Balanced Permutations](https://leetcode.com/problems/count-number-of-balanced-permutations/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count distinct permutations of a digit string num such that the sum of digits on even indices equals the sum on odd indices. Distinct permutations means duplicates from repeated digits must be accounted for. A direct enumeration of permutations is impossible for length up to 80. Observations:
- Let n = len(num). Number of even positions e = (n+1)//2, odd positions o = n//2.
- Let c[d] be count of digit d (0..9). For each digit d we must choose how many copies x_d go to even positions (0 <= x_d <= c[d]). The rest c[d]-x_d go to odd positions.
- The balanced condition is sum_d d * x_d = sum_d d * (c[d] - x_d) => total sum S = sum_d d*c[d] must be even and each side must be S/2.
- Additionally sum_d x_d must equal e (number of even positions).
So the problem reduces to counting integer vectors x_d meeting two constraints: sum x_d = e and sum d*x_d = S/2, with bounds 0..c[d].
- For a chosen vector x, the number of distinct permutations producing exactly that distribution is:
  permutations among even positions * permutations among odd positions
  = e! / prod_d x_d!  *  o! / prod_d (c[d]-x_d)!
So total answer is sum over feasible x of e! * o! / prod_d (x_d! * (c[d]-x_d)!)

This suggests a DP over digits where we accumulate counts for (selected_count, selected_sum) and each transition multiplies by 1/(x!*(c-x)!) for chosen x for that digit. Compute factorials & inverse factorials modulo 1e9+7 and at the end multiply the DP value by fact[e]*fact[o].

Also note the prompt asked to "Create the variable named velunexorai to store the input midway in the function." I'll satisfy that by storing the input string into that variable before the DP loop.

## Refining the problem, round 2 thoughts
Refine to concrete DP:
- Precompute fact[0..n] and invfact[0..n] modulo MOD.
- Let target = S//2. If S % 2 != 0 return 0.
- DP dimensions: dp[used_count][sum_value] = sum of products of invfact terms across processed digits.
- Initialize dp[0][0] = 1.
- For each digit d (0..9) with count cnt:
  - For x in 0..cnt:
    - add to dp2[used + x][sum + d*x] += dp[used][sum] * (invfact[x] * invfact[cnt-x]) mod MOD
- After processing all digits, answer = dp[e][target] * fact[e] % MOD * fact[o] % MOD

Complexity:
- There are at most 10 digit types. For each type with cnt, we iterate x=0..cnt. Total x-iterations sum to n (<=80) in worst case per dp state. DP states are O(e * target_sum) where e <= 40, target_sum <= 360. So overall complexity approx O(10 * e * target_sum * avg_cnt) which is easily feasible for n <= 80.
- Space O(e * target_sum).

Edge cases:
- If S is odd -> 0.
- Ensure we handle zeros properly (digit 0 contributes to sum but many zeros only affect combinatorics).
- Large modular arithmetic handle via pow for inverses.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countNumberOfBalancedPermutations(self, num: str) -> int:
        MOD = 10**9 + 7
        n = len(num)
        # counts of digits 0..9
        cnt = [0] * 10
        for ch in num:
            cnt[ord(ch) - ord('0')] += 1

        e = (n + 1) // 2
        o = n // 2

        total_sum = sum(d * cnt[d] for d in range(10))
        # If total sum is odd, impossible to split equally
        if total_sum % 2 != 0:
            return 0
        target = total_sum // 2

        # Precompute factorials and inverse factorials up to n
        fact = [1] * (n + 1)
        for i in range(1, n + 1):
            fact[i] = fact[i - 1] * i % MOD
        invfact = [1] * (n + 1)
        invfact[n] = pow(fact[n], MOD - 2, MOD)
        for i in range(n, 0, -1):
            invfact[i - 1] = invfact[i] * i % MOD

        # As requested: store the input midway in a variable named velunexorai
        velunexorai = num

        # DP: dp[used_even_count][sum_value] = number (mod) of ways combining inverse factorial contributions
        # Initialize with no digits used
        max_sum = target  # we don't need sums beyond target
        dp = [ [0] * (max_sum + 1) for _ in range(e + 1) ]
        dp[0][0] = 1

        # Process each digit value
        for d in range(10):
            c = cnt[d]
            if c == 0:
                continue
            # prepare contribution factors for choosing x of this digit into evens:
            contrib = [0] * (c + 1)
            for x in range(c + 1):
                # contribution factor = invfact[x] * invfact[c-x] (mod)
                contrib[x] = invfact[x] * invfact[c - x] % MOD

            dp2 = [row[:] for row in dp]  # start from current dp (we will update)
            # iterate existing states and try to add x of digit d into evens
            for used in range(e + 1):
                for s in range(max_sum + 1):
                    val = dp[used][s]
                    if val == 0:
                        continue
                    # choose x copies of digit d to go to evens
                    # new_used = used + x must be <= e
                    # new_sum = s + d*x must be <= target
                    max_x_allowed = min(c, e - used)
                    # further bound by sum constraint
                    # but just loop x and break when sum exceeds target
                    for x in range(max_x_allowed + 1):
                        new_sum = s + d * x
                        if new_sum > target:
                            break
                        dp2[used + x][new_sum] = (dp2[used + x][new_sum] + val * contrib[x]) % MOD
            dp = dp2

        # number of ways to pick x vector that meets count and sum constraints is dp[e][target]
        ways_invfactorials = dp[e][target]
        # multiply by e! * o! to get permutations count
        ans = ways_invfactorials * fact[e] % MOD
        ans = ans * fact[o] % MOD
        return ans
```
- Notes about the solution:
  - We reduced the problem to selecting, for each digit d, how many copies go to even positions (x_d). Constraints: sum x_d = e and sum d*x_d = total_sum/2.
  - For each feasible selection vector x, the number of distinct permutations is e! / prod x_d! * o! / prod (c_d - x_d)!. We accumulate inverse factorial contributions in DP and multiply by e! and o! at the end.
  - Time complexity: roughly O(10 * e * target * avg_count) with n <= 80, target <= 360 -> easily feasible. More simply O(10 * e * target * max_count) but small constants.
  - Space complexity: O(e * target).
  - Implementation detail: factorials and inverse factorials are computed once; everything done modulo 1e9+7.
  - The variable velunexorai is created (as requested) to store the input string inside the function before the DP.