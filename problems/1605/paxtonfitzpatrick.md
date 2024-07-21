# [Problem 1605: Find Valid Matrix Given Row and Column Sums](https://leetcode.com/problems/find-valid-matrix-given-row-and-column-sums/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- this looks tricky... I don't know of any matrix math tricks that would give us the answer to this outright... but that doesn't mean one doesn't exist...
- what would happen if we tried to iteratively fill in values, sort of like you'd do in a sudoku puzzle? Say I fill in some value in some position. I could subtract that value from the totals for that cell's row and column, and use those to track how much I still need to/can add to each row/column
- one immediate thought is that initializing a matrix full of 0's as a "board" would take $O(n \times m)$ time (where $n$ is the number of rows and $m$ is the number of columns, so $O(n^2)$ time in the worst case) before even starting to fill it in, which isn't great.
- could I build up the rows and columns as I go instead? That'd require starting with the first row/column, which I don't know if I necessarily want to do... I suppose I *could* just stick values in the first row/column and then adjust whatever I have to as I go, and I think I'll probably have to do some amount of that anyway... but I feel like that's something I'll want to minimize as much as possible cause those edits will cascade through the rest of the matrix and be complicated and time-consuming to deal with. So just choosing initial values/positions without some sort of "rule" for deciding where to put them seems like a bad plan. So for now I guess I'll just eat that $O(n \times m)$ cost...
- so then what could serve as a "rule" for placing values initially?
- if there are any 0's in the rows or columns, that's basically a freebie because I'll know for certain that entire row/column is 0's
- another thing is if I'm subtracting the value I place in a particular cell from its row and column sums, the max value I can place in that cell is the smaller of its row sum and column sum cause I don't want those to go negative
- okay, in both of the examples, the first row's sum is placed in a single cell, with 0s in all other columns. And the cell it's placed in is the column with the smallest sum. I feel like this might be hinting at an algorithm for filling the matrix in...
- Actually, I don't think it's that they're the first rows' sums that matters, I think it's that they're the smallest sums of any row -- *or* any column. That way subtracting it from the smallest sum of the other dimension will leave a non-negative value.
- It looks like those matrices could've been filled in as:
  - find the smallest sum of any row or column. I think we're basically going to be switching back and forth between considering rows/columns, so let's say the smallest value is a row sum.
  - place it in the cell with the smallest column sum
  - subtract that value from the row and column sums
  - take the remaining value of that column's sum and place it in the first availble row it can "fit" in
    - a "row it can fit in" is a row whose remaining sum value is greater than or equal to that remaining column sum value
  - subtract that value from the sums of the row and column it was placed in and repeat
- What happens if we run into a situation where we can't place the full remaining value in any one row(/column) of the current column(/row)? Does that indicate we should divide it across multiple cells within that same column(/row)?
- oh hmmmm... maybe it's not that you place the remaining value in the *first* row/column (i.e., from the top or left) that it can fit in, but the row/column with the smallest remaining value >= it
- also, maybe it's not that you switch back and forth between rows & columns, but that the smallest remaining sum just happened to in those examples (or that it'll tend to, if you've just subtracted the smallest sum from one dimension from the smallest sum in the other?)
- I think choosing the smallest sum of either dimension is the only way to ensure that it'll fit in some row and column each time -- it has to not only be smaller than all other sums along the same dimension but also smaller than the smallest sum along the other dimension
- Also importantly, "smallest" really needs to be "smallest non-zero", since any rows/columns with "remaining sums" of 0 are already full.
- But which rule do we use to choose where to place it? I wish there were more examples or test cases... maybe I'll try to come up with some:
  ```python
  # given some random matrix:
  [[18,  0, 5],
   [ 3,  6, 4],
   [ 2,  1, 0],
   [11, 11, 0],
   [ 0,  4, 5]]
  rowSum = [23, 13, 3, 22, 9]
  colSum = [34, 22, 14]
  # start with an empty matrix of len(rowSum) x len(colSum)
  [[0, 0, 0],
   [0, 0, 0],
   [0, 0, 0],
   [0, 0, 0],
   [0, 0, 0]]
  # and try to fill it in:
  ```
