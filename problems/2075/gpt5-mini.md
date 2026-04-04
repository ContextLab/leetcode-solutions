# [Problem 2075: Decode the Slanted Ciphertext](https://leetcode.com/problems/decode-the-slanted-ciphertext/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I remember this problem: encodedText is produced by filling a rows x cols matrix diagonally (top-left to bottom-right) with originalText, then reading the matrix row-wise to produce encodedText. The encodedText length n and rows are given, so the number of columns is n // rows (encodedText is constructed row-wise, so each row contributes exactly cols characters).  
First thought: reconstruct the matrix row-by-row from encodedText, then read the original by traversing diagonals starting at each column of the top row (or equivalently, for each starting column, walk down-right). That should recover the original characters in order. Finally strip trailing spaces (original has no trailing spaces).

## Refining the problem, round 2 thoughts
- Edge cases: empty encodedText -> return "". rows == 1 -> original == encodedText directly.
- We don't actually need to build a 2D array; we can index into the encodedText string directly since the matrix element at (r, c) equals encodedText[r * cols + c].
- For each starting column c from 0 to cols-1, for row r from 0 to rows-1, include character at index r*cols + (c + r) as long as c + r < cols.
- Append characters to a list and join, then rstrip() to remove trailing spaces (originalText does not have trailing spaces).
- Time complexity: O(n) where n = len(encodedText) (we visit each character at most once). Space complexity: O(n) for the output (plus O(1) extra).

## Attempted solution(s)
```python
class Solution:
    def decodeCiphertext(self, encodedText: str, rows: int) -> str:
        # handle trivial cases
        if not encodedText:
            return ""
        if rows == 1:
            return encodedText

        n = len(encodedText)
        cols = n // rows  # number of columns in the matrix
        res_chars = []

        # For each starting column in the top row, walk diagonally down-right
        for start_col in range(cols):
            r = 0
            while r < rows and start_col + r < cols:
                idx = r * cols + (start_col + r)
                res_chars.append(encodedText[idx])
                r += 1

        # originalText has no trailing spaces
        return ''.join(res_chars).rstrip()
```
- Notes:
  - We avoid creating an explicit 2D matrix by computing the index into encodedText directly: matrix[r][c] is at encodedText[r * cols + c].
  - Time complexity: O(n) where n = len(encodedText) because each character is visited at most once in the diagonal traversal.
  - Space complexity: O(n) for the output (res_chars), plus O(1) extra auxiliary space.
  - The final .rstrip() removes any trailing spaces introduced by padding in the encoding process; the problem guarantees originalText has no trailing spaces.