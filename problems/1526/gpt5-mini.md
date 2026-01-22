# [Problem 1526: Minimum Number of Increments on Subarrays to Form a Target Array](https://leetcode.com/problems/minimum-number-of-increments-on-subarrays-to-form-a-target-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I start by thinking about what one operation (incrementing a subarray by 1) does: it adds a "layer" of +1 to a contiguous segment. Building the target array from zeros is like stacking layers of contiguous segments. If the array were non-decreasing, we could keep extending the right end; if it decreases, we must stop some segments. Intuitively the number of operations seems related to how many new height units appear when moving left-to-right: whenever the next element is larger than the previous, we need additional increments to raise that position from the previous height to the new one. Decreases don't require extra operations because you can just stop extending the subarray. So maybe sum of positive increases between consecutive elements (with previous = 0 for the first element) gives the answer.

I also recall a known greedy / observation solution: answer = sum(max(0, target[i] - target[i-1])) with target[-1] = 0. That fits the layer interpretation: each time height increases, you must start (increase) that many new layers covering this index (and possibly extending further).

I'll check small examples mentally: [1,2,3,2,1] -> increases: 1-0=1, 2-1=1, 3-2=1, 2-3=-1->0, 1-2=-1->0 -> sum = 3 matches. [3,1,1,2] -> 3-0=3, 1-3=-2->0, 1-1=0, 2-1=1 -> sum=4 matches.

Edge cases: single element, all equal, strictly decreasing, large values. Complexity should be O(n) time, O(1) extra space.

## Refining the problem, round 2 thoughts
The greedy observation needs a short justification: think of each integer unit of height as a layer that must be applied as a contiguous subarray operation. A layer can cover a contiguous region where target >= layer_index. If you sweep from left to right and track previous height, whenever current > previous you need (current-previous) new layers that start at this index. When current <= previous no new layers start. Summing starts gives total layers (operations). This argument is standard and tight.

Alternative approaches like segment-tree simulation or difference-array manipulation are unnecessary here because the simple difference-sum is optimal and O(n). Space O(1) suffices.

Complexity: single pass over array O(n) time, O(1) extra space. For length up to 1e5 and target values up to 1e5, result fits 32-bit as guaranteed.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minNumberOperations(self, target: List[int]) -> int:
        # Greedy/sweep approach: sum of positive increases between consecutive elements,
        # treating previous value before index 0 as 0.
        if not target:
            return 0
        ops = 0
        prev = 0
        for x in target:
            if x > prev:
                ops += x - prev
            prev = x
        return ops

# Quick internal tests
if __name__ == "__main__":
    sol = Solution()
    print(sol.minNumberOperations([1,2,3,2,1]))  # 3
    print(sol.minNumberOperations([3,1,1,2]))    # 4
    print(sol.minNumberOperations([3,1,5,4,2]))  # 7
    print(sol.minNumberOperations([1]))          # 1
    print(sol.minNumberOperations([5,5,5]))      # 5
    print(sol.minNumberOperations([5,4,3,2,1]))  # 5
```
- Notes about the solution approach:
  - We interpret each unit-height layer as a contiguous block. Sweeping left-to-right, new layers must start exactly when the current value exceeds the previous value; the number of new layers is that difference.
  - Time complexity: O(n), where n = len(target).
  - Space complexity: O(1) extra space (only a couple of integer variables).
  - Implementation detail: treat previous height before index 0 as 0 so the first element contributes target[0] operations if >0.