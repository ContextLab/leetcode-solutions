# [Problem 1574: Shortest Subarray to be Removed to Make Array Sorted](https://leetcode.com/problems/shortest-subarray-to-be-removed-to-make-array-sorted/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to remove one contiguous subarray so the remaining elements (concatenation of prefix and suffix) are non-decreasing. The simplest checks: if the whole array is already non-decreasing, answer is 0. If the array is strictly decreasing, we may need to keep only one element so answer ~ n-1.

A common pattern: find the longest non-decreasing prefix and the longest non-decreasing suffix. If I keep the prefix and remove everything after it, that's one candidate. If I keep the suffix and remove everything before it, that's another. There may be better answers by keeping part of the prefix and part of the suffix and removing a middle chunk — so we want to try merging the two sorted pieces by finding the smallest middle chunk that can be removed so that prefix_end element <= suffix_start element.

Two-pointer merging seems natural: move a pointer on the prefix and a pointer on the suffix to find minimal removal length. Time complexity should be linear overall.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- Exact detection of prefix end: advance i while arr[i] <= arr[i+1]. If i reaches n-1 array already sorted -> return 0.
- Exact detection of suffix start: move j backward while arr[j-1] <= arr[j].
- Initial best answer is min(n - (i+1), j) — remove everything after the prefix, or everything before the suffix.
- To do better, set r = j and iterate l from 0..i. For each l, advance r until arr[r] >= arr[l]. Then we can remove elements (l+1 .. r-1), length r-l-1. Keep minimum.
- Ensure pointers stay in bounds. If r reaches n, removal length is n - (l+1) which is handled by formula.
- Time O(n) because r only moves forward overall.
- Space O(1) besides input.

Alternative: binary search for each prefix position to find the first suitable suffix index — would be O(n log n), but two pointers is simpler and optimal.

Now implement carefully in Python as LeetCode expects (class Solution, method findLengthOfShortestSubarray).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findLengthOfShortestSubarray(self, arr: List[int]) -> int:
        n = len(arr)
        # Find longest non-decreasing prefix
        i = 0
        while i + 1 < n and arr[i] <= arr[i + 1]:
            i += 1
        # If whole array is non-decreasing
        if i == n - 1:
            return 0

        # Find longest non-decreasing suffix
        j = n - 1
        while j - 1 >= 0 and arr[j - 1] <= arr[j]:
            j -= 1

        # Remove either suffix after prefix or prefix before suffix
        ans = min(n - (i + 1), j)

        # Try to merge prefix and suffix by removing middle part
        r = j
        for l in range(i + 1):
            # Move r right until arr[r] >= arr[l]
            while r < n and arr[r] < arr[l]:
                r += 1
            # Now we can keep arr[0..l] and arr[r..n-1], remove (l+1 .. r-1)
            ans = min(ans, r - l - 1)
            # Early stop: if r == n then removing to the end, no better answer possible for larger l
            if r == n:
                # Further l will only increase removed length, so break
                break

        return ans
```
- Notes about approach: We first locate the maximal non-decreasing prefix and suffix. The naive candidates are removing after the prefix or before the suffix. To find potentially smaller removals, we try to connect some prefix element arr[l] to some suffix element arr[r] (with r >= j) such that arr[l] <= arr[r]; the removed subarray is between them. Using a two-pointer sweep ensures each index is visited at most once, so overall time is O(n).
- Complexity: Time O(n), Space O(1) (ignoring input).