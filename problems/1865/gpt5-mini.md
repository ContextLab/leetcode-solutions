# [Problem 1865: Finding Pairs With a Certain Sum](https://leetcode.com/problems/finding-pairs-with-a-certain-sum/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I'm given two arrays nums1 and nums2 and need to support two operations: add to an element of nums2, and count pairs (i, j) with nums1[i] + nums2[j] == tot. Naively counting for each query would be O(n1 * n2) which is too slow when nums2 is large (up to 1e5). However, constraints show at most 1000 calls to add and 1000 calls to count, and nums1 length ≤ 1000 while nums2 length can be large. That suggests we should precompute something for nums2 (like a frequency map) and use nums1 in an efficient way on count queries.

A useful idea: keep a frequency map (Counter/dict) of values in nums2. For count(tot) iterate over nums1 and for each x look up freq2[tot - x] and sum. If nums1 has duplicates we can compress using a freq map for nums1 too so we iterate only over unique values. For add operations, update nums2 array and update the freq map accordingly (decrement old value count and increment new value count). This gives O(1) add and O(unique_nums1) count which is fine because unique nums1 ≤ 1000.

Edge thought: nums2 values and totals can be large, but Python dict handles it. Also ensure updates reflect in both stored nums2 array and freq2.

## Refining the problem, round 2 thoughts
- Use freq1 = Counter(nums1) to avoid repeating same nums1 values in counts.
- Use freq2 = Counter(nums2) and store nums2 array for indexed updates.
- add(index, val): old = nums2[index]; freq2[old] -= 1 (and remove key if count becomes 0 or leave it — Counter handles zeros but we can delete for cleanliness); new = old + val; nums2[index] = new; freq2[new] += 1.
- count(tot): for each value v in freq1, need freq1[v] * freq2.get(tot - v, 0) summed.
- Complexity:
  - Initialization: O(n2 + n1) time, O(n2 + unique(nums1)) space for freq2 and freq1.
  - add: O(1) average time.
  - count: O(unique(nums1)) time per query (≤ 1000).
- This is efficient given constraints. Alternative approaches (e.g., sorting + two pointers) wouldn't support efficient adds.

## Attempted solution(s)
```python
from collections import Counter
from typing import List

class FindSumPairs:
    def __init__(self, nums1: List[int], nums2: List[int]):
        # Keep original arrays for updates and lookups
        self.nums1 = nums1
        self.nums2 = nums2
        # Frequency maps
        self.freq1 = Counter(nums1)   # used to iterate unique nums1 values
        self.freq2 = Counter(nums2)   # updated on add operations

    def add(self, index: int, val: int) -> None:
        old = self.nums2[index]
        # Decrement old value count
        self.freq2[old] -= 1
        if self.freq2[old] == 0:
            # remove key to keep Counter/dict small (optional)
            del self.freq2[old]
        # Update the array value
        new = old + val
        self.nums2[index] = new
        # Increment new value count
        self.freq2[new] = self.freq2.get(new, 0) + 1

    def count(self, tot: int) -> int:
        total_pairs = 0
        # Iterate over unique nums1 values and multiply by their counts
        for v, cnt_v in self.freq1.items():
            need = tot - v
            cnt_need = self.freq2.get(need, 0)
            if cnt_need:
                total_pairs += cnt_v * cnt_need
        return total_pairs
```

- Notes about the solution:
  - Approach: Maintain frequency counters for nums1 (fixed) and nums2 (mutable). For count(tot), sum freq1[val] * freq2[tot - val] over all unique val in nums1.
  - Time complexity:
    - Initialization: O(n1 + n2).
    - add: O(1) average time (two dict updates and one array update).
    - count: O(U1) where U1 is the number of unique values in nums1 (≤ n1 ≤ 1000).
  - Space complexity: O(n2 + U1) for storing nums2 and the two frequency maps.
  - Implementation details: Using Python's Counter/dict for freq2; when decrementing to 0 we remove the key to avoid keys with zero counts (optional but keeps get lookups clean). This solution fits the constraints and handles repeated calls efficiently.