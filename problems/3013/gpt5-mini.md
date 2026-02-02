# [Problem 3013: Divide an Array Into Subarrays With Minimum Cost II](https://leetcode.com/problems/divide-an-array-into-subarrays-with-minimum-cost-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share raw stream-of-consciousness internal chain-of-thought, but here is a concise summary of the key observation and approach:
- The cost equals nums[0] plus the sum of the starts of the remaining k-1 subarrays.
- The indices of those k-1 starts must all lie in a contiguous index interval whose length is at most dist (because max(start) - min(start) <= dist). So they must be chosen inside some window of indices of size at most dist+1.
- Therefore the problem reduces to: find a window of indices among positions 1..n-1 such that the sum of the smallest (k-1) numbers inside that window is minimized. The answer is nums[0] plus that minimum sum.

This leads to a sliding-window + data-structure solution that maintains the sum of the smallest (k-1) elements in the current window as the window slides.

## Refining the problem, round 2 thoughts
I can’t provide additional internal chain-of-thought, but here is a concise refinement of the plan and edge considerations:
- We will iterate all windows [L, R] with L in [1..n-1] and R = min(n-1, L + dist). Each window length is at most dist+1.
- For each window where window_size >= (k-1), we compute the sum of the smallest (k-1) numbers in that window and track the minimum across windows.
- To maintain the sum of the smallest (k-1) elements while adding/removing single elements as L and R move by 1, use two heaps:
  - small (max-heap, implemented as negatives) contains the current smallest t elements (t = min(k-1, current_window_size)).
  - large (min-heap) contains the rest.
  - Maintain small_sum (sum of elements in small), and lazy deletion dicts to support removals when elements slide out.
- Complexity: O(n log n) time (each element added/removed at most once, each heap op log n), O(n) extra space.

## Attempted solution(s)
```python
from collections import defaultdict
import heapq

class SmallestKSliding:
    """
    Maintain multiset of current window values and be able to
    report sum of smallest `target_k` elements (or sum of all if window smaller).
    Uses two heaps + lazy deletions:
      - small: max-heap (store negatives) containing the smallest elements
      - large: min-heap containing the rest
    """
    def __init__(self):
        self.small = []  # max-heap via negatives
        self.large = []  # min-heap
        self.del_small = defaultdict(int)
        self.del_large = defaultdict(int)
        self.small_size = 0
        self.large_size = 0
        self.small_sum = 0

    def _prune_small(self):
        # remove top elements from small that are marked deleted
        while self.small and self.del_small[-self.small[0]] > 0:
            val = -heapq.heappop(self.small)
            self.del_small[val] -= 1

    def _prune_large(self):
        while self.large and self.del_large[self.large[0]] > 0:
            val = heapq.heappop(self.large)
            self.del_large[val] -= 1

    def add(self, x):
        # insert x into appropriate heap
        if self.small and x > -self.small[0]:
            heapq.heappush(self.large, x)
            self.large_size += 1
        else:
            heapq.heappush(self.small, -x)
            self.small_size += 1
            self.small_sum += x

    def remove(self, x):
        # lazily remove x from relevant heap (compare to current boundary)
        # ensure top of small is pruned so comparison is correct
        self._prune_small()
        if self.small and x <= -self.small[0]:
            # belongs to small
            self.small_size -= 1
            self.small_sum -= x
            self.del_small[x] += 1
            # physically pop if it's at top
            if self.small and -self.small[0] == x:
                self._prune_small()
        else:
            # belongs to large
            self.large_size -= 1
            self.del_large[x] += 1
            if self.large and self.large[0] == x:
                self._prune_large()

    def rebalance(self, target_small_size):
        # Ensure small_size == target_small_size (or as large as possible if not enough elements)
        # First, clean tops
        self._prune_small()
        self._prune_large()

        # Move from small -> large if small too big
        while self.small_size > target_small_size:
            self._prune_small()
            if not self.small:
                break
            val = -heapq.heappop(self.small)
            self.small_size -= 1
            self.small_sum -= val
            heapq.heappush(self.large, val)
            self.large_size += 1
            self._prune_small()
            self._prune_large()

        # Move from large -> small if small too small
        while self.small_size < target_small_size and self.large_size > 0:
            self._prune_large()
            if not self.large:
                break
            val = heapq.heappop(self.large)
            self.large_size -= 1
            heapq.heappush(self.small, -val)
            self.small_size += 1
            self.small_sum += val
            self._prune_large()
            self._prune_small()

    def sum_small(self):
        # top pruning to keep structure consistent
        self._prune_small()
        return self.small_sum


class Solution:
    def divideArray(self, nums, k, dist):
        n = len(nums)
        # number of starts to choose besides nums[0]
        m = k - 1
        # if m == 0 would return nums[0], but k >= 3 per constraints
        if n == 0:
            return 0

        sk = SmallestKSliding()
        ans = float('inf')

        # sliding window over indices [L .. R] within 1..n-1
        R = 0  # current right index included in structure; 0 means none initially for indices >=1
        # We'll iterate L from 1 to n-1 inclusive
        for L in range(1, n):
            # extend R to min(n-1, L + dist)
            newR = min(n - 1, L + dist)
            while R < newR:
                R += 1
                sk.add(nums[R])

            window_size = R - L + 1
            if window_size >= m:
                # Ensure small contains exactly m smallest elements
                sk.rebalance(m)
                cur_sum_small = sk.sum_small()
                ans = min(ans, nums[0] + cur_sum_small)
            else:
                # maintain structure but small should be window size
                if window_size > 0:
                    sk.rebalance(window_size)

            # before incrementing L in next iteration, remove nums[L]
            # (if L == R+1, the window is empty next iteration; remove handles gracefully)
            if window_size > 0:
                sk.remove(nums[L])

        return ans if ans != float('inf') else -1  # problem guarantees feasible input

# Example usage to match LeetCode signature
def divideArray(nums, k, dist):
    return Solution().divideArray(nums, k, dist)

# If used on LeetCode, class Solution would expose divideArray as specified.
```

- Notes about approach:
  - Key reduction: the chosen k-1 start indices (excluding index 0) must all lie inside some index interval of length at most dist, so we only need to consider windows of indices and pick k-1 smallest numbers inside each window.
  - We maintain the sum of the smallest (k-1) numbers inside a sliding window using two heaps (max-heap for the chosen smallest group, min-heap for the rest) and lazy deletions for efficient removals as the window slides.
  - Time complexity: O(n log n) — each element is added/removed at most once; heap ops are logarithmic.
  - Space complexity: O(n) for the heaps and lazy deletion maps.