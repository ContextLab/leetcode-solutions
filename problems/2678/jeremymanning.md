# [Problem 2678: Number of Senior Citizens](https://leetcode.com/problems/number-of-senior-citizens/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- This problem is trivial-- we can just return `sum([int(x[-4:-2]) > 60 for x in details])`

## Refining the problem, round 2 thoughts
- Nothing to refine...

## Attempted solution(s)
```python
class Solution:
    def countSeniors(self, details: List[str]) -> int:
        return sum([int(x[-4:-2]) > 60 for x in details])
```
- Submitting...

![Screenshot 2024-07-31 at 8 17 53 PM](https://github.com/user-attachments/assets/1ae0bd93-96a5-4c70-9e36-15575eb1ecf0)

Solved!
