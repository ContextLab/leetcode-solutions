# [Problem 1769: Minimum Number of Operations to Move All Balls to Each Box](https://leetcode.com/problems/minimum-number-of-operations-to-move-all-balls-to-each-box/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share internal step-by-step chain-of-thought reasoning, but here is a concise summary of the intended approach: compute the operation cost to move all balls to each box by using two linear passes. In the first pass accumulate costs coming from the left side (prefix), and in the second pass accumulate costs coming from the right side (suffix). Summing these two contributions gives the final answer for each box in O(n) time and O(1) extra space (besides the output).

## Refining the problem, round 2 thoughts
I won’t provide internal deliberation, but here is a clear refinement and plan:
- A brute-force O(n^2) solution sums distances from each ball to every box; this is fine for small n but unnecessary for n up to 2000.
- Use prefix-sum style accumulation: while scanning left-to-right keep:
  - left_count = number of '1's seen so far (balls to the left of current index),
  - left_ops = total operations to move those left-side balls to the current index.
  - For each index i, left_ops is the contribution from balls left of i.
- Similarly, scan right-to-left to compute right-side contributions and add to the previously stored left-side contributions.
- This yields O(n) time, O(n) output space, and O(1) extra space.

## Attempted solution(s)
```python
class Solution:
    def minOperations(self, boxes: str) -> list[int]:
        n = len(boxes)
        res = [0] * n

        # Left-to-right pass: cost to bring all balls from the left side to i
        left_count = 0  # number of balls seen to the left of (or at) current index so far
        left_ops = 0    # total operations to move those balls to current index
        for i in range(n):
            res[i] = left_ops
            if boxes[i] == '1':
                left_count += 1
            left_ops += left_count

        # Right-to-left pass: cost to bring all balls from the right side to i
        right_count = 0
        right_ops = 0
        for i in range(n - 1, -1, -1):
            res[i] += right_ops
            if boxes[i] == '1':
                right_count += 1
            right_ops += right_count

        return res
```
- Notes about the approach:
  - The left-to-right pass stores for each index i the total cost to move all balls located at indices < i (and effectively handled in left_ops) to i.
  - The right-to-left pass adds the analogous cost from balls located at indices > i.
  - Each pass updates a running count of balls and a running cost; updating the running cost by adding the ball count simulates that every existing ball must move one additional step when we advance the target index by one.
- Complexity:
  - Time: O(n) — two single linear passes over the boxes string.
  - Space: O(n) to store the result array; extra auxiliary space O(1).