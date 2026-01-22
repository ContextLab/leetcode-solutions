# [Problem 862: Shortest Subarray with Sum at Least K](https://leetcode.com/problems/shortest-subarray-with-sum-at-least-k/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the shortest contiguous subarray whose sum >= k. If all numbers were non-negative, a sliding window two-pointer approach would work to shrink the window when sum >= k. But nums can contain negative values, so the running sum is not monotonic and the standard two-pointer sliding window won't work.

A common pattern for these problems is to use prefix sums. Let P[i] be the sum of nums[0:i] (P[0] = 0). The sum of subarray nums[i:j] is P[j] - P[i]. We want min length j-i such that P[j] - P[i] >= k. That suggests for each j we want to find the smallest i < j with P[i] <= P[j] - k. We need to do this efficiently.

We can maintain candidate indices i in a deque ordered by increasing prefix sum P[i]. For a new j, we can pop from the front any indices i with P[j] - P[i] >= k (these give valid subarray and earlier ones are longer so popping yields shortest), and we also pop from the back while P[j] <= P[last index] because the current j is a better candidate (smaller prefix sum for later j's).

This is the classic monotonic deque approach for this problem.

## Refining the problem, round 2 thoughts
- Ensure prefix sum array length is n+1.
- Iterate j from 0..n inclusive (prefix indices). For each j:
  - While deque not empty and P[j] - P[deque[0]] >= k: update answer with j - deque.popleft()
  - While deque not empty and P[j] <= P[deque[-1]]: deque.pop()
  - Append j to deque.
- Edge cases: if result remains infinity => return -1.
- Complexity: each index is pushed/popped at most once -> O(n) time, O(n) space for prefix sums and deque.
- Be careful with large sums: prefix sums can be up to n * 1e5 ~ 1e10 so use Python int (unbounded).
- This handles negative values because the deque enforces monotonicity on prefix sums, ensuring correctness.

## Attempted solution(s)
```python
from collections import deque
from typing import List

class Solution:
    def shortestSubarray(self, nums: List[int], k: int) -> int:
        n = len(nums)
        # Prefix sums P where P[0] = 0, P[i] = sum(nums[:i])
        P = [0] * (n + 1)
        for i in range(n):
            P[i+1] = P[i] + nums[i]
        
        ans = n + 1  # sentinel larger than any possible subarray length
        dq = deque()  # will store indices of P in increasing order of P values
        
        for j in range(n + 1):
            # If current prefix minus smallest prefix in deque meets k, update answer
            while dq and P[j] - P[dq[0]] >= k:
                ans = min(ans, j - dq.popleft())
            # Maintain deque monotonic increasing by P value
            while dq and P[j] <= P[dq[-1]]:
                dq.pop()
            dq.append(j)
        
        return ans if ans <= n else -1
```
- Notes about the solution:
  - Approach: prefix sums + monotonic deque storing candidate start indices sorted by increasing prefix sum value.
  - Correctness: For each prefix index j, deque front holds the smallest prefix sums among candidates; if P[j] - P[dq[0]] >= k then that deque[0] gives the shortest subarray ending at j among candidates. Removing dominated indices from back (where P[j] <= P[last]) ensures we never keep an index that is worse for future j's.
  - Time complexity: O(n). Each index is appended/popped at most once from the deque.
  - Space complexity: O(n) for prefix sums and the deque.
  - Implementation detail: use n+1 for P length and iterate j from 0 to n inclusive. Return -1 if no valid subarray.