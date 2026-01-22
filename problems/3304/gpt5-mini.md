# [Problem 3304: Find the K-th Character in String Game I](https://leetcode.com/problems/find-the-k-th-character-in-string-game-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I start with word = "a". Each operation takes the current string, increments each character to the next letter (with 'z' wrapping to 'a'), and appends that incremented string to the original. So the string doubles in length each operation (same length appended), and characters cycle modulo 26.

For k up to 500, we can simply simulate building the string until its length >= k and then return word[k-1]. Important detail: wrap 'z' -> 'a' (example with "zb" -> "zbac" confirms wrap). Since k is small (<=500), a straightforward iterative build will be efficient enough. I should consider truncating to k to avoid unnecessary growth.

One subtle thought: we only ever need the first k characters, so when appending the next block, we can stop once we have k characters. Also the increment operation is character-wise using (ord(c) - ord('a') + 1) % 26.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- k = 1 should return "a".
- When incrementing characters, ensure wrap-around for 'z'.
- Because the appended part is the same length as the current word, the total length grows quickly (doubling). For k <= 500, even naive doubling is trivial. To be memory conscious, we can truncate word to length k after each step.
- Complexity: generating characters up to k gives O(k) time and O(k) space. The increment step processes each character at most a constant number of times overall (since we cap to k), so it's efficient.

Alternative solutions:
- There is a more theoretical approach using index mapping (like recursive decomposition), but not necessary for this constraint.

I'll implement a simple loop that builds the string until length >= k, incrementing characters with modular arithmetic, and return the k-th character.

## Attempted solution(s)
```python
class Solution:
    def findKthCharacter(self, k: int) -> str:
        # Start word
        word = "a"
        # Build until we have at least k characters
        while len(word) < k:
            # generate incremented version of current word
            inc = []
            for ch in word:
                # next character with wrap-around
                nxt = chr((ord(ch) - ord('a') + 1) % 26 + ord('a'))
                inc.append(nxt)
            inc = ''.join(inc)
            # append only as much as needed to reach k to avoid unnecessary growth
            needed = k - len(word)
            if needed < len(inc):
                word += inc[:needed]
            else:
                word += inc
            # keep word truncated to k (optional but safe)
            if len(word) > k:
                word = word[:k]
        return word[k-1]
```
- Notes:
  - Approach: iterative simulation. Start from "a", repeatedly form the incremented copy and append until length >= k. Return the (k-1)-th index.
  - Character increment uses modular arithmetic to wrap 'z' to 'a'.
  - We cap appended characters to only what is needed to reach k and optionally truncate to k to keep memory small.

Complexity:
- Time: O(k). We generate at most O(k) characters overall; each character is processed a small constant number of times.
- Space: O(k) for storing the built string.