# [Problem 1415: The k-th Lexicographical String of All Happy Strings of Length n](https://leetcode.com/problems/the-k-th-lexicographical-string-of-all-happy-strings-of-length-n/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I want the k-th lexicographical happy string of length n using letters 'a','b','c' with no two adjacent equal. For n up to 10, the total number of happy strings is small: first position has 3 choices, each subsequent position has 2 choices (anything but the previous char). So total = 3 * 2^(n-1). If k is larger than that, return "".

If k is valid, I can construct the k-th string greedily: pick the first character among ['a','b','c'] in lexicographic order. For each candidate first character, there are 2^(n-1) strings that start with it. Compare k to that block size to decide which first char to pick. After picking a character, for the next positions the alphabet of choices is the two letters different from the previous char; for each such candidate, the number of completions equals 2^(remaining_positions-1). So I can repeatedly choose characters by comparing k against block sizes and subtracting when skipping blocks. This yields O(n) time.

## Refining the problem, round 2 thoughts
Edge cases: n==1 (then block size for first char is 1, total = 3), k==1..3 handled naturally. Use bit shifts (1 << x) for powers of two. Keep k 1-indexed and decrement it when skipping blocks.

Alternative solution: generate all happy strings via DFS and return the k-th — but generating all is unnecessary and less efficient (though for n<=10 it's feasible). The greedy counting approach is cleaner and O(n) time and O(n) space.

Time complexity: O(n) because at each position we try at most 3 (first) or 2 candidates and do constant work.
Space complexity: O(n) for the output string and O(1) auxiliary.

## Attempted solution(s)
```python
class Solution:
    def getHappyString(self, n: int, k: int) -> str:
        # Total number of happy strings of length n is 3 * 2^(n-1)
        total = 3 * (1 << (n - 1))
        if k > total:
            return ""
        
        letters = ['a', 'b', 'c']
        res = []
        
        # Choose first character: each first char has block size = 2^(n-1)
        block = 1 << (n - 1)
        for ch in letters:
            if k <= block:
                res.append(ch)
                prev = ch
                break
            k -= block
        
        # Fill remaining positions
        remaining = n - 1
        while remaining > 0:
            # For each position, there are 2 choices (letters except prev),
            # and each choice has block size = 2^(remaining-1)
            block = 1 << (remaining - 1)
            # candidates in lexicographic order excluding prev
            for cand in letters:
                if cand == prev:
                    continue
                if k <= block:
                    res.append(cand)
                    prev = cand
                    break
                k -= block
            remaining -= 1
        
        return "".join(res)
```
- Notes:
  - Approach: greedy selection using block counts (powers of two) for each prefix.
  - Correctness: at each step we know how many strings share a given prefix; using that count we can decide which prefix contains the k-th string.
  - Time complexity: O(n). Space complexity: O(n) for the result string.