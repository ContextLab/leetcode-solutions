# [Problem 1422: Maximum Score After Splitting a String](https://leetcode.com/problems/maximum-score-after-splitting-a-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to split s into two non-empty parts and maximize (#zeros in left) + (#ones in right). Brute force: for every split, count zeros in left and ones in right — that would be O(n^2) if we recount each time. But we can do better with prefix/suffix counts.

Observations:
- We can precompute total number of ones in the whole string.
- As we move a split from left to right one character at a time, the left side gains that character and the right side loses it.
- Maintain leftZeros and rightOnes while iterating splits; update them in O(1) per split and compute score.
- Must avoid splitting at the ends, so splits are between indices 0..n-2 (left non-empty and right non-empty).

This suggests a single pass O(n) solution with O(1) extra space.

## Refining the problem, round 2 thoughts
Refinement: initialize rightOnes = total ones. leftZeros = 0. For each index i from 0 to n-2, incorporate s[i] into the left: if s[i] == '0' increment leftZeros; if s[i] == '1' decrement rightOnes (since that '1' moved from right to left). Then compute score = leftZeros + rightOnes and track maximum.

Edge cases:
- All zeros or all ones. Example "1111": total ones = 4. As we move splits, rightOnes will decrease; maximum becomes n-1 (all left zeros = 0, right ones = n-1) so result 3 for n=4. Works.
- Minimum length 2: only one possible split; loop from 0 to 0 (n-2) handles this.

Alternative: compute prefix zeros array and suffix ones array then compute max over splits; that's O(n) time and O(n) space. But the O(1) space streaming approach is simpler.

Time complexity: O(n). Space complexity: O(1).

## Attempted solution(s)
```python
class Solution:
    def maxScore(self, s: str) -> int:
        """
        Compute maximum score after splitting s into two non-empty substrings.
        Score = (# zeros in left) + (# ones in right).
        """
        n = len(s)
        # total ones in the string -> initial rightOnes
        rightOnes = s.count('1')
        leftZeros = 0
        max_score = 0

        # we can split after index i where i ranges 0..n-2 (left non-empty, right non-empty)
        for i in range(n - 1):
            if s[i] == '0':
                leftZeros += 1
            else:  # s[i] == '1'
                rightOnes -= 1
            # compute current split score
            score = leftZeros + rightOnes
            if score > max_score:
                max_score = score

        return max_score
```
- Notes:
  - Approach: single pass maintaining leftZeros and rightOnes; update based on s[i] and compute score for each valid split.
  - Time complexity: O(n) where n = len(s), since we traverse string once.
  - Space complexity: O(1) extra space (just a few counters).
  - Implementation detail: loop goes to n-1 exclusive so we never consider empty left or empty right.