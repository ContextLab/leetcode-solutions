# [Problem 1380: Lucky Numbers in a Matrix](https://leetcode.com/problems/lucky-numbers-in-a-matrix/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- Yay, finally a non-tree problem! This seems pretty straightforward
- Native solution: find the min of each row, find the max of each column, return values in both
- But we don't actually have to process every column, just the ones that contain a row min.
  - This would take some additional logic to write, so it may not actually end up being faster
  - If we wanted to add even more logic to further optimize this, we could choose whether to constrain rows based on columns or columns based on rows, depending on which there are more of (the one with fewer is the one we should process each of then use to constrain the other)
- I'll try implementing each of these 3 solutions to see whether the tradeoffs are worth it

## Refining the problem, round 2 thoughts

## Attempted solution(s)

### naive solution

```python
class Solution:
    def luckyNumbers(self, matrix: List[List[int]]) -> List[int]:
        row_mins = {min(row) for row in matrix}
        col_maxes = {max(col) for col in zip(*matrix)}
        return list(row_mins & col_maxes)

```

![](https://github.com/user-attachments/assets/4964fc30-5772-41a0-83b1-d2cceb52f6fb)

Huh, didn't expect that to be that fast.

**Update:** this was a low runtime/high memory outlier. I ran it 4 more times and the mean runtime over 5 runs was **107.8 ms, 16.79 MB memory**.

### optimized solution 1

```python
class Solution:
    def luckyNumbers(self, matrix: List[List[int]]) -> List[int]:
        n_cols = len(matrix[0])
        row_mins = set()
        row_min_ixs = set()
        for row_ix, row in enumerate(matrix):
            row_min_ix = min(range(n_cols), key=row.__getitem__)
            row_min_ixs.add(row_min_ix)
            row_mins.add(row[row_min_ix])
        result = []
        for col_ix in row_min_ixs:
            col_max = max([row[col_ix] for row in matrix])
            if col_max in row_mins:
                result.append(col_max)
        return result
```

![](https://github.com/user-attachments/assets/478db6d7-02b7-498f-abed-e9fc38d59ce3)

Mean over 5 runs: **107.4 ms, 16.90 MB memory**. So really no appreciable difference. Given that, I'm not gonna bother with the third version.
