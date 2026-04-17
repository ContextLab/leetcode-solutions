# [Problem 3761: Minimum Absolute Distance Between Mirror Pairs](https://leetcode.com/problems/minimum-absolute-distance-between-mirror-pairs/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to find pairs (i, j) with i < j such that reverse(nums[i]) == nums[j]. The naive O(n^2) check of all pairs will be too slow for n up to 1e5. Observing structure: for a given position j, we only care about earlier indices i where reverse(nums[i]) equals nums[j]. If I process left-to-right I can record information about earlier elements so I can check quickly for each j. For each earlier index i, compute r = reverse(nums[i]) and store some mapping from r -> index(es). When I reach j, check if nums[j] exists as a key in that map. To minimize |i-j| for a fixed j, among all earlier i with the same reversed value the closest one is the most recent i (largest i). So storing only the latest index for each reversed value is sufficient to get the minimum distance. So iterate left-to-right, maintain dict mapping value -> last index of an earlier element whose reverse equals that value. Update answer with j - last_index when found, then insert/update mapping for reverse(nums[j]) = j. Reverse operation is inexpensive (<=10 digits).

## Refining the problem, round 2 thoughts
- Edge cases: no mirror pairs -> return -1.
- Reversing should drop leading zeros automatically (e.g., 120 -> 21) — the integer reverse implementation via digits handles that.
- Complexity: we perform one reverse per element and one dict lookup/update per element -> O(n * digits) time (~O(n)), O(n) extra space for the map in worst case.
- Alternative: precompute reverse for every element then use a dictionary mapping values to latest index of their reverse; same idea but two-pass or one-pass. Single-pass left-to-right is natural and optimal for minimal distance because storing latest index ensures minimal j-i.
- Confirm correctness: for any mirror pair (i, j) with i < j, when we process index j that earlier i has been stored under key reverse(nums[i]) equal to nums[j]; the stored index will be the most recent among earlier i's so the computed distance j - stored_index is the smallest possible for that j. Since we consider all j, we find global minimum.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minimumAbsDifference(self, nums: List[int]) -> int:
        def rev(x: int) -> int:
            r = 0
            while x:
                r = r * 10 + (x % 10)
                x //= 10
            return r

        last_index_for_value = {}  # maps value -> latest index i such that reverse(nums[i]) == value
        ans = float('inf')
        for j, val in enumerate(nums):
            # if there is an earlier i such that reverse(nums[i]) == val
            if val in last_index_for_value:
                i = last_index_for_value[val]
                dist = j - i
                if dist < ans:
                    ans = dist
            # store reverse(nums[j]) so future indices can match it
            last_index_for_value[rev(val)] = j

        return -1 if ans == float('inf') else ans
```
- Notes:
  - Approach: single left-to-right pass. For each index j, check if nums[j] equals the reverse of any earlier element by looking up nums[j] in a map keyed by reversed-values of earlier elements. Then store reverse(nums[j]) mapped to j for future matches.
  - Time complexity: O(n * d) where d is the number of digits in nums[i] (d <= 10), effectively O(n).
  - Space complexity: O(n) for the dictionary in the worst case.
  - Implementation detail: reverse function uses integer arithmetic so leading zeros are naturally dropped (e.g., reverse(120) -> 21).