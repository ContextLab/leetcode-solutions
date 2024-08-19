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

## Several days later...
- Given the problems I've done over the past few days, I'm guessing we're in a dynamic programming block.  So let's see if there's a dynamic programming way of solving this...
- Suppose, given that we've gotten to row $i$, the best possible scores from selecting each column (in that row) are $\left[x_1, x_2, x_3, ..., x_n\right]$.
    - For the first row, the "best scores" are just the values in that first row
- Now how do we optimize the scores for row $i + 1$?
    - Suppose the next row has values $\left[y_1, y_2, y_3, ..., y_n\right]$
    - Suppose also that (when we get to row $i + 1$) we could pick *any* column from row $i$ (whatever would maximize our score)
    - Let's see what the total number of points would be...
        - By the time we get to row $i + 1$, suppose we've computed the maximum number of points we'd get if we chose each column in turn in row $i$.  Let's say the point values are $\left[p_1, p_2, p_3, ..., p_n\right]$.
        - In row $i + 1$, let's iterate across the columns, using the existing `best` values:
            - We want to compute, for each possible column $j$, the updated score we'd get if we pick column $j$ in the current row ($i + 1$)
            - Moving from left to right:
                - If we stay on column 0, and our *previous* choice was also 0, then our score is `best[0] + points[i + 1][0]`
                - If our previous choice was column $j$, then our new score is `best[0] + points[i + 1][0] - j`
                - Let's build up how much we'd add to our score if we move from whatever the best choice in the previous row was to column $j$ in the current row
                - `new_points = [0] * len(points[0])`
                - `new_points[0] = best[0]`...ok, I need to come back to this again 😞...I'm out of time...but what I'm thinking (but not totally sure how to solve) is:
                    - We should track the points we'd get if we move from whatever the best column was in the previous row to each possible column in the current row
                    - I'm not sure if we need a forward/backward pass through `points`, or a left/right pass through each column, or both, or neither
                    - It seems like we should be able to say something like: if we've gotten to column `j`, considering each column up to `j`, let's compute our best possible score
                    - So I guess we should also track the reverse direction, if we've gotten to column `j`, considering each column *after* `j` in turn...and then we'll need to compute the max of both of those options.
