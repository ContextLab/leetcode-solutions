# [Problem 3754: Concatenate Non-Zero Digits and Multiply by Sum I](https://leetcode.com/problems/concatenate-non-zero-digits-and-multiply-by-sum-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to form x by concatenating all non-zero digits of n in the original order, then compute sum of digits of x and return x * sum. The sum of digits of x is simply the sum of the non-zero digits of n (since x is made only of those digits). The simplest route is to treat n as a string, filter out '0', parse the result as an integer (or 0 if empty), and sum the characters. Alternatively we could do arithmetic digit extraction, but that often reverses order unless we collect digits and reverse — string approach is simpler and clear. Edge case: n = 0 or n contains only zeros -> x = 0, sum = 0, product = 0.

## Refining the problem, round 2 thoughts
- Using string operations: O(d) time where d is digit count (≤ 10 for constraints) and O(d) extra space for the filtered list/string.
- Using arithmetic: we could build x by iterating digits from most-significant to least-significant — easier via string. If we used mod 10 extraction, we'd get digits in reverse, so we'd need an extra reversal step or build x in reversed manner and then reverse it again — more work for little benefit.
- Edge cases: n = 0 -> return 0. Large n not a concern due to constraint n ≤ 1e9.
- Complexity is trivial: linear in digit count; space linear in digit count.

## Attempted solution(s)
```python
class Solution:
    def concatenatedProduct(self, n: int) -> int:
        """
        Build x by concatenating non-zero digits of n in original order.
        Then compute sum of digits of x (which equals sum of those non-zero digits)
        and return x * sum.
        """
        s = str(n)
        filtered = [ch for ch in s if ch != '0']
        if not filtered:
            return 0
        x_str = ''.join(filtered)
        x = int(x_str)
        digit_sum = sum(int(ch) for ch in x_str)
        return x * digit_sum

# Example usage:
# sol = Solution()
# print(sol.concatenatedProduct(10203004))  # 12340
# print(sol.concatenatedProduct(1000))     # 1
```

- Notes about the solution:
  - Approach: convert n to string, filter out '0' characters, form x from the filtered string, compute digit sum, multiply.
  - Time complexity: O(d) where d is number of digits in n (d ≤ 10 for given constraints), so effectively O(1).
  - Space complexity: O(d) for the filtered string/list.
  - Handles edge cases: if there are no non-zero digits (e.g., n = 0 or n = 000), we return 0.