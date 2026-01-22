# [Problem 1323: Maximum 69 Number](https://leetcode.com/problems/maximum-69-number/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The number only contains digits 6 and 9. To maximize the number by changing at most one digit, I should change a 6 to a 9 because 9 > 6. Changing a 9 to a 6 always decreases the number, so it's never helpful. To maximize the final integer, I should change the leftmost (most significant) 6 to a 9 (if any exist). Converting the number to a string makes it easy to locate and replace the first '6'. There is also a math-based approach (adding 3 * 10^k for the appropriate digit), but string manipulation is straightforward and clear.

## Refining the problem, round 2 thoughts
- Edge case: if there is no '6' in the number (all digits are 9), return the original number.
- Complexity: scanning the string once is O(n) where n is number of digits (n <= 5 here because num <= 10^4, but solution should be general). Converting to/from string uses O(n) extra space. A constant-space math approach is possible by finding the most significant 6 and adding 3 * 10^k; that would be O(n) time and O(1) extra space.
- Simpler and less error-prone: string -> find -> replace -> int.

## Attempted solution(s)
```python
class Solution:
    def maximum69Number(self, num: int) -> int:
        s = list(str(num))
        for i, ch in enumerate(s):
            if ch == '6':
                s[i] = '9'
                break
        return int(''.join(s))
```
- Notes:
  - Approach: Convert the integer to a string, change the first '6' (from left) to '9', and convert back to an integer. If there is no '6', the loop doesn't change anything and the original number is returned.
  - Time complexity: O(n), where n is the number of digits (we scan once and perform O(n) work to rebuild the string).
  - Space complexity: O(n) for the string/list representation. A math-based O(1) extra space solution exists but is more involved; the string approach is simple and clear.