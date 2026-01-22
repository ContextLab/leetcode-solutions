# [Problem 3005: Count Elements With Maximum Frequency](https://leetcode.com/problems/count-elements-with-maximum-frequency/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to find which elements appear most often, then return the total number of elements in the array that belong to those most-frequent values. The straightforward approach is to count frequencies (a hash map / Counter) and then determine the maximum frequency. Once I know the maximum frequency m, I can sum the frequencies of all values that have frequency m. That sum is simply m times the number of distinct values that have frequency m, but it's easy to compute by summing directly. Given constraints are small (n ≤ 100, values ≤ 100), either Counter or a fixed-size frequency array works.

## Refining the problem, round 2 thoughts
Edge cases: all elements unique (max freq = 1 -> answer = n), all elements the same (max freq = n -> answer = n). If multiple values tie for max frequency, count all their occurrences (so answer can be > distinct count). Time complexity target O(n), space O(k) where k is number of distinct values (≤ 100). Using collections.Counter is concise and clear. Alternatively, since nums[i] ≤ 100, a list of length 101 could be used for frequencies, but readability favors Counter.

## Attempted solution(s)
```python
from typing import List
from collections import Counter

class Solution:
    def countElementsWithMaximumFrequency(self, nums: List[int]) -> int:
        # Count frequencies of each value
        freq = Counter(nums)
        # Find maximum frequency
        if not freq:
            return 0
        max_freq = max(freq.values())
        # Sum frequencies of elements that have frequency == max_freq
        total = sum(count for count in freq.values() if count == max_freq)
        return total
```
- Approach notes: Use a frequency counter to get occurrences of each number. Compute the maximum frequency, then sum the counts of all numbers whose count equals that maximum.
- Time complexity: O(n) to build the Counter and O(k) to scan counts (k = number of distinct values, k ≤ n). Overall O(n).
- Space complexity: O(k) additional space for the Counter (k ≤ min(n, 100) given problem constraints).
- Implementation details: Handles all edge cases (empty list not expected per constraints but guarded). For small integer domain, an array-based frequency table could be used instead of Counter if desired.