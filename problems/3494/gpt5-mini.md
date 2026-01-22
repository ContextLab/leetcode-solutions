# [Problem 3494: Find the Minimum Amount of Time to Brew Potions](https://leetcode.com/problems/find-the-minimum-amount-of-time-to-brew-potions/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem describes n wizards (machines) and m potions (jobs) that must visit the wizards in the same order. Processing time of wizard i on potion j is skill[i] * mana[j]. A crucial sentence: "a potion must be passed to the next wizard immediately after the current wizard completes their work." That is the no-wait flow shop model: once a potion starts on wizard 0, it must flow through all wizards without any waiting between machines.

With a fixed job order (the mana array order is fixed), the no-wait flow-shop start time of each job on machine 0 is constrained by machine capacity: for each machine i the start times of consecutive jobs must respect that machine can't process two jobs at once. There is a standard way to compute start times greedily: s_0 = 0 and each subsequent job's start is s_j = s_{j-1} + max_{machines i} (delay_{i,j}) where delay_{i,j} expresses how much later job j must start so it won't collide with job j-1 on machine i. Because p_{i,j} = skill[i]*mana[j] is separable, these delays simplify to expressions that use prefix sums of skill, which suggests an O(n*m) solution by computing prefix sums and evaluating the max delay per pair of adjacent potions.

## Refining the problem, round 2 thoughts
Let prefix[i] = sum_{k=0..i} skill[k]. For machine i (0-based), the completion time of job j-1 on machines up to i is prefix[i] * mana[j-1], and the start of job j on machine i would be s_j + prefix[i-1] * mana[j] (prefix[-1] = 0). To avoid overlap on machine i we need:
s_j + prefix[i-1]*mana[j] >= s_{j-1} + prefix[i]*mana[j-1].
Rearrange:
s_j >= s_{j-1} + (prefix[i]*mana[j-1] - prefix[i-1]*mana[j]).
Thus s_j must be at least s_{j-1} + max_i delta_i where delta_i = prefix[i]*mana[j-1] - prefix[i-1]*mana[j]. For i=0 the formula reduces to skill[0]*mana[j-1] (with prefix[-1]=0) so max delta is always >= 0 and start times are nondecreasing.

We can compute prefix once (O(n)), then for each adjacent pair of potions (m-1 pairs) compute the maximal delta by iterating over i from 0..n-1 (O(n)). That gives overall O(n*m) time and O(1) extra space (besides input/prefix). Constraints n,m <= 5000 give up to 25e6 simple arithmetic ops which is acceptable in Python if implemented straightforwardly.

Edge cases:
- m == 1: only one potion, answer is sum(skill) * mana[0].
- n == 1: single wizard, potions are processed sequentially so answer is sum_j (skill[0] * mana[j])? Wait careful: no-wait constraint with single wizard just means wizard processes potions one after another; start times are cumulative sum, final completion is skill[0] * sum(mana). But our general formula covers these.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minAmountOfTime(self, skill: List[int], mana: List[int]) -> int:
        n = len(skill)
        m = len(mana)
        # prefix[i] = sum(skill[0..i])
        prefix = [0] * n
        s = 0
        acc = 0
        for i in range(n):
            acc += skill[i]
            prefix[i] = acc

        # start time for potion 0
        start_prev = 0
        # compute start times for potion j (only need previous)
        for j in range(1, m):
            prev_mana = mana[j-1]
            cur_mana = mana[j]
            # compute max delta over all machines i
            # delta_i = prefix[i]*prev_mana - prefix[i-1]*cur_mana
            # for i=0 prefix[-1]=0 gives delta = skill[0]*prev_mana
            max_delta = -10**30
            # i = 0 separately if desired, but loop handles it with prefix_minus = 0
            prefix_minus = 0
            for i in range(n):
                # prefix[i] is sum up to i, prefix_minus is sum up to i-1
                delta = prefix[i] * prev_mana - prefix_minus * cur_mana
                if delta > max_delta:
                    max_delta = delta
                prefix_minus = prefix[i]
            # start time for current potion
            start_curr = start_prev + max_delta
            start_prev = start_curr

        # final completion = start of last potion + total processing of last potion (sum skill * mana[-1])
        total_skill = prefix[-1]
        return start_prev + total_skill * mana[-1]
```
- Notes on approach:
  - Model is no-wait flow-shop with fixed job order. We compute contiguous start times s_j for each potion j.
  - Using prefix sums of skills makes the machine-wise delay delta expression separable and fast to compute.
  - Time complexity: O(n * m) where n = len(skill), m = len(mana). Space complexity: O(n) for prefix (plus O(1) extra).
  - All arithmetic stays in integers; Python builtin int can handle the result size.