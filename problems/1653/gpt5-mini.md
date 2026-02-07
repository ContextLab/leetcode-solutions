# [Problem 1653: Minimum Deletions to Make String Balanced](https://leetcode.com/problems/minimum-deletions-to-make-string-balanced/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to make the string "balanced" meaning no 'b' appears before an 'a' (equivalently all 'a's must come before all 'b's). We can delete characters. This is like choosing a split point where everything left should be 'a' (delete 'b's) and everything right should be 'b' (delete 'a's). Brute-force would be to try every split and count deletions, but that would be O(n^2) if done naively. There's likely an O(n) greedy/DP solution.

One convenient greedy idea: scan left to right, keep how many 'b's we've seen (these are potential problematic characters if an 'a' appears later). When we encounter an 'a', we have two choices: delete this 'a' (increment deletions) or delete all previous 'b's (which is b_count). So for each 'a' we can update the minimal deletions so far as min(delete_this_a, delete_all_prev_bs). That suggests keeping two counters: b_count and deletions, and updating deletions = min(deletions + 1, b_count) when we see an 'a'. For 'b' we just increment b_count.

This seems linear and constant-space.

## Refining the problem, round 2 thoughts
Edge cases: all 'a' (no deletions), all 'b' (no deletions), alternating patterns. The reasoning for deletions update: deletions stores the minimal deletions to make the prefix balanced. When an 'a' appears, either we delete this 'a' (so deletions+1) or we delete all earlier 'b's (b_count). Take minimum. For a 'b', no immediate conflict, just increase b_count.

Alternative solution: precompute prefix counts of 'b' and suffix counts of 'a' and take min over split i of prefix_b[i] + suffix_a[i]. That is also O(n) time and O(n) space (or O(1) if done carefully in two passes). But the greedy update is simpler and O(1) extra space.

Time complexity O(n), space O(1). n up to 1e5 so this is fine.

## Attempted solution(s)
```python
class Solution:
    def minDeletions(self, s: str) -> int:
        b_count = 0      # number of 'b's seen so far
        deletions = 0    # minimal deletions to make the prefix balanced
        for ch in s:
            if ch == 'b':
                b_count += 1
            else:  # ch == 'a'
                # Either delete this 'a' (deletions + 1) or delete all previous 'b's (b_count)
                deletions = min(deletions + 1, b_count)
        return deletions
```
- Notes: We scan once. For each character: if it's 'b', increment b_count; if it's 'a', update deletions = min(deletions + 1, b_count). This maintains the minimal deletions to make the prefix balanced. Final deletions is the answer.
- Complexity: Time O(n), Space O(1).