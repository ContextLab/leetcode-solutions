# [Problem 2958: Length of Longest Subarray With at Most K Frequency](https://leetcode.com/problems/length-of-longest-subarray-with-at-most-k-frequency/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the longest contiguous subarray where every distinct value appears at most k times. This suggests a sliding-window (two pointers) approach that maintains counts per value for the current window. As we extend the right pointer we update the count of that element; if its count exceeds k we must move the left pointer until the window becomes valid again. Since adding one element only increments the count of that element, only that element can cause an immediate violation, so shrinking until that element's count <= k will restore validity. This should be O(n) time.

Edge cases: if k >= n then the whole array is valid. Repeated single value arrays should return min(count, k). Large values in nums (up to 1e9) are fine as keys in a dictionary.

## Refining the problem, round 2 thoughts
- Use a dictionary (or collections.defaultdict) to track counts of elements in current window.
- Two pointers l and r; for each r increment count[nums[r]]. While count[nums[r]] > k, decrement count[nums[l]] and increment l.
- After making it valid, update maximum window length.
- Time complexity O(n) because each element is added once and removed at most once. Space complexity O(m) where m is the number of distinct elements in nums (<= n).
- Alternative approaches (like binary search + check) are possible but unnecessary since the straightforward two-pointer approach is linear and simple.

## Attempted solution(s)
```python
from typing import List
from collections import defaultdict

class Solution:
    def longestSubarray(self, nums: List[int], k: int) -> int:
        """
        Return the length of the longest contiguous subarray where each element's
        frequency in that subarray is <= k.
        """
        count = defaultdict(int)
        l = 0
        max_len = 0

        for r, val in enumerate(nums):
            count[val] += 1
            # If this value now exceeds k, shrink from the left until it's <= k
            while count[val] > k:
                count[nums[l]] -= 1
                l += 1
            # window [l..r] is valid
            max_len = max(max_len, r - l + 1)

        return max_len
```
- Notes on approach: This uses a standard sliding-window (two pointers) technique with a hash map for counts. When adding nums[r] causes its frequency to exceed k, we move the left pointer forward, decrementing counts, until that frequency no longer exceeds k. Because only the newly added element's count increases at each step, only that element can cause a violation, so shrinking based on that element is sufficient to restore validity.
- Time complexity: O(n), where n = len(nums). Each index is visited at most twice (once by r when added, once by l when removed).
- Space complexity: O(m) for the count dictionary, where m is the number of distinct elements in nums (m <= n).

Here is the problem:

**Title:** Length of Longest Subarray With at Most K Frequency
**Difficulty:** Medium
**Link:** https://leetcode.com/problems/length-of-longest-subarray-with-at-most-k-frequency/description/?envType=daily-question

**Problem Description:**
You are given an integer array nums and an integer k.

The frequency of an element x is the number of times it occurs in an array.

An array is called good if the frequency of each element in this array is less than or equal to k.

Return the length of the longest good subarray of nums.

A subarray is a contiguous non-empty sequence of elements within an array.

Example 1:
Input: nums = [1,2,3,1,2,3,1,2], k = 2
Output: 6
Explanation: The longest possible good subarray is [1,2,3,1,2,3] since the values 1, 2, and 3 occur at most twice in this subarray. Note that the subarrays [2,3,1,2,3,1] and [3,1,2,3,1,2] are also good.
It can be shown that there are no good subarrays with length more than 6.

Example 2:
Input: nums = [1,2,1,2,1,2,1,2], k = 1
Output: 2
Explanation: The longest possible good subarray is [1,2] since the values 1 and 2 occur at most once in this subarray. Note that the subarray [2,1] is also good.
It can be shown that there are no good subarrays with length more than 2.

Example 3:
Input: nums = [5,5,5,5,5,5,5], k = 4
Output: 4
Explanation: The longest possible good subarray is [5,5,5,5] since the value 5 occurs 4 times in this subarray.
It can be shown that there are no good subarrays with length more than 4.

Constraints:
- 1 <= nums.length <= 10^5
- 1 <= nums[i] <= 10^9
- 1 <= k <= nums.length