# [Problem 1920: Build Array from Permutation](https://leetcode.com/problems/build-array-from-permutation/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are given a zero-based permutation nums of length n, and we need ans where ans[i] = nums[nums[i]] for each i. Because nums is a permutation of 0..n-1 (distinct), nums[i] is a valid index into nums. The direct approach is to build a new list ans of length n and set ans[i] = nums[nums[i]]. This is straightforward and O(n) time, O(n) extra space.

The follow-up asks for O(1) extra space. That suggests encoding both old and new values in each nums[i] simultaneously (e.g., using arithmetic mixing since values are bounded by n-1). A common trick is to store combined value = old + new * n (or new + old * n) and then extract the new value by integer division / modulo.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- n >= 1 per constraints; length 1 is trivial: ans = [nums[nums[0]]] works.
- Distinctness and range guarantees make indexing safe.
- Time complexity: we must touch each element once or a constant number of times -> O(n).
- Space complexity: baseline solution uses O(n) additional space for ans. The follow-up can be satisfied with O(1) extra space by encoding new values into the existing array using multiplication by n (since values < n).
- Implementation detail for in-place trick: to avoid losing original numbers when computing nums[nums[i]], use nums[nums[i]] % n to get original value if it may have been encoded already.

I'll provide the straightforward solution (clean and idiomatic) and also show the O(1) extra space variant as an alternative method.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def buildArray(self, nums: List[int]) -> List[int]:
        """
        Simple O(n) time, O(n) extra space solution.
        """
        n = len(nums)
        return [nums[nums[i]] for i in range(n)]

    def buildArray_inplace(self, nums: List[int]) -> List[int]:
        """
        In-place O(n) time, O(1) extra space solution using value encoding.
        Each nums[i] is updated to old + new * n, where old is original nums[i],
        new is nums[old]. After encoding all, extract new values by integer division.
        """
        n = len(nums)
        # Encode both old and new into nums[i]
        for i in range(n):
            # nums[nums[i]] might already be encoded, so take % n to get original
            new_val = nums[nums[i]] % n
            nums[i] += new_val * n
        # Decode to get the new values
        for i in range(n):
            nums[i] //= n
        return nums
```
- Notes:
  - Straightforward solution: ans = [nums[nums[i]] for i in range(n)] — time O(n), space O(n).
  - In-place solution: encode both values in each element using base n:
    - Encoding step: nums[i] = old + new * n (we actually do nums[i] += (new % n) * n).
    - Decoding step: nums[i] //= n gives new.
    - Because 0 <= nums[i] < n initially and n <= 1000, multiplication won't overflow Python ints.
  - Complexity:
    - Time: O(n) for either approach (two passes in the in-place method still O(n)).
    - Space: O(n) extra for the simple approach; O(1) extra for the in-place approach (mutates input).