# [Problem 11: Container With Most Water](https://leetcode.com/problems/container-with-most-water/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share internal stream-of-consciousness or step-by-step private reasoning. I can, however, provide a concise, non-sensitive summary of the initial approach:

Summary: The optimal solution uses a two-pointer technique. Place one pointer at the left end and one at the right end. The area is determined by the shorter of the two heights times the width between pointers. To try to increase area, move the pointer at the shorter height inward (because moving the taller pointer cannot increase the limiting height). Repeat until pointers meet, tracking the maximum area seen.

## Refining the problem, round 2 thoughts
Refinement and important notes:
- A brute-force approach checks all pairs (O(n^2)) but is too slow for n up to 10^5.
- Two-pointer method is O(n) time and O(1) space: start left = 0, right = n-1; at each step compute area = min(height[left], height[right]) * (right - left). Update max. Move the pointer at the smaller height inward (left++ if height[left] < height[right], else right--). If equal heights, moving either is fine; typically move one (e.g., right--).
- Edge cases: heights of zero, all equal heights, very large n — method handles these naturally.
- Complexity: O(n) time, O(1) extra space.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxArea(self, height: List[int]) -> int:
        """
        Two-pointer approach:
        - Initialize left pointer at 0 and right pointer at len(height) - 1.
        - Compute area = min(height[left], height[right]) * (right - left).
        - Update max_area.
        - Move the pointer at the smaller height inward (since the limiting height
          is the smaller one; moving the taller won't help increase area).
        - Repeat until left >= right.
        Time: O(n), Space: O(1).
        """
        left, right = 0, len(height) - 1
        max_area = 0

        while left < right:
            h_left = height[left]
            h_right = height[right]
            width = right - left
            area = min(h_left, h_right) * width
            if area > max_area:
                max_area = area

            # Move the pointer at the shorter line inward
            if h_left < h_right:
                left += 1
            else:
                right -= 1

        return max_area
```
- Notes:
  - Approach: Two-pointer greedy-style. By always moving the shorter pointer, we potentially find a taller boundary that can increase area despite the reduced width; moving the taller pointer cannot increase the limiting height.
  - Time complexity: O(n), as each pointer moves inward at most n steps total.
  - Space complexity: O(1) additional space (in-place, only a few variables used).