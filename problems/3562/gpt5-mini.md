# [Problem 3562: Maximum Profit from Trading Stocks with Discounts](https://leetcode.com/problems/maximum-profit-from-trading-stocks-with-discounts/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is a tree + knapsack problem. We have a company hierarchy (a rooted tree with node 1 as root), and each node can be bought at one of two possible prices depending on whether its direct boss bought (discounted floor(present/2)) or not (full present). Buying a node also affects only its direct children (they get discount if this node bought). We have a total budget (cost limit) and cannot reuse future profit to buy more, so this is a 0/1 choice per node with a global cost constraint.

That suggests a tree DP where for each node we compute, for each possible cost up to budget, the maximum profit achievable in that subtree. Because whether a node is bought affects only its children (not siblings or ancestors beyond parent), we should maintain DP arrays for two contexts: when the parent did buy (so this node would have discount if bought) and when the parent did not buy.

We must combine children contributions like knapsacks (convolution / merging costs). n and budget are ≤ 160, so O(n * budget^2) DP is acceptable.

## Refining the problem, round 2 thoughts
Plan:
- Build children adjacency from the hierarchy input (it's already a tree, root=1).
- For each node u, compute two arrays:
  - dp0[c]: max profit in subtree u with total cost c when u's parent did NOT buy (so if u buys it pays full price).
  - dp1[c]: max profit in subtree u with total cost c when u's parent DID buy (so if u buys it pays discounted floor(present[u]/2)).
- To compute these, first merge children contributions in two ways:
  - base_no: result of merging child dp0 arrays (children see parent not bought).
  - base_yes: result of merging child dp1 arrays (children see parent bought).
- Then for dp0: we can either not buy u (use base_no unchanged) or buy u paying full price, gaining future-present, while children behave as if parent bought (use base_yes + node's profit with full price shifted by price).
- For dp1: similarly, either not buy u (use base_no), or buy u paying discounted price and children use base_yes.
- Use -inf for impossible entries. Final answer is max dp0[c] for c <= budget at root (root has no parent so parent not bought).
Edge cases: negative profit (future < price) — algorithm will naturally avoid buying those since not buying is considered.

Complexity: merging children with O(budget^2) per edge gives O(n * budget^2) time, space O(budget) per node during recursion (overall O(n * budget) if persistent).

## Attempted solution(s)
```python
from typing import List, Tuple
import sys
sys.setrecursionlimit(10000)

def maximumProfit(n: int, present: List[int], future: List[int], hierarchy: List[List[int]], budget: int) -> int:
    # build children adjacency
    children = [[] for _ in range(n + 1)]
    for u, v in hierarchy:
        children[u].append(v)

    B = budget
    NEG_INF = -10**9

    def dfs(u: int) -> Tuple[List[int], List[int]]:
        # base_no: children merged when this node is NOT bought (children see parent not bought => use child's dp0)
        # base_yes: children merged when this node IS bought (children see parent bought => use child's dp1)
        base_no = [NEG_INF] * (B + 1)
        base_no[0] = 0
        base_yes = [NEG_INF] * (B + 1)
        base_yes[0] = 0

        for v in children[u]:
            child_dp0, child_dp1 = dfs(v)

            # merge for base_no with child_dp0
            new_no = [NEG_INF] * (B + 1)
            for c1 in range(B + 1):
                if base_no[c1] == NEG_INF:
                    continue
                # c2 cost from child
                # iterate up to remaining budget
                rem = B - c1
                # typical small loops: iterate c2 and check child's value
                for c2 in range(rem + 1):
                    val = child_dp0[c2]
                    if val == NEG_INF:
                        continue
                    nc = c1 + c2
                    cur = base_no[c1] + val
                    if cur > new_no[nc]:
                        new_no[nc] = cur
            base_no = new_no

            # merge for base_yes with child_dp1
            new_yes = [NEG_INF] * (B + 1)
            for c1 in range(B + 1):
                if base_yes[c1] == NEG_INF:
                    continue
                rem = B - c1
                for c2 in range(rem + 1):
                    val = child_dp1[c2]
                    if val == NEG_INF:
                        continue
                    nc = c1 + c2
                    cur = base_yes[c1] + val
                    if cur > new_yes[nc]:
                        new_yes[nc] = cur
            base_yes = new_yes

        # Now build dp0 and dp1 for node u
        dp0 = [NEG_INF] * (B + 1)  # parent not bought
        dp1 = [NEG_INF] * (B + 1)  # parent bought

        # option: node NOT bought -> children merged under base_no, same for dp0 and dp1
        for c in range(B + 1):
            if base_no[c] != NEG_INF:
                if base_no[c] > dp0[c]:
                    dp0[c] = base_no[c]
                if base_no[c] > dp1[c]:
                    dp1[c] = base_no[c]

        price_full = present[u - 1]
        price_disc = present[u - 1] // 2
        profit_full = future[u - 1] - price_full
        profit_disc = future[u - 1] - price_disc

        # option: node IS bought -> children merged under base_yes, then add node cost & profit
        for c in range(B + 1):
            if base_yes[c] == NEG_INF:
                continue
            # buy when parent not bought: cost add price_full, profit add profit_full => affects dp0
            nc = c + price_full
            if nc <= B:
                val = base_yes[c] + profit_full
                if val > dp0[nc]:
                    dp0[nc] = val
            # buy when parent bought: cost add price_disc, profit add profit_disc => affects dp1
            nc2 = c + price_disc
            if nc2 <= B:
                val2 = base_yes[c] + profit_disc
                if val2 > dp1[nc2]:
                    dp1[nc2] = val2

        return dp0, dp1

    root_dp0, _ = dfs(1)
    # answer is max profit achievable with cost <= budget when root's parent is considered not bought
    ans = max(root_dp0)
    return max(ans, 0)  # profit can't be negative, but return 0 if all negative

# The LeetCode function signature would be similar to:
# class Solution:
#     def maxProfit(self, n: int, present: List[int], future: List[int],
#                   hierarchy: List[List[int]], budget: int) -> int:
#         return maximumProfit(n, present, future, hierarchy, budget)
```

- Notes about the solution:
  - We perform a DFS on the rooted tree and maintain two knapsack DP arrays per node: dp0 (parent not bought) and dp1 (parent bought).
  - For each node we first merge children contributions under two contexts (child sees parent not bought vs parent bought). Merging is a standard knapsack convolution (double loop up to budget).
  - After merging children, we consider not buying the node (just keep merged children) or buying it (pay price, add profit, and children should have been merged under the "node bought" context).
  - Complexity: Time O(n * budget^2) in the worst case because for each edge we do a merging that is O(budget^2). With n, budget ≤ 160 this is fine (~ a few million operations). Space O(budget) per recursion level (total stack depth <= n).
  - Implementation detail: we use NEG_INF to represent unreachable cost states; initial base lists have base[0] = 0. The final answer is the maximum dp0[c] for c ≤ budget at the root (root has no parent, so parent's bought flag is False). We clamp to at least 0 if desired (problem expects nonnegative profit maximum).