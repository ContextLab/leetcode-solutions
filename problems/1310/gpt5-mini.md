# [Problem 1310: XOR Queries of a Subarray](https://leetcode.com/problems/xor-queries-of-a-subarray/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This asks for XOR of subarray ranges for multiple queries. Computing each query by looping from left to right would be O(n) per query and too slow when queries are many. XOR has a useful associative/invertible property: if prefix_xor[i] = arr[0] ^ arr[1] ^ ... ^ arr[i-1] (prefix_xor[0] = 0), then XOR of arr[l..r] equals prefix_xor[r+1] ^ prefix_xor[l]. So precompute prefix XORs once in O(n), then answer each query in O(1).

## Refining the problem, round 2 thoughts
- Build prefix_xor array of length n+1 (prefix_xor[0] = 0). For i from 0..n-1 do prefix_xor[i+1] = prefix_xor[i] ^ arr[i].
- For query [l, r] answer is prefix_xor[r+1] ^ prefix_xor[l].
- Edge cases: l = 0 works because prefix_xor[0] = 0.
- Time complexity: O(n + q). Space complexity: O(n) for prefix_xor (can be reduced by modifying arr in-place to store prefix values if desired).
- Alternative: brute force (too slow). No other trick needed.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def xorQueries(self, arr: List[int], queries: List[List[int]]) -> List[int]:
        # Build prefix XOR array where pref[i] = XOR of arr[0..i-1], pref[0] = 0
        n = len(arr)
        pref = [0] * (n + 1)
        for i in range(n):
            pref[i+1] = pref[i] ^ arr[i]
        
        result = []
        for l, r in queries:
            # XOR of arr[l..r] = pref[r+1] ^ pref[l]
            result.append(pref[r+1] ^ pref[l])
        return result
```
- Notes:
  - Approach: prefix XOR (cumulative XOR) to answer each query in O(1).
  - Time complexity: O(n + q) where n = len(arr), q = len(queries).
  - Space complexity: O(n) for the prefix array (can be reduced to O(1) extra by using arr to store running XORs).
  - Works for all valid inputs including l = 0, and handles large arr[i] values within Python's integer range.