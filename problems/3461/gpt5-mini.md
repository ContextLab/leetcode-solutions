# [Problem 3461: Check If Digits Are Equal in String After Operations I](https://leetcode.com/problems/check-if-digits-are-equal-in-string-after-operations-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem describes repeatedly replacing the string of digits with the pairwise sums (mod 10) of consecutive digits until exactly two digits remain, then checking whether those two are equal.

My immediate thought: just simulate the process. Convert the string to a list of integers, then repeatedly build the next list by summing adjacent pairs modulo 10 until length == 2. Constraints are small (length up to 100) so an O(n^2) simulation (because lengths shrink each step) is perfectly fine.

I also note there's no tricky edge case: input length >= 3 and characters are digits. There's no need for a mathematical shortcut here.

## Refining the problem, round 2 thoughts
- Implementation detail: working with integer lists is simpler than string manipulation because of modulo arithmetic.
- Termination: loop until the list length is 2.
- Complexity: each reduction step costs O(current length), and lengths form n+(n-1)+...+3 = O(n^2). With n <= 100 this is trivial.
- Memory: we can reuse lists (build a new one each step) or try in-place updates, but building a new list is clear and efficient enough.
- Return True if the final two integers are equal, otherwise False.

No special corner cases beyond the described behavior.

## Attempted solution(s)
```python
class Solution:
    def isSameAfterOperations(self, s: str) -> bool:
        """
        Simulate the described operation: repeatedly replace the sequence by
        pairwise sums modulo 10 until only two digits remain, then check equality.
        """
        arr = [ord(c) - ord('0') for c in s]
        while len(arr) > 2:
            arr = [(arr[i] + arr[i+1]) % 10 for i in range(len(arr) - 1)]
        return arr[0] == arr[1]
```
- Notes:
  - Approach: straightforward simulation using a list of integers and list comprehension to compute the next sequence.
  - Time complexity: O(n^2) in the worst case (summing over shrinking lengths), where n = len(s). With n <= 100 this is fine.
  - Space complexity: O(n) for the list of digits (plus smaller temporary lists during each iteration).