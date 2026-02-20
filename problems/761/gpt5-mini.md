# [Problem 761: Special Binary String](https://leetcode.com/problems/special-binary-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The string is "special": equal number of 1s and 0s and every prefix has at least as many 1s as 0s. I remember this problem: we can treat the string as concatenation of balanced "primitive" special substrings (each starts with 1, ends with 0 and is balanced). The allowed operation swaps two consecutive special substrings. Swapping consecutive blocks repeatedly means we can reorder sibling special blocks (at the same nesting level). To maximize lexicographically, we want larger blocks (as strings) earlier. But inside each primitive block we can also reorder its inner children to make it maximal — recursion.

So approach: parse top-level balanced blocks, for each block process the inner substring recursively to make it maximal, then sort those processed blocks in descending lexicographic order and concatenate. Each block is returned as "1" + inner_max + "0".

This is a standard recursive greedy solution.

## Refining the problem, round 2 thoughts
- Parsing: iterate with a balance counter; when counter returns to zero we found a top-level block.
- For each block we recursively apply the same routine to its inner content (excluding the leading 1 and trailing 0).
- After we obtain all processed child blocks at current level, sort them in reverse lexicographic order and join.
- Edge cases: s = "10" (base case) returns "10". Nested structures are handled by recursion.
- Complexity: Each character is visited in parsing; recursive calls process disjoint substrings. Sorting at each level may cause extra string comparisons; worst-case complexity is often O(n log n) with string comparison costs, but upper bound can be O(n^2) in practice for small n (n ≤ 50 here), which is fine.
- Space: recursion stack up to nesting depth (≤ n), plus storage of substrings (total O(n)).

## Attempted solution(s)
```python
class Solution:
    def makeLargestSpecial(self, s: str) -> str:
        # Helper that processes s and returns the largest special string for that segment
        if len(s) <= 2:
            return s  # "10" or empty
        
        parts = []
        i = 0
        n = len(s)
        while i < n:
            # find a balanced primitive substring starting at i
            cnt = 0
            j = i
            while j < n:
                if s[j] == '1':
                    cnt += 1
                else:
                    cnt -= 1
                j += 1
                if cnt == 0:
                    # s[i:j] is a primitive special substring
                    # process the inner part recursively (exclude outer 1 and 0)
                    inner = s[i+1:j-1]
                    parts.append('1' + self.makeLargestSpecial(inner) + '0')
                    break
            i = j
        
        # sort parts in descending lexicographic order and concatenate
        parts.sort(reverse=True)
        return ''.join(parts)
```
- Notes:
  - Approach: recursively parse top-level primitive special substrings, maximize each recursively, then sort them in descending lexicographic order and join. Each primitive is of form "1" + inner + "0".
  - Correctness intuition: swapping adjacent special substrings allows arbitrary reordering of sibling blocks; to maximize lexicographic order place the lexicographically largest blocks first. Recursively making each block maximal ensures optimality.
  - Time complexity: O(n * log n) for sorting comparisons dominated by string comparison cost; worst-case upper bound O(n^2) across recursion due to repeated concatenations and comparisons. Given constraint n ≤ 50 this is acceptable.
  - Space complexity: O(n) extra for parts and recursion stack.