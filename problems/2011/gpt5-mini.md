# [Problem 2011: Final Value of Variable After Performing Operations](https://leetcode.com/problems/final-value-of-variable-after-performing-operations/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is straightforward: each operation is either an increment or decrement of X by 1. We start at 0 and apply each operation in order. The operations are strings like "++X", "X++", "--X", "X--". The simplest approach is to iterate through the list and adjust a counter accordingly.

I notice every operation string has length 3 and the middle character indicates the operation: '+' for increment, '-' for decrement. So instead of comparing full strings or using startswith, checking the middle character is concise and efficient.

I might also consider counting occurrences of increment operations versus decrement operations and returning the difference, but a single pass updating a counter is simplest and clear.

## Refining the problem, round 2 thoughts
Edge cases: operations length is between 1 and 100 per constraints, so no empty list; but even if empty, returning 0 would be correct. Strings are guaranteed to be one of the four valid forms, so checking op[1] is safe (always present).

Alternative solutions:
- Use operations.count("++X") + operations.count("X++") minus decrement counts (two counts approach).
- Use a generator expression sum(1 if '+' in op else -1 for op in operations).
Both are O(n) time; the op[1] check is slightly faster and uses O(1) extra space.

Time complexity: O(n) where n = len(operations).
Space complexity: O(1) extra space.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def finalValueAfterOperations(self, operations: List[str]) -> int:
        """
        Compute the final value of X after performing the given operations.
        Each operation is one of: "++X", "X++", "--X", "X--".
        The middle character determines the operation: '+' => increment, '-' => decrement.
        """
        x = 0
        for op in operations:
            # op is guaranteed to be one of the four valid forms, length 3
            if op[1] == '+':
                x += 1
            else:
                x -= 1
        return x
```
- Notes:
  - Approach: single-pass iteration, inspect op[1] to decide increment vs decrement.
  - Time complexity: O(n), where n is number of operations.
  - Space complexity: O(1) extra space.
  - Implementation detail: op[1] check is safe given problem constraints (each string has length 3 and valid characters). Alternative readable options include checking for '+' in op or counting occurrences of increment/decrement patterns.