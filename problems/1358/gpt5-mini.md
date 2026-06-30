# [Problem 1358: Number of Substrings Containing All Three Characters](https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I will avoid detailed internal step-by-step reasoning, but at a high level:
- The string contains only 'a', 'b', 'c' — that suggests an O(n) sliding-window or two-pointer approach.
- For every left index, find the smallest right index so the substring [left, right] contains all three characters; once it's satisfied, every longer substring starting at left is also valid.
- So we can move right forward until we have all three, add count of valid substrings starting at left, then move left forward and update counts.

## Refining the problem, round 2 thoughts
- Use two pointers left and right, maintain counts for 'a', 'b', 'c'. right will be the exclusive end of the current window.
- When window contains all three characters, the number of valid substrings starting at left is (n - (right-1)) = n - right + 1, because any end index >= right-1 works.
- Move left forward by one (decrement the count for s[left]) and repeat; if the window no longer contains all three, advance right further.
- Time complexity: each index is visited at most twice (once by right, once by left) → O(n).
- Space complexity: O(1) extra space (only counts for 3 characters).

## Attempted solution(s)
```python
class Solution:
    def numberOfSubstrings(self, s: str) -> int:
        n = len(s)
        # counts for 'a', 'b', 'c' mapped to indices 0,1,2
        counts = [0, 0, 0]
        left = 0
        right = 0  # right is exclusive
        res = 0

        def has_all_three() -> bool:
            return counts[0] > 0 and counts[1] > 0 and counts[2] > 0

        while left < n:
            # expand right until window [left, right-1] contains all three or right reaches n
            while right < n and not has_all_three():
                counts[ord(s[right]) - ord('a')] += 1
                right += 1

            # if we have all three, every substring starting at left and ending at any index >= right-1 is valid
            if has_all_three():
                res += n - right + 1
            else:
                # right == n and window still doesn't have all three -> no further valid substrings for larger left
                break

            # move left forward, shrink window from the left
            counts[ord(s[left]) - ord('a')] -= 1
            left += 1

        return res
```
- Approach: two-pointer sliding window maintaining counts of 'a', 'b', 'c'. For each left, move right until the window contains all three; then add the number of valid substrings starting at left (n - right + 1). Increment left and update counts, repeating until left reaches n or it's impossible to get all three.
- Time complexity: O(n) — each character is processed by right at most once and by left at most once.
- Space complexity: O(1) — only a fixed-size counts array is used.