- okay this happened to be a really helpful example. I can see that if we start with the smallest sum in any row/column (3) and put it in the first column it can fit in (col 1, sum = 34), then switch to using that column's remainder (31), we won't be able to repeat this process even once. So that's some evidence we should use the smallest remaining sum each time.
- Let's try iteratively filling in the matrix by choosing the smallest remaining sum and placing it in the first cell of that row/column it can fit into:
  ```python
  # smallest sum: 3 (row 3). First col it can fit in is col 1
  [[0, 0, 0],
   [0, 0, 0],
   [3, 0, 0],
   [0, 0, 0],
   [0, 0, 0]]
  # new rowSum: [23, 13, 0, 22, 9]
  # new colSum: [31, 22, 14]

  # smallest sum: 9 (row 5). First col it can fit in is col 1
  [[0, 0, 0],
   [0, 0, 0],
   [3, 0, 0],
   [0, 0, 0],
   [9, 0, 0]]
  # new rowSum: [23, 13, 0, 22, 0]
  # new colSum: [22, 22, 14]

  # smallest sum: 13 (row 2). First col it can fit in is col 1
  [[ 0, 0,  0],
   [13, 0,  0],
   [ 3, 0,  0],
   [ 0, 0,  0],
   [ 9, 0,  0]]
  # new rowSum: [23, 0, 0, 22, 0]
  # new colSum: [9, 22, 14]

  # smallest sum: 9 (col 1). First row it can fit in is row 1
  [[ 9, 0,  0],
   [13, 0,  0],
   [ 3, 0,  0],
   [ 0, 0,  0],
   [ 9, 0,  0]]
  # new rowSum: [14, 0, 0, 22, 0]
  # new colSum: [0, 22, 14]

  # smallest sum: 14 (row 1)... also col 3.... but I don't think it matters which we choose?
  # First col it can fit in is col 2
  [[ 9, 14,  0],
   [13,  0,  0],
   [ 3,  0,  0],
   [ 0,  0,  0],
   [ 9,  0,  0]]
  # new rowSum: [0, 0, 0, 22, 0]
  # new colSum: [0, 8, 14]

  # smallest sum: 8 (col 2). First row it can fit in is row 4
  [[ 9, 14,  0],
   [13,  0,  0],
   [ 3,  0,  0],
   [ 0,  8,  0],
   [ 9,  0,  0]]
  # new rowSum: [0, 0, 0, 14, 0]
  # new colSum: [0, 0, 14]

  # smallest sum: 14 (row 4) (also col 3). First col it can fit in is col 3
  [[ 9, 14,  0],
   [13,  0,  0],
   [ 3,  0,  0],
   [ 0,  8, 14],
   [ 9,  0,  0]]
  # new rowSum: [0, 0, 0, 0, 0]
  # new colSum: [0, 0, 0]
  ```
- cool, that seems to have worked! It didn't give us back the original matrix, but the new one is also valid. I think this is a good sign, and also the algorithm is pretty straightforward, so I'm gonna try implementing this.

---

- I just thought of another potential algorithm for doing this: what if we initially put all row & column sums in the top row and left column, and then sort of "cascaded" them down through the rest of the rows/column, leaving as many in each as can fit? Maybe if my first idea doesn't work I'll come back to this...


## Refining the problem, round 2 thoughts

- There are some cases where it might be worth short-circuiting because they have simple solutions:
  - length of both `rowSum` and `colSum` is 1
    - just return `[[rowSum[0]]]`
  - length of `rowSum` (but not `colSum`) is 1
    - return `[colSum]`
  - length of `colSum` (but not `rowSum`) is 1
    - return `[[i] for i in rowSum]`
