# [Problem 1605: Find Valid Matrix Given Row and Column Sums](https://leetcode.com/problems/find-valid-matrix-given-row-and-column-sums/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- this looks tricky... I don't know of any matrix math tricks that would give us the answer to this outright... but that doesn't mean one doesn't exist...
- what would happen if we tried to iteratively fill in values, sort of like you'd do in a sudoku puzzle? Say I fill in some value in some position. I could subtract that value from the totals for that cell's row and column, and use those to check how much I still need to/can add to each row/column
- one immediate thought is that initializing a matrix full of 0's as a "board" would take $O(n \times m)$ time & space (where $n$ is the number of rows and $m$ is the number of columns, so $O(n^2)$ time in the worst case) before even starting to fill it in, which isn't great.
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
- I wish there were more examples or test cases... maybe I'll try to come up with some:
  ```
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
- okay this happened to be a really helpful example. I can see that if we start with the smallest sum in any row/column (3) and put it in the first column it can fit in (col 0, sum = 34), then switch to using that column's remainder (31), we won't be able to repeat this process even once.




---

- I just thought of another potential algorithm for doing this: what if we initially put all row & column sums in the top row and left column, and then sort of "cascaded" them down through the rest of the rows/column, leaving as many in each as can fit? I'll come back to this...


## Refining the problem, round 2 thoughts

## Attempted solution(s)

```python
class Solution:
    def restoreMatrix(self, rowSum: List[int], colSum: List[int]) -> List[List[int]]:

```
