# [Problem 1937: Maximum Number of Points with Cost](https://leetcode.com/problems/maximum-number-of-points-with-cost/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- One observation is that we're definitely going to need to visit every number at least once, so we're looking at an $O(mn)$ algorithm, at minimum.  So any steps that are $O(mn)$ or faster are "free."  (Here $m$ is the number of columns and $n$ is the number of rows in the matrix.)
- I wonder if we could do something like:
    - In an intial pass through (or maybe this can be done in a first pass...) start by selecting the cell with the maximum point value (ignoring the previous vs. next selections).
    - Then ask: if we shift each value...or...actually, here's a better idea
- What if we do this:
    - If `len(points) == 1` then just return `max(points[0])`
    - Initialize `score = 0`
    - For each row, `i in range(1, len(points))`:
        - Figure out which pick of the *current* row would maximize the score up to and including the *previous* row:
        ```python
        prev_best = -1
        max_score = -1
        for i, a in enumerate(points[i - 1]):
            for j, b in enumerate(points[i]):
                if a + b - abs(i - j) > max_score:
                    max_score = a + b - abs(i - j)
                    prev_best = i        
        ```
        - Then if `i < len(points) - 1`, increment the total score by `points[i - 1][prev_best]`.  Otherwise increment the total score by `max_score`.
        - Side note: I can't re-use `i` as an index-- so for those inner loops we should instead use `j` and `k`, respectively.
    - Now just return `score`

## Refining the problem, round 2 thoughts
- This seems straightforward to implement.  I'm not 100% sure it's *correct* though.
- Walking through this one is going to be annoying, and I'm feeling tired, so as a poor substitute I'm going to intentionally not learn from my previous mistakes and just "test" this by making up a bunch of test problems using random `points` matrices.

## Attempted solution(s)
```python
class Solution:
    def maxPoints(self, points: List[List[int]]) -> int:
        if len(points) == 1:
            return max(points[0])
        score = 0
        for i in range(1, len(points)):
            prev_best = -1
            max_score = -1
            for j, a in enumerate(points[i - 1]):
                for k, b in enumerate(points[i]):
                    next_score = a + b - abs(j - k)
                    if next_score > max_score:
                        max_score = next_score
                        prev_best = j
            if i < len(points) - 1:
                score += points[i - 1][prev_best]
            else:
                score += max_score
        return score
```
- Given test cases pass, which is promising...
- `points = [[91, 0, 35, 50, 71], [77, 35, 95, 3, 2], [67, 61, 81, 76, 42], [19, 89, 29, 80, 68], [88, 74, 62, 99, 6]]`: fail...hmmm
- What about: `points = [[56, 19, 26, 75], [83, 31, 47, 100], [69, 100, 3, 4], [12, 100, 43, 12]]`: ok, also wrong... but this is a little smaller, so easier to debug?
- I think the problem is actually a bit trickier than I am accounting for here:
    - There could be several picks with the same score
    - Choosing one vs. the other may be the same for *this* row (`i - 1`), but that decision could affect *previous* rows' scores.
    - So actually, I need to somehow track all decisions for each new row that would have maximized the score up to that point.  Then somehow I'll need to go back through and figure out which specific pics to make.
- I think I'm too tired to think through this fully, so I'm going to take a break here and revisit tomorrow!

