# [Problem 1550: Three Consecutive Odds](https://leetcode.com/problems/three-consecutive-odds/description/)

## Initial thoughts (stream-of-consciousness)
- This seems easy.  I'll keep a running count of consecutive odds.  If an even number is encountered, reset the counter.  If the counter hits 3, return True.  At the end of the list (if the counter has not yet hit 3), return False.

## Attempted solution(s)
```python
class Solution:
    def threeConsecutiveOdds(self, arr: List[int]) -> bool:
        counter = 0
        for x in arr:
            if x %2 == 0:
                counter = 0
            else:
                counter += 1
            if counter == 3:
                return True
        return False
```
- The given test cases pass; the problem is also too simply to have tricky cases
- Submitting...

<img width="657" alt="Screenshot 2024-07-05 at 7 50 37 PM" src="https://github.com/ContextLab/leetcode-solutions/assets/9030494/dfd800db-f1c0-4cc1-8f8e-a02f75521656">

Problem solved!
