# [Problem 2490: Circular Sentence](https://leetcode.com/problems/circular-sentence/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem asks to determine if a sentence is "circular": each word's last character equals the next word's first character, and the last word's last character equals the first word's first character. My first, straightforward thought is to split the sentence into words and compare adjacent words' characters. For a single word, we simply compare its last and first characters. Splitting is simple since the input guarantees single spaces and no leading/trailing spaces.

I also think about doing it without extra memory (no split), by scanning the string and checking characters around spaces. Either approach is O(n) time given sentence length <= 500, so splitting is fine and easier to read.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- Single-word sentence: check last char == first char.
- Multiple words: check for each adjacent pair words[i][-1] == words[i+1][0].
- Finally check last word's last char equals first word's first char (wrap-around).
- Input constraints guarantee words separated by a single space and no leading/trailing spaces, so split() will produce correct words without empty strings.
- Time complexity: O(L) where L is length of sentence (we read characters once; splitting also touches each char).
- Space complexity: O(W) for words list if using split, where total size is bounded by L; can be optimized to O(1) by scanning, but not necessary here.

I'll implement the split-based solution for clarity and reliability.

## Attempted solution(s)
```python
class Solution:
    def isCircularSentence(self, sentence: str) -> bool:
        # Split the sentence into words. Input guarantees single spaces and no leading/trailing spaces.
        words = sentence.split(" ")
        n = len(words)
        if n == 0:
            return False  # though by constraints sentence length >= 1, so this won't occur
        
        # Check adjacent words
        for i in range(n - 1):
            if words[i][-1] != words[i + 1][0]:
                return False
        
        # Check wrap-around: last word's last char vs first word's first char
        return words[-1][-1] == words[0][0]
```

- Notes on approach:
  - Approach: Split sentence into words and verify that for each adjacent pair, last char of the left word equals first char of the right word. Then verify the last word links back to the first word.
  - Time complexity: O(L) where L is the length of the sentence (splitting and character checks touch each character a constant number of times).
  - Space complexity: O(L) in the worst case for the list of words produced by split; can be reduced to O(1) by scanning the string directly if needed.
  - Implementation details: Using sentence.split(" ") is safe because constraints guarantee single spaces between words and no leading/trailing spaces. For a single-word sentence, the loop is skipped and the final wrap-around check compares the word's last and first characters.