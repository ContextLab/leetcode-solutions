# [Problem 1189: Maximum Number of Balloons](https://leetcode.com/problems/maximum-number-of-balloons/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to see how many times I can form the word "balloon" from the letters of the given text. The word "balloon" has repeated letters: 'l' twice and 'o' twice. So the limiting factor will be counts of each required letter in text divided by how many of that letter the word needs. I can count letters in the input and then compute how many full "balloon" words can be formed by taking the minimum across required letters after dividing where necessary. If any required letter is missing, answer is 0. This is straightforward counting.

## Refining the problem, round 2 thoughts
- Target word letter counts: b:1, a:1, l:2, o:2, n:1.
- For each of these letters, compute floor(count_in_text / required_count). The minimum of these values is the answer.
- Use a Counter or an array of size 26 for counts. Complexity will be O(n) time and O(1) additional space (since alphabet size is constant).
- Edge cases: very short text, missing letters -> result 0. Large input length up to 1e4 is trivial for counting.
- Alternative: simulate removing characters repeatedly until you can't form, but that's less efficient and unnecessary.

## Attempted solution(s)
```python
from collections import Counter

class Solution:
    def maxNumberOfBalloons(self, text: str) -> int:
        # Count letters in text
        cnt = Counter(text)
        # Required counts for the word "balloon"
        required = Counter("balloon")  # {'l':2, 'o':2, 'b':1, 'a':1, 'n':1}
        # For each required character, compute how many times it can appear,
        # then return the minimum across all required chars.
        return min(cnt[ch] // required[ch] for ch in required)
```
- Notes:
  - Approach: Count characters in the input and in the target word "balloon", then for each character in the target compute integer division of available by needed and take the minimum.
  - Time complexity: O(n) to build the Counter for the input text (n = len(text)). The final min over the small fixed set of target letters is O(1).
  - Space complexity: O(1) additional space beyond the input and small Counters (alphabet size is constant), more precisely O(26) = O(1).
  - Implementation detail: Using collections.Counter makes the code concise and clear. If a required character is missing in text, cnt[ch] is 0 and the division yields 0, correctly handling that edge case.