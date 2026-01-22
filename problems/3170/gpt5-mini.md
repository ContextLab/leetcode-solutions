# [Problem 3170: Lexicographically Minimum String After Removing Stars](https://leetcode.com/problems/lexicographically-minimum-string-after-removing-stars/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We must repeatedly take the leftmost '*' and remove it and the smallest non-'*' character to its left. The stars are processed left-to-right in the original string order. So if we scan the string left-to-right and treat each '*' as "delete one character among letters seen so far", that matches the operation order.

Key questions:
- Which occurrence of the smallest character should we remove if there are several? Removing an earlier occurrence (closer to the front) will shift later characters left and may make the prefix larger lexicographically. Removing a later occurrence (closer to the star) seems better to preserve small letters in the prefix.
- So the greedy choice appears to be: at each star, remove the smallest character among the letters seen so far, and among ties remove its rightmost occurrence (closest to the star). That should give the lexicographically smallest final string.

Data structures:
- Keep 26 stacks (lists) of indices for each letter as we scan left-to-right.
- On seeing a letter, push its index into the corresponding stack.
- On seeing '*', find the smallest letter with a non-empty stack and pop its rightmost index (mark it deleted).

Finally build the answer from letters that are not deleted (skip stars).

## Refining the problem, round 2 thoughts
- Correctness sketch: each star must remove some smallest letter to its left. Deleting the rightmost occurrence of the smallest letter is at least as good as deleting any earlier occurrence (an exchange argument: swapping deletions so we delete the rightmost smallest cannot worsen any prefix and often preserves more small letters in the front).
- Complexity: scanning once O(n). For each '*' we need to find the smallest letter present; there are only 26 letters so scanning up to 26 buckets per star is acceptable => O(26 * number_of_stars) = O(n) effectively.
- Space: O(n) to store indices and deleted flags.
- Edge cases: input may have no stars (just return s). The problem guarantees it's possible to delete all stars (i.e., when a star appears there will be at least one leftover letter to its left).

This approach is simple and efficient enough for n up to 1e5.

## Attempted solution(s)
```python
class Solution:
    def lexicographicallyMinimumStringAfterRemovingStars(self, s: str) -> str:
        """
        Greedy: scan left-to-right. Maintain 26 stacks of indices for letters seen so far.
        On each '*', pick the smallest letter with a non-empty stack and pop its rightmost index.
        Mark that index deleted. Finally build the result from non-deleted letters.
        """
        n = len(s)
        # stacks for 'a'..'z', storing indices of occurrences (in increasing order as we scan)
        stacks = [[] for _ in range(26)]
        deleted = [False] * n

        for i, ch in enumerate(s):
            if ch == '*':
                # find smallest letter with a non-empty stack
                for c in range(26):
                    if stacks[c]:
                        idx = stacks[c].pop()  # remove rightmost occurrence of this smallest letter
                        deleted[idx] = True
                        break
            else:
                stacks[ord(ch) - ord('a')].append(i)

        # build final string: include letters that are not deleted and skip '*'
        res_chars = []
        for i, ch in enumerate(s):
            if ch != '*' and not deleted[i]:
                res_chars.append(ch)
        return ''.join(res_chars)
```
- Notes about the solution approach:
  - Greedy correctness: at each star we must remove some smallest character to its left. Removing the rightmost occurrence of this smallest character preserves as much of the leading small characters as possible, yielding the lexicographically smallest final string (exchange argument).
  - Time complexity: O(n * 26) in worst case for scanning buckets at each star, which is effectively O(n) because 26 is constant. More precisely O(n + 26 * m) where m is number of stars <= n.
  - Space complexity: O(n) for storing indices and deleted flags.
  - Implementation details: using 26 lists to store indices keeps pop() as O(1). The problem guarantee ensures when encountering a star there is at least one available letter to delete.