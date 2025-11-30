# [Problem 1590: Make Sum Divisible by P](https://leetcode.com/problems/make-sum-divisible-by-p/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to remove the smallest contiguous subarray so that the remaining sum is divisible by p. Let total = sum(nums). If total % p == 0, return 0 immediately. Otherwise we need to remove a subarray whose sum % p equals total % p (call this need). So the problem becomes: find the shortest subarray with sum % p == need. Brute force O(n^2) checking all subarrays is too slow for n up to 1e5.

Prefix sums modulo p can help: sum(i..j) % p = (pref[j] - pref[i-1]) % p. So for each prefix remainder pref_i, we want to find a previous prefix remainder pref_j such that (pref_i - pref_j) % p == need, equivalently pref_j == (pref_i - need) % p. We can keep a map from remainder -> latest index and update as we scan. Initialize map{0: -1} to represent empty prefix. Track minimal length. If minimal length equals the whole array, not allowed (must not remove whole array), return -1.

## Refining the problem, round 2 thoughts
- Edge cases: need == 0 (already divisible) -> return 0. If no valid subarray found -> return -1.
- Must ensure we don't allow removing whole array: if best length == n -> return -1.
- Implementation detail: use modulo arithmetic carefully: (pref - need) % p gives target remainder in Python (non-negative).
- Complexity: single pass O(n) time, O(n) extra space for the map (at most n distinct remainders stored). Works for large nums since we only use remainders.
- Alternative: sliding window doesn't apply directly because elements are arbitrary and we want modulo condition, not fixed target sum.

## Attempted solution(s)
```python
class Solution:
    def minSubarray(self, nums: list[int], p: int) -> int:
        total = sum(nums)
        need = total % p
        if need == 0:
            return 0

        pref = 0
        best = len(nums) + 1
        last_index = {0: -1}  # remainder -> latest index

        for i, x in enumerate(nums):
            pref = (pref + x) % p
            # we need previous remainder such that (pref - prev) % p == need
            target = (pref - need) % p
            if target in last_index:
                length = i - last_index[target]
                if length < best:
                    best = length
            # update with current prefix remainder (store latest index)
            last_index[pref] = i

        if best <= 0 or best > len(nums) - 1:
            # best == len(nums) means removing whole array (not allowed)
            return -1
        return best
```
- Notes about solution:
  - Approach: Use prefix-sum remainders and a hashmap from remainder to latest index to find shortest subarray whose sum % p == need in one pass.
  - Correctness: For each index i, if a previous index j has remainder equal to (pref_i - need) % p, then the subarray (j+1..i) has sum % p == need. We minimize i-j.
  - Time complexity: O(n) single pass.
  - Space complexity: O(n) for the hashmap (in worst case storing one entry per index).
  - Implementation details: Initialize map with 0 -> -1 to allow subarrays starting at index 0. Ensure we do not return length equal to n (can't remove entire array).