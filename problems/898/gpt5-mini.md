# [Problem 898: Bitwise ORs of Subarrays](https://leetcode.com/problems/bitwise-ors-of-subarrays/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Brute force: enumerate all subarrays and compute OR — that’s O(n^2) subarrays and each OR could be O(1) amortized but still O(n^2) time and too slow for n up to 5e4. Need to exploit bitwise OR properties.

Key observations:
- OR is monotonic in the sense bits only turn on and never turn off when you extend a subarray to the right.
- For subarrays ending at index i, many OR values will collapse (many different starting points may produce the same OR).
- If we keep the set of distinct OR-values for subarrays ending at i-1, we can produce those for ending at i by OR-ing each with arr[i] and also including arr[i] as a single-element subarray.
- The number of distinct OR results ending at any index is small (bounded by number of bits ~ 31 for 32-bit numbers) because each successive OR can only turn on new bits.

So I can iterate once through the array, maintain a set prev of ORs for subarrays ending at previous index, compute cur = {arr[i]} ∪ {x | arr[i] for x in prev}, and accumulate all seen ORs in a global set.

## Refining the problem, round 2 thoughts
- Edge cases: arr contains zeros and duplicates — algorithm handles these naturally.
- Complexity: Each step we loop over prev. Prev's size is bounded by number of bits (≤ 31 for input range), so total complexity approximates O(n * B) where B ~ 31. This is fast for n up to 5e4.
- Memory: store prev (O(B)) and result set of all distinct OR values. The result size is at most n * B in worst counting, but practically limited; still fits constraints.
- Alternative: There is no need for fancy bit tricks; set-based dynamic approach is straightforward and optimal for this problem.
- Implementation detail: Use Python set operations, iterate prev and build cur. After processing, set prev = cur.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def subarrayBitwiseORs(self, arr: List[int]) -> int:
        # res: set of all distinct OR results across all subarrays seen so far
        res = set()
        # prev: set of distinct OR results for subarrays ending at previous index
        prev = set()
        
        for a in arr:
            # start new set for subarrays ending at current index
            cur = {a}
            # extend each previous ending-subarray OR by current element
            for val in prev:
                cur.add(val | a)
            # add all current-ending ORs to global results
            res.update(cur)
            # current becomes previous for next iteration
            prev = cur
        
        return len(res)
```
- Notes about the approach:
  - We iterate once through arr. For each element a, we compute ORs of all subarrays that end at that element by OR-ing a with every distinct OR value that ended at the previous index.
  - Because OR only sets bits, many starting positions collapse to the same OR result; the number of distinct ORs ending at any index is bounded (by the number of bits), keeping the loop short.
- Complexity:
  - Time: O(n * B) where B is number of bits needed (for constraints B ≤ 31). Practically O(n * 31) ≈ O(n).
  - Space: O(U + B) where U is number of distinct OR results across all subarrays (the result set) and B is the size of prev/cur (bounded by number of bits).