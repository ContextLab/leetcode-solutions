# [Problem 3335: Total Characters in String After Transformations I](https://leetcode.com/problems/total-characters-in-string-after-transformations-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The transformation rules act on each character independently: non-'z' becomes the next letter (one character), 'z' becomes "ab" (two characters). So the contributions of different starting characters don't interact except by producing different letters in subsequent steps. That suggests treating the process as counts of letters evolving over t steps. We can maintain a length-26 vector of frequencies for letters 'a'..'z' and simulate t transformations with simple linear updates. Since there are only 26 states, each step is O(26) and total cost O(26 * t), which is fine for t up to 1e5. We must do all arithmetic modulo 1e9+7.

Another perspective: for a single starting character ch, define f(ch, k) = resulting length after k steps; the same recurrence arises: f(ch,k) = f(next(ch), k-1) for ch!='z', and f('z',k)=f('a',k-1)+f('b',k-1). But it's simpler to simulate counts for the whole string at once.

## Refining the problem, round 2 thoughts
- Initialization: counts from s (frequency of each letter).
- Transition in one step:
  - For i in 0..24 (letters 'a'..'y'): all counts[i] move to position i+1.
  - For i == 25 ('z'): counts[25] split into +counts[25] at position 0 ('a') and +counts[25] at position 1 ('b').
- Repeat the transition t times, each time apply mod 1e9+7.
- Edge cases:
  - t = 0 (not in constraints, t >= 1 here but algorithm would still work).
  - s length up to 1e5, but we only build initial counts; simulation time depends on t only.
- Complexity: O(26 * t + |s|) time, O(26) space. With t up to 1e5 this is ~2.6e6 small operations, fine in Python.

## Attempted solution(s)
```python
MOD = 10**9 + 7

class Solution:
    def getLength(self, s: str, t: int) -> int:
        # counts[i] = number of letter chr(ord('a') + i) currently in the string
        counts = [0] * 26
        for ch in s:
            counts[ord(ch) - 97] += 1

        for _ in range(t):
            new = [0] * 26
            # letters 'a'..'y' shift to next letter
            for i in range(25):
                if counts[i]:
                    new[i + 1] = (new[i + 1] + counts[i]) % MOD
            # 'z' splits into 'a' and 'b'
            if counts[25]:
                val = counts[25] % MOD
                new[0] = (new[0] + val) % MOD
                new[1] = (new[1] + val) % MOD
            counts = new

        return sum(counts) % MOD

# If using LeetCode signature:
# class Solution:
#     def getLength(self, s: str, t: int) -> int:
#         ...
```

- Notes about the approach:
  - We treat the entire string as a frequency vector over 26 letters and simulate t transformations. Each step applies a fixed linear update based on the rules.
  - Time complexity: O(26 * t + n) where n = len(s). Space complexity: O(1) extra (26-sized arrays).
  - All arithmetic is done modulo 10^9 + 7 to avoid overflow. The approach is straightforward, easy to implement, and efficient for the given constraints.