# [Problem 1605: Find Valid Matrix Given Row and Column Sums](https://leetcode.com/problems/find-valid-matrix-given-row-and-column-sums/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- My first intution here is that the outer product of `rowSum` and `colSum` will tell us the "shape" of the desired matrix, up to a scaling factor.  It's possible we could then normalize the matrix (maybe by dividing by `min(min(rowSum), min(colSum))`?  or the vector lengths?  or the product of vector lengths?...off the top of my head I'm not sure of the right correction factor.  But something like this...maybe?:
```python
import numpy as np

def get_matrix(a, b):
  x = np.outer(a, b)
  return np.round(x / np.sum(x, 1)[0] * a[0])
```
- The problem is that this doesn't work for every case, because of the "all entries are integers" constraint
- It's possible we could compute some sort of correction matrix.  E.g., we could do something like:
    - Change `np.round` to `np.floor` (as an aside, I realize in the submitted solution we can't use `NumPy`...but we could easily implement these functions ourselves)
        - Or...maybe just leave it as `np.round`?
    - Take the sums across the rows (`x`) and columns (`y`) of the result
    - Then take the outer product of `x` and `y`, and add that to the (revised) output of the function above...?
```python
import numpy as np

def get_matrix(a, b):
  x = np.outer(a, b)
  x = np.round(x / np.sum(x, 1)[0] * a[0])

  a2 = a - np.sum(x, 1)
  b2 = b - np.sum(x, 0)

  correction = np.round(np.outer(a2, b2) / max(np.linalg.norm(a2) * np.linalg.norm(b2), 1))
  return x + correction
```
- This doesn't really work either...it's *close* (very close!).  There might be an analytic solution, but I think I'm going to try a different approach instead.
- Brainstorming ideas:
    - Fill in one cell of the matrix randomly and see what else follows...it'd need to be something less than or equal to the minimum row/column sum corresponding to that entry
    - For a given entry, what's the maximum value?  We know that it can't be greater than the sum for its row or column...🤔
    - We could do some sort of iterative approach...get an approximate solution and then correct the entries one at a time?  I think we'd only be off by (up to) 1...🤔
    - I don't think this can be solved recursively (e.g., through some sort of divide and conquer algorithm)
    - What if we use a greedy algorithm?  Something like this:
        - Find the minimum across the row and column sums (`m = min(min(rowSum), min(colSum))`).  Let's say it occurs at `matrix[i][j]`
        - Fill in `matrix[i][j] = m`
        - Now adjust the appropriate entries of `rowSum` and `colSum` to correct for what we've filled in.
    - Will the greedy algorithm work?
        - For the first example, we'd put a 3 in the upper-left cell of the matrix.  Then (after updating) `rowSum = [0, 8]` and `colSum = [1, 7]`.  The matrix is `[[3, -], [-, -]]`.
        - Next (we can ignore the positions we've already updated...hopefully-- note: come back to this) we put a 1 in the next position in the first column.  Now `rowSum = [0, 7]` and `colSum = [0, 7]`.  The matrix is now `[[3, -], [1, -]]`.
        - Next (using the updated row/column sums) we update the first row second column using the updated row sum (0).  Now `rowSum = [0, 7]` (unchanged) and `colSum = [0, 7]` (unchanged).  the matrix is now `[[3, 0], [1, -]]`.
        - Finally, the last entry has to be a 7 since it's the minimum of the row/column sums, excluding already-updated positions.  So the final matrix is `[[3, 0], [1, 7]]`.  (This checks out)
        - Actually...I think we want to just go in order (e.g., across columns, down rows)
        - In general:
            - Just loop through the rows and columns (nested loops)
            - Set each entry to the minimum of the sum for that row/column
            - Then update the target sums by subtracting the value we just entered
        - Questions:
            - Do we need to make multiple iterations (passes)?
            - Will the row or column sums ever have non-zero entries?
            - Can the row or column sums every become negative (which isn't allowed)?

## Refining the problem, round 2 thoughts
- Let's go with the greedy algorithm approach.  It's $O(nm)$ where $n$ is the length of `rowSum` and $m$ is the length of `colSum`.  But I don't think we can hope to do better than this, since we need to return the $n \times m$ matrix at the end anyway.  So at minimum we'll need to fill in each entry of the matrix.
- Let's hold off on the "multiple passes" question
- Will rows or columns every end up with non-zero entries?  Can we ever get negative values?
    - Re: negative values: When we fill in an entry of the matrix at position $(i, j)$, either `rowSum` or `colSum` goes to 0 at the corresponding position.  The other gets updated to something greater than or equal to 0, since by definition the *other* entry had a smaller value.  So we know the sums will never be negative, since the values we're taking the minimums of are always greater than or equal to 0, and the values we're subtracting from the updated row/column sums are always less than or equal to the values at the corresponding entries.
    - Re: non-zero entries: let's suppose that, after going through the full matrix (through all rows/columns) one value in `rowSum` or `colSum` is greater than 0.  Let's call the value $x$.  Hmm...
        - Actually, maybe another way to think about this is: the *total* sum of the values in the final matrix has to be the same, no matter whether you add across the rows (and then add those sums) or whether you add across the columns (and then add those sums).
        - Each time we update an entry, *either* a value of `rowSum` is updated to 0, or a value of `colSum` is updated to 0.  Both vectors' sums (across all entries) are reduced by the same amount (since we subtract the value of the entry to the matrix that we just made).
        - So the sums of `rowSum` and `colSum` are *always* equal, which means that the same total "mass" within each of those vectors has to be distributed across their entries.  So we could never have something like `rowSum = [0, 0, 0]` and `colSum = [10, 10, 10]` (i.e., the entries of `rowSum` are always selected preferentially), since then the sums would be unequal.  So if we had some 0 entries of `rowSum`, the remaining entries would have to divvy up the sum of `colSum` so that the two vectors' sums remained equal.  And that means that at some point some entry of `colSum` will have a smaller value than the corresponding entry of `rowSum`, unless both are 0.
        - So after we go through all of the entries of the matrix, we *must* end up with a sum of 0 in `rowSum` and `colSum`, since every entry in each had to be selected once.
        - This also tells us that we won't need to do multiple passes: after one pass through the full matrix, we're guaranteed to get the desired row and column sums.
- Ok, let's implement this!  I think it'll be relatively straightforward now that we have the key idea...


## Attempted solution(s)
```python
class Solution:
    def restoreMatrix(self, rowSum: List[int], colSum: List[int]) -> List[List[int]]:
        # initialize the matrix to all zeros
        x = [[0 for _ in colSum] for _ in rowSum]

        # go through each row and column, setting x[i][j] to min(rowSum[i], colSum[j]) each time
        for i, r in enumerate(rowSum):
            for j, c in enumerate(colSum):
                x[i][j] = min(rowSum[i], colSum[j])
                rowSum[i] -= x[i][j]
                colSum[j] -= x[i][j]

        return x
```
- Given test cases pass
- Making up another test case with some help from a calculator 🙂: `rowSum = [5,3,8,36,10,50,100,1,7,6,20,5,3], colSum = [1,4,7,9,12,19,94,5,2,10,18,50,1,1,1,20]`: pass
- Ok, this seems fine; submitting...

![Screenshot 2024-07-19 at 11 14 54 PM](https://github.com/user-attachments/assets/7cc9ddfc-1dd8-491d-888e-8411c73fd982)

Solved!  But...slow!  This seems to be my MO 🙃.

