# [Problem 1105: Filling Bookcase Shelves](https://leetcode.com/problems/filling-bookcase-shelves/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We must place books in the given order onto shelves of limited width. We can choose how many consecutive books to put on each shelf, and the shelf height is the maximum height among those books. We want to minimize the total sum of shelf heights.

This smells like dynamic programming because the decision of where to break between shelves depends on previous choices and we must consider prefixes of the list. A greedy approach (e.g., always pack as many as possible on a shelf) can fail because a taller book later might force a different partition.

So consider dp[i] = minimum total height to place the first i books. To compute dp[i], consider the last shelf contains books j..i-1 for some j < = i-1, as long as their total thickness <= shelfWidth. The cost then is dp[j] + max(height of books j..i-1). Try all possible j (scanning backwards to accumulate width and max height). This yields an O(n^2) DP which should be fine for n <= 1000.

## Refining the problem, round 2 thoughts
We should scan backward from i-1 to 0, accumulating width and max height. As soon as width exceeds shelfWidth we can break because earlier j will only increase width. Initialize dp[0] = 0 and dp[i] = inf for others.

Edge cases:
- All books fit in one shelf => dp[n] equals max height of all books.
- Single book => dp[1] = height of that book.
- widths equal shelfWidth or some thickness = shelfWidth: still fine since each book individually can occupy a shelf.

Complexity:
- Time: O(n^2) in worst case because for each i we might scan back to 0.
- Space: O(n) for dp.

Alternative: top-down memoization yields same complexity; bottom-up is straightforward.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minHeightShelves(self, books: List[List[int]], shelfWidth: int) -> int:
        n = len(books)
        # dp[i] = minimum height to place first i books (books[0..i-1])
        dp = [float('inf')] * (n + 1)
        dp[0] = 0

        for i in range(1, n + 1):
            width_acc = 0
            max_height = 0
            # try to place books[j..i-1] on the last shelf, scanning j backwards
            for j in range(i - 1, -1, -1):
                thickness, height = books[j]
                width_acc += thickness
                if width_acc > shelfWidth:
                    break
                if height > max_height:
                    max_height = height
                dp[i] = min(dp[i], dp[j] + max_height)

        return dp[n]
```
- Notes:
  - Approach: bottom-up dynamic programming where dp[i] is the min total height for first i books. For each i, scan backward to consider every possible start j of the last shelf while maintaining accumulated width and max height to compute dp[i] = min(dp[j] + max_height_for_books_j_to_i-1).
  - Time complexity: O(n^2) in the worst case (n = number of books). Each i may scan up to i previous books.
  - Space complexity: O(n) for the dp array.
  - Implementation details: scanning backwards allows early termination when accumulated width exceeds shelfWidth which saves work in many instances.