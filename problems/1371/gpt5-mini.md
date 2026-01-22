# [Problem 1371: Find the Longest Substring Containing Vowels in Even Counts](https://leetcode.com/problems/find-the-longest-substring-containing-vowels-in-even-counts/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the longest substring where each vowel (a, e, i, o, u) appears an even number of times. Parity (even/odd) suggests toggling states rather than counting exact occurrences. For each prefix of the string I can record the parity state of the five vowels; if two prefixes have the same parity state then the substring between them has every vowel appearing an even number of times (because parities cancel). That makes me think of a bitmask of 5 bits (one bit per vowel) that I toggle as I scan the string left to right. If I remember the earliest index where each mask first occurred, when I encounter the same mask again I can compute a candidate substring length. This yields an O(n) single-pass approach with small constant extra space (at most 32 states).

## Refining the problem, round 2 thoughts
- Represent vowels as bits: a -> bit0, e -> bit1, i -> bit2, o -> bit3, u -> bit4. Start with mask = 0 at index -1 so substrings starting at index 0 are handled correctly.
- Use an array of size 32 to store first occurrence index for each mask; initialize entries to a sentinel (e.g., -2) except mask 0 which maps to -1.
- For each character, if it's a vowel flip the corresponding bit (mask ^= (1 << bit)). If the mask was seen before, update answer with current_index - first_index_of_mask. If not seen, record current_index as first occurrence.
- Complexity: O(n) time, O(1) space (32 ints). Edge cases: all consonants (mask stays 0 so full length), single character, shortest/long tests (n up to 5e5) — algorithm is linear and memory constant so fine.
- Alternative approaches (inefficient): brute force O(n^2) checking parity counts, not acceptable for 5e5.

## Attempted solution(s)
```python
class Solution:
    def findTheLongestSubstring(self, s: str) -> int:
        # Map vowels to bits: a=0, e=1, i=2, o=3, u=4
        vowel_to_bit = {'a':0, 'e':1, 'i':2, 'o':3, 'u':4}
        # There are 2^5 = 32 possible parity states
        first_seen = [-2] * 32
        # mask 0 (all even) is considered seen at index -1 (prefix before string)
        first_seen[0] = -1
        
        mask = 0
        max_len = 0
        
        for i, ch in enumerate(s):
            if ch in vowel_to_bit:
                mask ^= 1 << vowel_to_bit[ch]
            # If we've seen this mask before, update max length
            if first_seen[mask] != -2:
                curr_len = i - first_seen[mask]
                if curr_len > max_len:
                    max_len = curr_len
            else:
                # Record first occurrence of this mask
                first_seen[mask] = i
        
        return max_len
```
- Notes:
  - Approach: use prefix parity mask (bitmask of 5 vowels). If mask repeats between two indices, the substring between them has even counts for all vowels.
  - Time complexity: O(n), where n = len(s). Each character processed in O(1).
  - Space complexity: O(1) (array of size 32 and a few scalars).
  - Implementation detail: setting first_seen[0] = -1 ensures substrings starting at index 0 are handled (length = i - (-1) = i+1). Using a sentinel (-2) distinguishes "not seen yet" from index 0 or -1.