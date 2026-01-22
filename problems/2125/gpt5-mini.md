# [Problem 2125: Number of Laser Beams in a Bank](https://leetcode.com/problems/number-of-laser-beams-in-a-bank/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem describes a grid of '0'/'1' rows. A beam exists between any two devices if they are on different rows and every row strictly between them has no devices. That means beams are formed only between devices in two rows that are the nearest non-empty rows to each other (ignoring empty rows in between). For any two such rows, every device in the upper row connects to every device in the lower row, so the number of beams contributed by those two rows is simply (#ones in upper row) * (#ones in lower row).

So a straightforward plan: for each row compute number of '1's. Then iterate rows in order, keep the count of the previous non-empty row; when you hit a new non-empty row, add prev_count * current_count to the answer and update prev_count. Empty rows are skipped. This is linear in the size of the input.

## Refining the problem, round 2 thoughts
Edge cases:
- All rows empty => answer 0.
- Only one non-empty row => answer 0.
- Multiple non-empty rows separated by empty rows => still count products only between consecutive non-empty rows.

Alternative approaches:
- Could scan columns or use prefix sums, but unnecessary—simple per-row counts suffice.
- Time complexity minimal: O(m * n) to count ones in every row; space O(1).

Constraints (m,n <= 500) make O(m*n) perfectly fine.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def numberOfBeams(self, bank: List[str]) -> int:
        res = 0
        prev_count = 0
        for row in bank:
            cnt = row.count('1')
            if cnt > 0:
                res += prev_count * cnt
                prev_count = cnt
        return res
```
- Approach: Count ones per row. Maintain previous non-empty row's device count. For each new non-empty row, add product of current count with previous count (these are the beams between these two nearest non-empty rows). Update previous to current.
- Time complexity: O(m * n) where m is number of rows and n is row length (we count ones in each row).
- Space complexity: O(1) extra space (ignoring input storage).
- Important details: Using Python's str.count('1') is simple and efficient enough for given constraints. Empty rows (count == 0) are skipped implicitly.