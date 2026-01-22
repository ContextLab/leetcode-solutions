# [Problem 2598: Smallest Missing Non-negative Integer After Operations](https://leetcode.com/problems/smallest-missing-non-negative-integer-after-operations/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can add or subtract `value` any number of times to any element, so each element can become any integer congruent to its original value modulo `value`. That suggests the important part of each element is its residue modulo `value`. To make the MEX as large as possible we want to create 0,1,2,... consecutively. For each target integer t we need some element whose residue equals t % value. So this becomes a resource allocation per residue: how many targets with residue r can we supply?

A straightforward greedy approach: count how many numbers have each residue r in [0, value-1]. Then try to build targets m = 0,1,2,...; for each m check residue r = m % value, if we have at least one element with that residue use it (decrement count) and continue, otherwise m is the MEX.

This should be correct because every required target number only cares about matching residue, and using one element per target is necessary.

## Refining the problem, round 2 thoughts
- Implementation detail: handle negative numbers when computing residue. In Python `x % value` gives a non-negative residue in [0, value-1], so it's fine.
- Complexity: building freq is O(n). The loop to find MEX will at most run until we fail to fill a target; since each step consumes one element, the number of successful steps <= n, so loop iterations <= n+1. So overall O(n + value) time (value for the freq array allocation) and O(value) space.
- Edge cases: when `value` > n or when many numbers share same residue; algorithm naturally handles these.
- Proof/sketch: Greedy is optimal because a target number m can only be produced by an element with residue r = m % value. Using any such element for an earlier target that has the same residue is interchangeable; the simple consumption scheme yields the maximal prefix 0..MEX-1 we can form.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def findSmallestMissingValue(self, nums: List[int], value: int) -> int:
        # Frequency of residues 0..value-1
        freq = [0] * value
        for x in nums:
            r = x % value  # Python ensures non-negative residue
            freq[r] += 1

        m = 0
        # Try to build 0,1,2,... greedily
        while True:
            r = m % value
            if freq[r] == 0:
                return m
            freq[r] -= 1
            m += 1
```
- Notes:
  - Approach: map each number to its residue modulo `value`, then greedily fill targets 0,1,2,... consuming one element from the corresponding residue group each time. When a residue group is exhausted for the next required target, that target is the MEX.
  - Time complexity: O(n + value) to build freq and run the greedy loop (the loop runs at most n+1 times).
  - Space complexity: O(value) for the frequency array.
  - Implementation detail: using Python's `%` handles negative numbers correctly (returns non-negative residue).