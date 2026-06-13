# [Problem 3838: Weighted Word Mapping](https://leetcode.com/problems/weighted-word-mapping/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to compute a "weight" for each word by summing weights for each character. After summing, take modulo 26 and map 0 -> 'z', 1 -> 'y', ..., 25 -> 'a'. The mapping is reverse alphabetical order, so once I have remainder r in [0,25] the mapped char can be computed as chr(ord('z') - r). Words are short (<=10) and there are at most 100 words, so a straightforward loop over characters per word is fine. To keep sums small I can take modulo 26 while accumulating, though it's not necessary given constraints.

Edge cases: empty words are not allowed by constraints. Ensure weights list length is 26. Everything consists of lowercase letters.

## Refining the problem, round 2 thoughts
Implementation details:
- Iterate each word, compute sum(weights[ord(c) - ord('a')] for c in word) % 26.
- Map with chr(ord('z') - remainder).
- Append to result list and join at the end.

Complexity: O(total_characters) time and O(1) extra space besides output (output length = number of words). Because constraints are tiny this will be fast. Taking modulo during the accumulation avoids any temporary large integers (not needed here but is a good habit).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def weightedWordMapping(self, words: List[str], weights: List[int]) -> str:
        """
        For each word compute the weighted sum of its characters using the provided weights,
        take the sum modulo 26, and map 0 -> 'z', 1 -> 'y', ..., 25 -> 'a'. Return the
        concatenation of mapped characters for all words.
        """
        if not weights or len(weights) != 26:
            raise ValueError("weights must be a list of length 26")
        
        res_chars = []
        base_a = ord('a')
        base_z = ord('z')
        
        for word in words:
            # accumulate modulo 26 to keep numbers small
            sm = 0
            for ch in word:
                sm = (sm + weights[ord(ch) - base_a]) % 26
            mapped_char = chr(base_z - sm)  # 0 -> 'z', 1 -> 'y', ...
            res_chars.append(mapped_char)
        
        return ''.join(res_chars)

# Example usage / quick tests
if __name__ == "__main__":
    sol = Solution()
    words1 = ["abcd","def","xyz"]
    weights1 = [5,3,12,14,1,2,3,2,10,6,6,9,7,8,7,10,8,9,6,9,9,8,3,7,7,2]
    print(sol.weightedWordMapping(words1, weights1))  # Expected "rij"

    words2 = ["a","b","c"]
    weights2 = [1]*26
    print(sol.weightedWordMapping(words2, weights2))  # Expected "yyy"

    words3 = ["abcd"]
    weights3 = [7,5,3,4,3,5,4,9,4,2,2,7,10,2,5,10,6,1,2,2,4,1,3,4,4,5]
    print(sol.weightedWordMapping(words3, weights3))  # Expected "g"
```
- Solution approach: For each word sum the respective letter weights, take modulo 26, then map remainder r to chr(ord('z') - r).
- Time complexity: O(T) where T is total number of characters across all words (each character processed once).
- Space complexity: O(W) for the output string where W is number of words (plus O(1) extra).