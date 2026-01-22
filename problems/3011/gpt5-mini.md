# [Problem 3011: Find if Array Can Be Sorted](https://leetcode.com/problems/find-if-array-can-be-sorted/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can only swap adjacent elements if they have the same number of set bits. That constraint ties swapping ability to the popcount of numbers. My first thought: group numbers by their popcount and see if each group can be sorted independently. But I need to be careful — swapping is only allowed between adjacent elements that share the same popcount, so elements with the same popcount that are separated by elements of other popcounts cannot pass through those separators. That means the relative pattern of popcounts across indices is invariant; the positions (indices) that hold a given popcount cannot be occupied by a different popcount after any sequence of allowed swaps. So the sorted target must have the same popcount at each index as the original. Moreover, within each contiguous block (run) of the same popcount in the original array we can freely reorder elements (because all adjacent pairs inside the block are swappable), but elements from different runs of the same popcount that are separated by other popcounts cannot exchange. So we must check the ability to match the globally sorted array chunk-by-chunk for each contiguous popcount run.

## Refining the problem, round 2 thoughts
Steps that make sense:
- Compute target = sorted(nums).
- If the popcount pattern (sequence of popcounts at each index) of nums differs from the popcount pattern of target, return False — because you can never move a differently-popcount element into an index occupied by another popcount.
- If the popcount patterns match, then for each contiguous run of identical popcount in the original nums, the multiset of values that currently occupy that run must be the same as the multiset of values the sorted target wants to place in those exact indices. Within a run we can permute arbitrarily (bubble-sort via allowed swaps), so multiset equality within each run is sufficient.
- Implementation detail: iterate runs of equal popcount (using .bit_count() or bin(x).count('1')), compare Counters or sorted lists for the original run and the corresponding target slice.

Time complexity: O(n log n) dominated by sorting the array of length n (n <= 100). Space complexity: O(n) for copies and counters.

## Attempted solution(s)
```python
from typing import List
from collections import Counter

class Solution:
    def canBeSorted(self, nums: List[int]) -> bool:
        n = len(nums)
        target = sorted(nums)
        # compute popcounts for original and target
        orig_pc = [x.bit_count() for x in nums]
        targ_pc = [x.bit_count() for x in target]
        # if popcount pattern differs at any index, impossible
        if orig_pc != targ_pc:
            return False
        # for each contiguous run of equal popcount, compare multisets
        i = 0
        while i < n:
            j = i + 1
            while j < n and orig_pc[j] == orig_pc[i]:
                j += 1
            # compare multiset of values in nums[i:j] with target[i:j]
            if Counter(nums[i:j]) != Counter(target[i:j]):
                return False
            i = j
        return True
```
- Notes:
  - Approach: Ensure the target sorted array has the same popcount at each index as the original (invariant), then for each contiguous run of equal popcount verify the values in that run can be permuted to match the target slice (multiset equality).
  - Correctness: You cannot move elements across indices occupied by different popcounts, so the popcount pattern per index is invariant. Inside a contiguous run of identical popcount, any permutation is achievable through adjacent swaps of equal-popcount elements.
  - Time complexity: O(n log n) due to sorting (n <= 100, so negligible). Other work is O(n).
  - Space complexity: O(n) for the target array and counters.