# [Problem 757: Set Intersection Size At Least Two](https://leetcode.com/problems/set-intersection-size-at-least-two/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the smallest set of integers such that every interval contains at least two of those integers. This smells like a greedy covering problem. If I process intervals by their right endpoints (earliest finishing first) I can try to place points as far right as possible so they help future intervals too. For each interval I want to know how many of the already chosen points fall inside it. If none, I should add two points inside the interval (preferably the two largest possible, i.e., r-1 and r). If exactly one, add one more (again put it at r). If two or more, nothing to do.

I remember one tricky part: when intervals share the same right endpoint, the ordering by start matters (we should process intervals with larger starts first when ends tie), so that we don't mistakenly think an already chosen point at r suffices for a tighter interval that requires two distinct points.

So approach: sort by end ascending, and for equal ends by start descending, maintain two largest chosen points a (second last) and b (last), and update as we scan.

## Refining the problem, round 2 thoughts
- Sorting: key = (end, -start).
- Maintain two latest chosen points a < b (initialize to very small values). For interval [l, r]:
  - If l > b: none of a or b in interval -> pick r-1 and r (ans += 2), set a = r-1, b = r.
  - Else if l > a: exactly one (b) in interval -> pick r (ans += 1), set a = b, b = r.
  - Else: a and b both in interval -> nothing to do.
- Edge cases:
  - intervals length up to 3000 so sorting O(n log n) is fine.
  - r-1 will always be >= l? Given start < end, r-1 >= l can be equal or greater; r-1 could be < l if interval length is 1? Actually start < end implies at least two integers, e.g., [1,2] => r-1 == 1 == l. So r-1 always >= l.
  - Sorting by start descending for same end prevents incorrect reuse of existing r when we need two distinct points inside tight intervals with same end.
- Complexity: sorting O(n log n), single pass O(n), space O(1) extra.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def intersectionSizeTwo(self, intervals: List[List[int]]) -> int:
        # Sort by end ascending, and for equal end sort by start descending
        intervals.sort(key=lambda x: (x[1], -x[0]))
        
        # a = second-last chosen point, b = last chosen point
        a = -10**18
        b = -10**18
        ans = 0
        
        for l, r in intervals:
            if l > b:
                # neither a nor b is in [l, r]: pick r-1 and r
                ans += 2
                a = r - 1
                b = r
            elif l > a:
                # only b is in [l, r]: pick r
                ans += 1
                a = b
                b = r
            else:
                # both a and b are in [l, r]: nothing to do
                continue
        
        return ans
```
- Notes:
  - Greedy idea: always choose points as far to the right as possible (r-1 and r) so they maximize reuse by later intervals.
  - Sorting by (end asc, start desc) ensures correctness when multiple intervals share the same end.
  - Time complexity: O(n log n) due to sorting, where n = number of intervals.
  - Space complexity: O(1) extra (besides input and sorting).