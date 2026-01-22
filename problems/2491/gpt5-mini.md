# [Problem 2491: Divide Players Into Teams of Equal Skill](https://leetcode.com/problems/divide-players-into-teams-of-equal-skill/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to pair up n players into n/2 teams of 2 such that each pair has the same total skill. If every pair must sum to the same value T, then the total sum S of all skills must equal m * T where m = n/2, so T = S / m (must be integer). Once T is fixed, we need to form pairs that each sum to T. Sorting and using two pointers (smallest with largest) is a natural greedy: if the smallest can't pair with the largest to make T, we can't make all pairs sum to T. The chemistry is sum of products of paired elements. Alternative: frequency/counting approach since skill values are small (<=1000) — can do linear-time pairing with counts. But sorting with two pointers is simple and O(n log n).

## Refining the problem, round 2 thoughts
- First check S % m == 0; if not, return -1.
- Sort skills, then use two pointers l=0, r=n-1: if skills[l] + skills[r] != T -> impossible.
- If they match, accumulate skills[l] * skills[r], move l++ and r-- until all paired.
- Proof sketch for greedy: after sorting, the smallest element must pair with some element to reach T; pairing it with anything smaller than the largest would force the largest to pair with someone >= that other partner which would exceed T, so we can (and must) pair extremes.
- Time complexity: sorting dominates O(n log n), two-pointer pass O(n); space O(1) extra (or O(n) if counting sort built-in).
- Edge cases: n = 2 trivial; large sums handled by Python ints. Also ensure integer division check.

## Attempted solution(s)
```python
class Solution:
    def dividePlayers(self, skill: list[int]) -> int:
        n = len(skill)
        m = n // 2
        total = sum(skill)
        # Each team's total must be integer
        if total % m != 0:
            return -1
        target = total // m

        skill.sort()
        l, r = 0, n - 1
        chemistry_sum = 0
        while l < r:
            if skill[l] + skill[r] != target:
                return -1
            chemistry_sum += skill[l] * skill[r]
            l += 1
            r -= 1
        return chemistry_sum
```
- Approach: sort the array and pair smallest with largest using two pointers, checking that each pair sums to target (total sum divided by m). Accumulate product for chemistry sum.
- Time complexity: O(n log n) due to sorting, plus O(n) for the pairing pass.
- Space complexity: O(1) additional (not counting input) or O(n) if counting the sort's extra memory.
- Notes: Because skill[i] ≤ 1000 and n ≤ 1e5, products and total chemistry fit comfortably in Python integers. An alternative O(n + U) approach (U = max skill range) is to use counting/frequency array (since skill values ≤ 1000) to pair values without sorting.