# [Problem 1380: Lucky Numbers in a Matrix](https://leetcode.com/problems/lucky-numbers-in-a-matrix/description/)

## Initial thoughts (stream-of-consciousness)
- Let's use set comprehensions to compute the minimum values in each row (`row_mins`) and the maximum values in each column (`column_maxes`)
- Then we can just return `list(row_mins.intersect(column_maxes))`

## Refining the problem, round 2 thoughts
- Since every element in the matrix is distinct (per the problem definition), we don't need to deal with the same value potentially appearing in different rows/columns (otherwise we'd also need to track the positions)

## Attempted solution(s)
```python
class Solution:
    def luckyNumbers (self, matrix: List[List[int]]) -> List[int]:
        # compute the minimum for each row
        row_mins = {min(r) for r in matrix}

        # compute the maximum for each column
        n = len(matrix[0])
        column_maxes = {max([r[i] for r in matrix]) for i in range(n)}

        # return a list of the set intersection between the mins and maxes
        return list(row_mins.intersection(column_maxes))
```
- Given test cases pass
- I don't think there are other special cases we need to account for that this solution won't cover; submitting...

![Screenshot 2024-07-18 at 8 26 55 PM](https://github.com/user-attachments/assets/e855d252-0c1d-4d8c-afba-fdcbde8e319f)

Solved!
