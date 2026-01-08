# [Problem 1458: Max Dot Product of Two Subsequences](https://leetcode.com/problems/max-dot-product-of-two-subsequences/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the maximum dot product between two non-empty subsequences of equal length. Sounds like a dynamic programming problem over prefixes of both arrays. A naive combinatorial approach (try all subsequence pairs) is exponential. We want an optimal substructure: consider prefixes of nums1 and nums2 and decide whether to match the current elements or skip one of them.

The dot product accumulates pairwise multiplications in order. For indices i and j (pointing to last elements of chosen subsequences), either we use nums1[i] with nums2[j] (and add their product to the best result for previous prefixes) or we skip one side (move left in one array). Need to ensure subsequences are non-empty: we must allow starting the pairing at some point (choose a single pair as baseline). Negative values complicate things: the best may be a single negative*positive giving a negative, or multiple pairs combining to a positive sum.

So dp on prefixes seems right. Need to carefully initialize to allow starting new pair (single product) and not force choosing pairs.

## Refining the problem, round 2 thoughts
Define dp[i][j] = maximum dot product you can get using some non-empty subsequences taken from nums1[:i] and nums2[:j] (i and j are lengths, 1-based). For each (i,j):

- We can skip nums1[i-1]: dp[i-1][j]
- We can skip nums2[j-1]: dp[i][j-1]
- We can take the pair nums1[i-1]*nums2[j-1] and add it to dp[i-1][j-1] (if dp[i-1][j-1] exists)
- Or we can start a new subsequence pair with just this product (choose the single pair), because dp[i-1][j-1] might be undefined or very negative; so include product itself explicitly.

Thus:
dp[i][j] = max(dp[i-1][j], dp[i][j-1], dp[i-1][j-1] + prod, prod)

Initialize dp with negative infinity for zero prefixes so that skipping until a first match is allowed and single product is always an option. Finally dp[n][m] is the answer.

Complexity: O(n*m) time, O(n*m) space (or O(m) space if rolling rows used). n,m <= 500 so both fine.

Edge cases:
- All numbers negative or mixed signs — including the single product option ensures we can return the best single-pair negative if needed.
- Must ensure subsequences are non-empty; dp definition and initialization ensure we only return values derived from at least one pair.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxDotProduct(self, nums1: List[int], nums2: List[int]) -> int:
        n, m = len(nums1), len(nums2)
        NEG_INF = -10**18  # sufficiently small sentinel

        # dp[i][j]: max dot product using non-empty subsequences from nums1[:i] and nums2[:j]
        dp = [[NEG_INF] * (m + 1) for _ in range(n + 1)]

        for i in range(1, n + 1):
            for j in range(1, m + 1):
                prod = nums1[i-1] * nums2[j-1]
                # Option 1,2: skip an element from one side
                skip1 = dp[i-1][j]
                skip2 = dp[i][j-1]
                # Option 3: extend a previous pairing
                extend = dp[i-1][j-1] + prod if dp[i-1][j-1] != NEG_INF else NEG_INF
                # Option 4: start a new subsequence with this single pair
                start_new = prod

                dp[i][j] = max(skip1, skip2, extend, start_new)

        return dp[n][m]
```
- Notes about the solution:
  - Approach: 2D dynamic programming over prefixes. For each pair of prefix endpoints, consider skipping elements or pairing the endpoints (either as extension of a prior pairing or as a new single-pair subsequence).
  - Correctness: dp always represents the best non-empty subsequence dot product from those prefixes. Including the product itself handles starting subsequences and guarantees non-empty result. Skipping options allow choosing the best placement.
  - Time complexity: O(n * m), where n = len(nums1) and m = len(nums2).
  - Space complexity: O(n * m) for the dp table. This can be reduced to O(m) by keeping only previous and current rows because dp[i][j] depends only on dp[i-1][*] and dp[i][j-1]/dp[i-1][j-1].
  - Implementation detail: Use a very small sentinel (NEG_INF) to represent impossible/unused states for empty prefixes. This prevents invalid accumulation when extending.