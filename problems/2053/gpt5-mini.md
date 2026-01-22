# [Problem 2053: Kth Distinct String in an Array](https://leetcode.com/problems/kth-distinct-string-in-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to find the k-th string that appears exactly once in the array, considering the original order. First thing that comes to mind is counting occurrences (one pass) and then scanning the array in order to pick out strings with count == 1 until I reach the k-th such string. I could also try keeping an ordered map of counts (OrderedDict) but a simple counter + second pass is straightforward and O(n). Edge cases: fewer than k distinct strings -> return "". Strings are short so hashing/counting is cheap.

## Refining the problem, round 2 thoughts
Two-pass approach:
1. Count frequency of each string (hash map / Counter).
2. Iterate arr in order and decrement k each time we see a string with freq == 1; when k reaches 0 return the string.
If finished loop without finding k distinct strings return "".

Time complexity: O(n * L) where L is average string length (hashing/comparisons); given constraints L <= 5 this is effectively O(n). Space: O(n) for the frequency map. This is simple, clear, and efficient. No tricky corner cases besides returning "" when not enough distinct strings.

## Attempted solution(s)
```python
from collections import Counter
from typing import List

class Solution:
    def kthDistinct(self, arr: List[str], k: int) -> str:
        freq = Counter(arr)
        for s in arr:
            if freq[s] == 1:
                k -= 1
                if k == 0:
                    return s
        return ""
```
- Approach: Count frequencies with Counter, then scan arr in original order and return the k-th string whose frequency is 1.
- Time complexity: O(n * L) for n = len(arr) and L = average string length (hashing costs). With L <= 5 by constraints this is effectively O(n).
- Space complexity: O(n) for the frequency map.
- Implementation details: Using Counter from collections keeps the code concise and clear; iterating arr preserves original order as required. If there are fewer than k distinct strings the function returns an empty string "".