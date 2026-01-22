# [Problem 2364: Count Number of Bad Pairs](https://leetcode.com/problems/count-number-of-bad-pairs/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see pairs (i, j) are bad when j - i != nums[j] - nums[i]. A brute-force double loop would check all pairs but that's O(n^2) and n can be up to 1e5, so that's impossible. Try to transform the equality: j - i == nums[j] - nums[i]  <=>  nums[j] - j == nums[i] - i. That means pairs are "good" exactly when nums[k] - k is the same for both indices. So if I group indices by the value (nums[i] - i), any pair within the same group is good. Total pairs is n*(n-1)/2, so bad = total - sum_over_groups C(cnt,2). So we only need to count frequencies of nums[i]-i. That gives an O(n) solution with a hash map.

## Refining the problem, round 2 thoughts
Edge cases: n = 1 -> 0 pairs; all elements arranged so all differences equal -> no bad pairs; all differences unique -> all pairs are bad. Implementation choices: either build frequencies then compute combination sum, or accumulate good pair count on the fly by for each i adding current frequency of key (nums[i]-i) before incrementing it. Use Python dict or collections.Counter. Time complexity O(n). Space O(n) worst-case (all keys distinct). Integer sizes fit in Python ints. Return total - good (as integer).

## Attempted solution(s)
```python
from typing import List
import collections

class Solution:
    def countBadPairs(self, nums: List[int]) -> int:
        n = len(nums)
        total_pairs = n * (n - 1) // 2
        freq = collections.defaultdict(int)
        good_pairs = 0
        for i, val in enumerate(nums):
            key = val - i
            # every previous index with same key forms a good pair with current i
            good_pairs += freq[key]
            freq[key] += 1
        return total_pairs - good_pairs
```
- Notes:
  - Approach: transform condition to nums[j] - j == nums[i] - i, count frequencies of nums[i]-i and compute good pairs = sum C(count, 2), then subtract from total pairs to get bad pairs. The implementation accumulates good pairs on the fly for a single pass.
  - Time complexity: O(n), where n = len(nums).
  - Space complexity: O(n) in the worst case for the frequency dictionary.