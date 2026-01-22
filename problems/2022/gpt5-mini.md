# [Problem 2022: Convert 1D Array Into 2D Array](https://leetcode.com/problems/convert-1d-array-into-2d-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to take a flat list and pack it into m rows and n columns, preserving order. The immediate check is whether the total number of elements equals m * n — if not, return an empty 2D list. If the lengths match, we can slice the original array into consecutive chunks of size n to form each row. Alternatively, we can iterate with an index and build each row by appending n elements. This is straightforward and linear in the number of elements.

## Refining the problem, round 2 thoughts
Edge cases:
- original length not equal to m * n -> return []
- minimal sizes (m or n equals 1) still works with the same logic
- large m and n but small original length -> early mismatch check avoids extra work

Performance:
- Time complexity should be O(len(original)) since we process each element exactly once.
- Space complexity is O(m * n) to build the output (required by the problem).
Implementation choices:
- Using list slicing in a list comprehension is concise: [original[i*n:(i+1)*n] for i in range(m)]
- Or use an index pointer and append elements to rows to avoid repeated slice allocations if desired. Both are fine; slicing overall is still linear.

## Attempted solution(s)
```python
class Solution:
    def construct2DArray(self, original: list[int], m: int, n: int) -> list[list[int]]:
        # If sizes don't match, it's impossible
        if len(original) != m * n:
            return []
        # Use slicing to create each row of length n
        return [original[i * n:(i + 1) * n] for i in range(m)]
```
- Notes:
  - Approach: check length equality, then partition the list into m chunks of size n in order.
  - Time complexity: O(len(original)) = O(m * n) since each element is visited/used once.
  - Space complexity: O(m * n) for the returned 2D array (plus negligible overhead for slices).