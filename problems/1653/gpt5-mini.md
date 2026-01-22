# [Problem 1653: Minimum Deletions to Make String Balanced](https://leetcode.com/problems/minimum-deletions-to-make-string-balanced/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to make the string "balanced" meaning no 'b' appears before an 'a'. That effectively means after deletions the string must look like all 'a's followed by all 'b's (i.e., zero or more 'a's then zero or more 'b's). So any occurrence of a 'b' followed later by an 'a' is a conflict that requires deleting at least one of those characters. 

Brute force would consider deleting combinations, but n up to 1e5 disallows exponential approaches. A natural idea: scan left-to-right keeping track of how many 'b's I've seen (these are potential problematic characters if an 'a' appears later). For each 'a', I can either delete this 'a' (increment deletions) or delete all previously seen 'b's instead. So for each 'a' choose the cheaper option. That suggests a greedy/dynamic update while scanning with O(1) state.

Another equivalent approach: consider every partition between characters; delete all 'b's on the left plus all 'a's on the right, compute minimum over partitions (prefix/suffix counts). That is O(n) with prefix/suffix counts.

## Refining the problem, round 2 thoughts
Refine the greedy invariant: maintain b_count = number of 'b' seen so far, and deletions = minimum deletions to make prefix balanced. When a 'b' arrives, it never creates a new conflict with previous characters (it can be kept), so b_count++ and deletions unchanged. When an 'a' arrives, it conflicts with all prior b's unless we delete either this 'a' or those prior b's. The best for the prefix becomes min(deletions+1 (delete this a), b_count (delete all prior b's)). Update deletions to that min.

Edge cases: all 'a' or all 'b' should work (result 0). Complexity: O(n) time, O(1) extra space. The partition method would use O(n) space if implemented with arrays, but can be done with two passes and O(1) as well.

This greedy is standard and provably correct because the local choice keeps the prefix optimal (DP with 2 states collapses to this).

## Attempted solution(s)
```python
class Solution:
    def minimumDeletions(self, s: str) -> int:
        """
        Greedy/Dynamic approach:
        b_count: number of 'b' characters seen so far
        deletions: minimum deletions to make the processed prefix balanced
        For each char:
          - if 'b': keep it, increment b_count
          - if 'a': either delete this 'a' (deletions+1) or delete all prior b's (b_count)
            choose the cheaper option and set deletions accordingly
        """
        b_count = 0
        deletions = 0
        for ch in s:
            if ch == 'b':
                b_count += 1
            else:  # ch == 'a'
                # either delete this 'a' (deletions + 1) or delete all previous 'b's (b_count)
                deletions = min(deletions + 1, b_count)
        return deletions
```
- Notes:
  - Approach: Single left-to-right scan maintaining two integers. For each 'a' decide between deleting it or deleting all previous 'b's.
  - Time complexity: O(n), where n = len(s), since we scan once.
  - Space complexity: O(1), only two integers of extra space.
  - Correctness: The update preserves the optimal minimum deletions for the prefix. When seeing an 'a', the only conflict is with prior 'b's; either remove this 'a' or remove enough prior 'b's — taking the minimum yields the optimal prefix solution. The process extends greedily to the whole string.