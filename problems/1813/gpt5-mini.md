# [Problem 1813: Sentence Similarity III](https://leetcode.com/problems/sentence-similarity-iii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to check if by inserting an arbitrary sentence (possibly empty) into one sentence we can make it equal to the other. That suggests one sentence must be a "subsequence" of words of the other where the matched words appear contiguously at the start and end (prefix + suffix), with a single contiguous block of words possibly missing in the shorter sentence. So I can compare words from the start until they differ, and from the end until they differ. If all words of the shorter sentence are covered by these prefix+suffix matches, the answer is true. If the shorter sentence has any remaining unmatched words in the middle, then we can't make them equal by a single insertion.

Plan: split sentences into word lists, ensure one is the shorter (swap if necessary), compare prefix and suffix. Check if prefix_matches + suffix_matches == len(shorter).

## Refining the problem, round 2 thoughts
Edge cases:
- Sentences identical -> true (prefix matches whole shorter).
- One-word sentences and the other longer: works via prefix or suffix matching.
- Need to swap so we always treat the shorter as the one that must be fully matched.
- Be careful with suffix comparison bounds: when comparing from the end, ensure we don't overlap the already matched prefix part of the shorter sentence.
Time complexity: splitting is O(n) where n = total characters; comparing words is O(m) where m = number of words. Space: O(m) for word lists.

This approach is linear in number of words; no complicated data structures required.

## Attempted solution(s)
```python
class Solution:
    def areSentencesSimilar(self, sentence1: str, sentence2: str) -> bool:
        # Split into words
        a = sentence1.split()
        b = sentence2.split()
        # Ensure a is the shorter (or equal) list
        if len(a) > len(b):
            a, b = b, a

        # Match prefix
        i = 0
        while i < len(a) and a[i] == b[i]:
            i += 1

        # If entire shorter sentence matched as prefix, it's similar
        if i == len(a):
            return True

        # Match suffix without overlapping the matched prefix part
        j = 0
        while j < len(a) - i and a[-1 - j] == b[-1 - j]:
            j += 1

        # If prefix matches + suffix matches cover the whole shorter sentence -> similar
        return i + j == len(a)
```
- Notes:
  - We split sentences into words (O(n) time and space).
  - We match from the start with pointer i, and from the end with pointer j, ensuring the suffix comparison does not overlap the already matched prefix region of the shorter sentence (limit j < len(a) - i).
  - The sentences are similar iff i + j == len(shorter), meaning every word of the shorter sentence is matched either in the prefix or suffix, and the middle part of the longer sentence can be the inserted sentence.
  - Time complexity: O(W) where W is the number of words (plus cost of splitting). Space complexity: O(W) for the split word lists.