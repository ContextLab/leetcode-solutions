# [Problem 3318: Find X-Sum of All K-Long Subarrays I](https://leetcode.com/problems/find-x-sum-of-all-k-long-subarrays-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to compute, for every k-length sliding window, the "x-sum": keep only the occurrences of the top x most frequent elements (ties broken by larger element value), then sum the kept elements (equivalently sum freq * value for the selected elements). With n <= 50 and nums[i] <= 50, brute-force per window is perfectly fine. For each window I can count frequencies (Counter), sort distinct elements by (frequency desc, value desc), take the top x and sum freq*value. If distinct elements < x, just sum whole window. I should also note the special easy case: if k == x, the x-sum is the sum of the window directly.

## Refining the problem, round 2 thoughts
Edge cases: windows with fewer distinct elements than x (we keep everything), tie-breaking when frequencies equal (choose larger value), k==x optimization, tiny input sizes mean no need for complex data structures. Complexity: for each of up to n windows, counting takes O(k) and sorting at most min(k, 50) items so overall cost is small: O(n * (k + m log m)), m distinct per window. Memory O(m). This is simple and reliable.

## Attempted solution(s)
```python
from typing import List
from collections import Counter

class Solution:
    def xSumOfAllKLengthSubarrays(self, nums: List[int], k: int, x: int) -> List[int]:
        n = len(nums)
        res: List[int] = []
        for i in range(n - k + 1):
            window = nums[i:i+k]
            # Count frequencies
            cnt = Counter(window)  # mapping value -> frequency
            # Sort distinct elements by (frequency desc, value desc)
            # Counter.items() yields (value, freq)
            items = sorted(cnt.items(), key=lambda iv: (-iv[1], -iv[0]))
            s = 0
            taken = 0
            for val, freq in items:
                if taken >= x:
                    break
                s += val * freq
                taken += 1
            res.append(s)
        return res
```
- Approach notes: For each k-length window, count frequencies using Counter, sort distinct elements by (-frequency, -value) so higher frequency and, on ties, larger value come first. Sum freq*value for the first x items (or all if fewer).
- Time complexity: O(n * (k + m log m)) where n is length of nums, k window size, m is number of distinct elements in a window (m <= min(k, 50)). Given constraints this is efficient.
- Space complexity: O(m) for the counter and temporary structures.