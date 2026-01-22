# [Problem 2461: Maximum Sum of Distinct Subarrays With Length K](https://leetcode.com/problems/maximum-sum-of-distinct-subarrays-with-length-k/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
[I see we need the maximum sum among all contiguous subarrays of length k where all elements are distinct. The immediate idea is sliding window of fixed length k. For each window of size k, check if all k elements are distinct and if so consider its sum. Naively checking distinctness each time by building a set would cost O(k) per window, giving O(n*k) worst-case which is too slow for n up to 1e5. Instead maintain a frequency map of elements in the current window and the current window sum; as we slide the window we update frequencies and sum in O(1). If the frequency map has size k then all elements are distinct. So a standard fixed-size sliding window with a hashmap (or Counter) will do it in O(n).]

## Refining the problem, round 2 thoughts
[Refinements: use two pointers (left and right) or just index-based window of size k. Maintain curr_sum and freq dict. When adding a new element increment its count and add to curr_sum; when window grows > k remove leftmost element, decrement its count and subtract from curr_sum, deleting the key if count reaches 0. When window size == k check if len(freq) == k (which implies all counts are 1) and update max. Edge cases: k == 1 trivial but handled by the same logic; if no valid window found return 0. Time complexity O(n) and space O(k). Alternative: maintain a set plus a duplicate counter, but the freq dict is simplest and clear.]

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:
        n = len(nums)
        freq = {}
        curr_sum = 0
        max_sum = 0
        left = 0

        for right in range(n):
            x = nums[right]
            curr_sum += x
            freq[x] = freq.get(x, 0) + 1

            # Ensure window size does not exceed k
            if right - left + 1 > k:
                y = nums[left]
                curr_sum -= y
                freq[y] -= 1
                if freq[y] == 0:
                    del freq[y]
                left += 1

            # If window size == k and all elements distinct (freq size == k)
            if right - left + 1 == k and len(freq) == k:
                if curr_sum > max_sum:
                    max_sum = curr_sum

        return max_sum
```
- Notes:
  - Approach: fixed-size sliding window with a frequency dictionary and running sum.
  - Time complexity: O(n), where n = len(nums). Each element is added/removed at most once.
  - Space complexity: O(k) for the frequency dictionary (at most k distinct elements in a window).
  - Implementation details: Keep window as [left, right]. When window exceeds k, remove leftmost element and advance left. When window size equals k, check if the number of distinct keys in freq equals k to ensure all elements are distinct. If no valid subarray exists, max_sum remains 0 (as required).