# [Problem 955: Delete Columns to Make Sorted II](https://leetcode.com/problems/delete-columns-to-make-sorted-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to delete as few columns as possible so that the remaining rows (strings) are in non-decreasing lexicographic order. Columns can be removed in any set, but deletions affect all rows. A brute-force try-all-subsets of columns is impossible (2^m). A greedy approach scanning columns left-to-right feels natural because lexicographic order compares from left to right: the first differing column determines order between two rows.

So iterate columns from left to right and decide whether to keep or delete each column. If keeping a column would create a violation (some row i > row i+1 considering seen columns so far), then we must delete that column. If keeping it doesn't violate order, we can use it to finalize some row-pair ordering (if character at column makes row i < row i+1 strictly, that pair is permanently ordered and subsequent columns don't need to check that pair). Maintain an array of "confirmed" pairs between consecutive rows.

This is a known greedy solution: for each column, check pairs that are not yet confirmed; if any pair has char_a > char_b at this column, delete the entire column (count +1) and don't update confirmed pairs; otherwise update confirmed pairs where char_a < char_b. Stop early if all pairs become confirmed.

## Refining the problem, round 2 thoughts
Edge cases:
- n == 1 -> already sorted, answer = 0.
- Strings of length 1 or all columns decreasing -> may need to delete all columns.
- We must ensure when a column is deleted we do not change confirmed pairs; we simply skip the column.
- Complexity: we check each column and for each column we may inspect up to n-1 pairs, so O(n*m) time and O(n) extra space for the flags. This fits constraints (n, m <= 100).

Alternative: dynamic programming or building minimal set of columns to keep, but greedy is simpler and optimal because lexicographic comparison is left-to-right—the earliest difference matters—so once a pair is confirmed in order, later columns cannot undo it.

## Attempted solution(s)
```python
class Solution:
    def minDeletionSize(self, strs: list[str]) -> int:
        if not strs:
            return 0
        n = len(strs)
        m = len(strs[0])
        # If only one string, already sorted
        if n <= 1:
            return 0

        # confirmed[i] means strs[i] <= strs[i+1] is already guaranteed by kept columns
        confirmed = [False] * (n - 1)
        deletions = 0

        for col in range(m):
            # Check if keeping this column would cause any violation
            bad = False
            for i in range(n - 1):
                if not confirmed[i] and strs[i][col] > strs[i + 1][col]:
                    bad = True
                    break
            if bad:
                deletions += 1
                # delete this column, don't update confirmed, move to next column
                continue

            # No violation: update confirmed pairs where this column strictly orders them
            all_confirmed = True
            for i in range(n - 1):
                if not confirmed[i]:
                    if strs[i][col] < strs[i + 1][col]:
                        confirmed[i] = True
                    else:
                        # still not confirmed; keep checking others
                        all_confirmed = False
            if all_confirmed:
                # all pairs are confirmed, we can stop early
                break

        return deletions
```
- Notes about the approach:
  - Greedy left-to-right scanning of columns. If any unconfirmed adjacent pair would be out of order by keeping the column, delete that column.
  - If the column does not cause any violation, use it to mark pairs that become strictly ordered (strs[i][col] < strs[i+1][col]) as confirmed.
  - Early exit when all adjacent pairs are confirmed.
- Complexity:
  - Time: O(n * m) where n = number of strings and m = length of each string (we inspect each column and up to n-1 adjacent pairs).
  - Space: O(n) extra for the confirmed flags (or O(1) additional beyond input if you reuse input memory, but we use a small boolean array).