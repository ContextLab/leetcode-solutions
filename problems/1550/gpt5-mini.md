# [Problem 1550: Three Consecutive Odds](https://leetcode.com/problems/three-consecutive-odds/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to check whether there exist three numbers in a row that are all odd. The simplest idea is to scan the array and maintain a running count of consecutive odd numbers; when I see an odd, increment the count; when I see an even, reset the count to zero. If the count ever reaches 3, return True. Alternatively I could check every window of size 3 and test the parity of each of the three elements, but that is effectively the same work. The array size is at most 1000, so an O(n) scan is trivial. Watch out for small arrays (length < 3) — immediately return False.

## Refining the problem, round 2 thoughts
Edge cases:
- If arr length < 3, answer is False.
- All odd or all even sequences are handled naturally by the counter approach.
Alternative approaches: sliding-window using sum of parities or checking arr[i]%2 for i..i+2. Both are O(n) time and O(1) space. The counter approach is simpler and avoids extra indexing concerns.
Time complexity: O(n) where n = len(arr). Space complexity: O(1) extra space.

## Attempted solution(s)
```python
class Solution:
    def threeConsecutiveOdds(self, arr: list[int]) -> bool:
        consecutive = 0
        for x in arr:
            if x % 2 == 1:
                consecutive += 1
                if consecutive == 3:
                    return True
            else:
                consecutive = 0
        return False
```
- Notes:
  - Approach: single pass, maintain a counter of consecutive odd numbers; reset on even, return True when counter reaches 3.
  - Time complexity: O(n), where n is the length of arr (each element visited once).
  - Space complexity: O(1) extra space (only an integer counter).
  - Implementation detail: Using x % 2 == 1 to check oddness works for the given constraints (positive integers). For general integers, x & 1 or x % 2 != 0 are also fine.