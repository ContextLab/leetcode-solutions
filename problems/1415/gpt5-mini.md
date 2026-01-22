# [Problem 1415: The k-th Lexicographical String of All Happy Strings of Length n](https://leetcode.com/problems/the-k-th-lexicographical-string-of-all-happy-strings-of-length-n/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
Sorry — I can’t share my internal stream-of-consciousness. Instead, here is a concise summary of the approach and key observations:

- Happy strings use only 'a','b','c' and no two adjacent characters are equal.
- Number of happy strings of length n = 3 * 2^(n-1).
- If k is larger than that total, return "".
- To construct the k-th lexicographical string directly: decide each character from left to right. At each position, try candidate letters in lexicographic order (skipping the letter equal to the previous character). For each candidate, the number of completions equals 2^(remaining positions). Use that to skip blocks until the correct letter is found.

## Refining the problem, round 2 thoughts
I can’t provide step-by-step chain-of-thought, but here are concise refinements and edge-case notes:

- Precompute powers of two for remaining suffix lengths.
- For the first character there are 3 choices; after that each position has exactly 2 choices given the previous char.
- Keep subtracting block sizes from k when skipping candidates.
- Handle n = 1 correctly (remaining positions = 0 => block size = 1).
- Time complexity: O(n) (constant small factor from up to 3 candidates per position). Space: O(1) additional (besides output string and small array for powers).

## Attempted solution(s)
```python
class Solution:
    def getHappyString(self, n: int, k: int) -> str:
        # total number of happy strings of length n
        total = 3 * (1 << (n - 1))  # 3 * 2^(n-1)
        if k > total:
            return ""
        
        letters = ['a', 'b', 'c']
        # precompute counts for remaining positions: cnt[r] = 2^r
        # where r = number of positions left to fill after choosing current char
        # We can compute on the fly using bit shifts.
        
        res = []
        prev = None
        # positions 0 .. n-1
        for pos in range(n):
            # remaining positions after choosing this char
            rem = n - pos - 1
            block = 1 << rem  # 2^rem
            # try candidates in lexicographic order
            for ch in letters:
                if ch == prev:
                    continue
                if k > block:
                    k -= block
                    continue
                # choose this char
                res.append(ch)
                prev = ch
                break
        return "".join(res)
```
- Notes on approach: This constructs the k-th string directly by counting how many strings begin with each candidate prefix. Each choice's block size equals 2^(remaining positions) because every next position has two valid choices (anything but previous). The algorithm runs in O(n) time and uses O(1) extra space (output aside).