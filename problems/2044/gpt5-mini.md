# [Problem 2044: Count Number of Maximum Bitwise-OR Subsets](https://leetcode.com/problems/count-number-of-maximum-bitwise-OR-subsets/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the number of non-empty subsets whose bitwise OR equals the maximum possible OR obtainable from any subset. The maximum OR of any subset cannot exceed the OR of all elements, and in fact the OR of all elements is the maximum possible OR (since adding elements never clears bits). So compute total_or = OR of all nums; then count how many non-empty subsets produce OR == total_or.

n <= 16 so enumerating subsets (2^n <= 65536) is feasible. A straightforward approach is to either iterate all masks or do DFS/backtracking. We can prune: if current OR reaches total_or at some point, every choice for remaining elements (include or exclude) will keep OR == total_or, so we can add 2^(remaining) combinations at once. We must ensure we don't count the empty subset; handle the degenerate case when total_or == 0 (though with nums[i] >= 1 this won't occur, but I'll make the solution robust).

## Refining the problem, round 2 thoughts
- Compute target = OR of all numbers.
- Use DFS(index, cur_or, chosen_any) where chosen_any indicates whether we've picked at least one element so we won't accidentally count the empty subset when target == 0.
- If cur_or == target at index i, remaining choices are 2^(n-i) subsets; if we haven't chosen any yet (chosen_any == False), subtract 1 to exclude the empty subset of the remaining elements.
- Otherwise, continue branching include/exclude for nums[i].
- Time complexity worst-case O(2^n) (with pruning often faster). Space is O(n) recursion depth.

## Attempted solution(s)
```python
class Solution:
    def countMaxOrSubsets(self, nums: list[int]) -> int:
        n = len(nums)
        # compute target maximum OR (OR of all elements)
        target = 0
        for x in nums:
            target |= x

        count = 0

        def dfs(i: int, cur_or: int, chosen: bool) -> None:
            nonlocal count
            if cur_or == target:
                # All combinations of remaining elements keep OR == target.
                rem = n - i
                add = 1 << rem  # all subsets of remaining elements
                if not chosen:
                    # exclude the completely empty selection (no element chosen at all)
                    add -= 1
                count += add
                return
            if i == n:
                # reached end and cur_or != target -> nothing to add
                return
            # choose nums[i]
            dfs(i + 1, cur_or | nums[i], True)
            # skip nums[i]
            dfs(i + 1, cur_or, chosen)

        dfs(0, 0, False)
        return count
```
- Approach notes: Compute target OR once. Use DFS with pruning: when cur_or reaches target, add the count of all combinations of remaining elements at once, adjusting to avoid counting the empty subset when nothing has been chosen yet.
- Time complexity: O(2^n) in the worst case (n <= 16 so feasible). Pruning where cur_or reaches target can reduce the explored states.
- Space complexity: O(n) recursion depth (plus O(1) extra).