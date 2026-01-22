# [Problem 2537: Count the Number of Good Subarrays](https://leetcode.com/problems/count-the-number-of-good-subarrays/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the number of contiguous subarrays that contain at least k equal pairs (i < j with arr[i] == arr[j]). A direct brute-force O(n^2) enumerating all subarrays and counting pairs would be too slow for n up to 1e5.

Pairs inside a window can be tracked incrementally if we maintain counts of each value: when we add an element x, it forms "count[x]" new pairs. That suggests a sliding-window approach: expand the right pointer, update pair count, and when the window has >= k pairs, we can count some number of valid subarrays. The typical pattern: for a fixed right, if window [left..right] has >= k pairs then any extension to the right will also have >= k, so we can count how many starts (or ends) contribute. We'll use two pointers plus a freq map and maintain the current number of equal pairs.

## Refining the problem, round 2 thoughts
We can iterate right from 0..n-1, update freq and current_pairs. While current_pairs >= k, we can count subarrays starting at left that end at >= right. For the current right, all subarrays that start at left and end at any index from right to n-1 are valid; that's (n - right). After adding that to result, we shrink from left by removing nums[left] and updating current_pairs and freq, then continue the while loop. This counts every valid subarray exactly once.

Careful about updating pairs when adding/removing:
- When adding x: pairs += freq[x] (pairs formed with previous occurrences), then freq[x] += 1 (or equivalently do freq[x]+=1 and pairs += freq[x]-1).
- When removing x from left: currently freq[x] is c, removal reduces pairs by (c-1) because the removed element contributed pairs with the remaining (c-1) occurrences. Implement safely by doing freq[x] -= 1 and then pairs -= freq[x] (where freq[x] is new count after decrement).

Time complexity: O(n) since each index is visited by left and right at most once. Space: O(unique values) up to O(n).

Edge cases:
- k might be very large; if total pairs in entire array < k, answer is 0 — algorithm will naturally produce 0.
- Values of nums can be large (up to 1e9), so use a hash map (dict).

## Attempted solution(s)
```python
from collections import defaultdict
from typing import List

class Solution:
    def countGood(self, nums: List[int], k: int) -> int:
        n = len(nums)
        freq = defaultdict(int)
        left = 0
        pairs = 0
        result = 0

        for right, x in enumerate(nums):
            # Add nums[right]
            freq[x] += 1
            pairs += freq[x] - 1  # new pairs formed with existing occurrences

            # While current window has at least k pairs, count subarrays
            while pairs >= k:
                # All subarrays starting at left and ending at any index >= right are valid.
                result += (n - right)
                # Remove nums[left] and update pairs accordingly
                y = nums[left]
                freq[y] -= 1
                pairs -= freq[y]  # after decrement, freq[y] is count of y remaining; removed element had that many pairs
                left += 1

        return result
```
- Notes:
  - Approach: two-pointer sliding window + frequency hashmap. Maintain current number of equal pairs in the window; expand right, and when pairs >= k shrink left while counting how many end-extensions produce valid subarrays.
  - Time complexity: O(n) because each element is added and removed at most once.
  - Space complexity: O(m) where m is the number of distinct values in nums (<= n).
  - Implementation detail: careful ordering when updating freq and pairs — when adding do freq+=1 then pairs += freq-1; when removing do freq-=1 then pairs -= freq (the updated freq equals number of remaining same elements, which equals how many pairs the removed element contributed).