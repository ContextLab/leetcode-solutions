# [Problem 2379: Minimum Recolors to Get K Consecutive Black Blocks](https://leetcode.com/problems/minimum-recolors-to-get-k-consecutive-black-blocks/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We want k consecutive 'B' characters. Recoloring turns a 'W' into 'B' and costs 1. So for any length-k window, the number of recolors required equals the number of 'W's in that window. Therefore we need to find a length-k substring with the minimum count of 'W'. That suggests a sliding-window or prefix-sum approach. Sliding window is straightforward and O(n) time, O(1) extra space. Edge cases: k == n (only one window), already existing k blacks (answer 0).

## Refining the problem, round 2 thoughts
Implement sliding window: count whites in the first k characters, set that as current and minimum. Then slide window one step at a time, updating the white count by subtracting the leaving char if it's 'W' and adding the entering char if it's 'W'. Keep track of minimum white count seen. That minimum is the answer. Complexity: O(n) time, O(1) space. Constraints are small (n <= 100) so approach is plenty fast. Alternative: prefix sums of whites and query each window in O(1) too, but sliding window is simpler.

## Attempted solution(s)
```python
class Solution:
    def minimumRecolors(self, blocks: str, k: int) -> int:
        n = len(blocks)
        # Count 'W' in the first window of size k
        whites = sum(1 for i in range(k) if blocks[i] == 'W')
        min_whites = whites
        
        # Slide the window from i=k to n-1 (window is [i-k+1 .. i])
        for i in range(k, n):
            if blocks[i] == 'W':
                whites += 1
            if blocks[i - k] == 'W':
                whites -= 1
            if whites < min_whites:
                min_whites = whites
        
        return min_whites
```
- Notes: The solution uses a sliding window counting the number of white blocks in each window of length k; the minimum whites across windows equals the minimum recolors needed.
- Time complexity: O(n), where n = len(blocks), since each character is considered a constant number of times.
- Space complexity: O(1) extra space (only a few counters used).