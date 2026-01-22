# [Problem 1128: Number of Equivalent Domino Pairs](https://leetcode.com/problems/number-of-equivalent-domino-pairs/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see each domino is a pair [a, b] with values 1..9. Two dominoes are equivalent if they are the same pair up to order, so [a,b] is equivalent to [b,a]. A natural idea is to canonicalize each domino so order doesn't matter, e.g. sort the two numbers or take (min, max). Then count how many times each canonical domino appears; for a canonical value that appears k times it contributes C(k,2) = k*(k-1)/2 pairs. Alternatively, while scanning, I can keep counts and for each new domino add the current count for its canonical key to the answer (incremental counting). Because values are small (1..9) I could also use a fixed-size array keyed by 10*min + max instead of a dict.

## Refining the problem, round 2 thoughts
Edge cases: very small arrays (length 1) should return 0. Using incremental addition avoids computing combinations at the end and is straightforward. Time complexity should be O(n) and space can be considered O(1) bounded by 100 possible canonical keys (since a,b in 1..9 => keys in 11..99 with only 45 possible unordered pairs), so using an array of size 100 or a hashmap both work fine. I'll implement the incremental counting approach with a small fixed-size list for speed and simplicity.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def numEquivDominoPairs(self, dominoes: List[List[int]]) -> int:
        # counts for keys 0..99 (we'll use a*10 + b where a <= b)
        counts = [0] * 100
        ans = 0
        for a, b in dominoes:
            if a <= b:
                key = a * 10 + b
            else:
                key = b * 10 + a
            ans += counts[key]
            counts[key] += 1
        return ans
```
- Notes:
  - Approach: canonicalize each domino as (min, max) encoded into an integer key (a*10 + b). Keep an array of counts for keys and perform incremental counting: for each domino, the number of new pairs it forms equals how many identical canonical dominoes we've seen before.
  - Time complexity: O(n), where n = len(dominoes), since each domino is processed once.
  - Space complexity: O(1) (bounded), specifically O(100) = O(1) extra space for the counts array; or if using a hashmap, O(k) where k ≤ 45 distinct unordered domino types.
  - Implementation details: encoding as a*10 + b is safe because domino values are 1..9, so keys are two-digit numbers that uniquely represent ordered pairs with a ≤ b.