- Also, since I'll need to repeatedly check for the smallest non-zero value across both row and column sums, I think I'm best off combining them into a single list and then just checking for the minimum value in that list each time.
  - also (it'll make the variable names a little misleading so I'd never do this IRL, but) since I'll just be working with that list and won't need the original `rowSum` and `colSum` lists, I could just extend `rowSum` with `colSum` rather than creating a new list to save some memory

## Attempted solution(s)

```python
class Solution:
    def restoreMatrix(self, rowSum: List[int], colSum: List[int]) -> List[List[int]]:
        n_rows = len(rowSum)
        n_cols = len(colSum)
        matrix = [[0] * n_cols for _ in range(n_rows)]
        rowsums_colsums = rowSum + colSum

        while True:
            # get min non-zero sum in row/column sums
            try:
                min_sum = min(filter(None, rowsums_colsums))
            except ValueError:
                # if no non-zero sums remain, the matrix is filled in
                return matrix
            # get its index
            min_sum_ix = rowsums_colsums.index(min_sum)
            # figure out whether it's a row or column sum (without membership
            # check since that's O(n) for a list)
            if min_sum_ix > n_rows - 1:
                # min sum is a column sum
                col_ix = min_sum_ix - n_rows
                for row_ix, row_sum in enumerate(rowSum):
                    if row_sum >= min_sum:
                        matrix[row_ix][col_ix] = min_sum
                        new_row_sum = rowSum[row_ix] - min_sum
                        rowSum[row_ix] = new_row_sum
                        rowsums_colsums[row_ix] = new_row_sum
                        colSum[col_ix] = 0
                        rowsums_colsums[min_sum_ix] = 0
                        break
            else:
                # min sum is a row sum
                for col_ix, col_sum in enumerate(colSum):
                    if col_sum >= min_sum:
                        matrix[min_sum_ix][col_ix] = min_sum
                        new_col_sum = colSum[col_ix] - min_sum
                        colSum[col_ix] = new_col_sum
                        rowsums_colsums[col_ix + n_rows] = new_col_sum
                        rowSum[min_sum_ix] = 0
                        rowsums_colsums[min_sum_ix] = 0
                        break
```

![](https://github.com/user-attachments/assets/c54134c9-7dfd-4ad0-9f41-0f462aa808b7)

Yay it worked! Now let's try to optimize it a bit by incorporating the ideas in [**Refining the problem, round 2 thoughts**](#refining-the-problem-round-2-thoughts), combining/removing some duplicate/unused variables, and avoiding slicing the list where possible.

```python
class Solution:
    def restoreMatrix(self, rowSum: List[int], colSum: List[int]) -> List[List[int]]:
        if (n_rows := len(rowSum)) == 1:
            if len(colSum) == 1:
                return [[rowSum[0]]]
            return [colSum]
        if len(colSum) == 1:
            return [[s] for s in rowSum]

        matrix = [[0] * len(colSum) for _ in range(n_rows)]
        rowSum.extend(colSum)

        while True:
            try:
                min_sum = min(filter(None, rowSum))
            except ValueError:
                return matrix

            min_sum_ix = rowSum.index(min_sum)
            if min_sum_ix < n_rows:
                search_ix = n_rows
                while rowSum[col_ix] < min_sum:
                    search_ix += 1
                matrix[min_sum_ix][search_ix-n_rows] = min_sum
                rowSum[search_ix] -= min_sum
                rowSum[min_sum_ix] = 0
            else:
                for search_ix, row_sum in enumerate(rowSum):
                    if row_sum >= min_sum:
                        matrix[search_ix][min_sum_ix-n_rows] = min_sum
                        rowSum[search_ix] -= min_sum
                        rowSum[min_sum_ix] = 0
                        break
```

![](https://github.com/user-attachments/assets/0cb84df4-8132-4316-88b6-81ac68e05090)

So that really only gave a small improvement in runtime and memory. I guess that could be because the short-circuit cases I added are situations where the function would return pretty quickly anyway, so they don't save much time in those cases and add some overhead to the others.
