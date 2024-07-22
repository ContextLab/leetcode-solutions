# [Problem 2418: Sort the People](https://leetcode.com/problems/sort-the-people/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- I think this is just a one-liner...I'm just going to code it

## Attempted solution(s)
```python
class Solution:
    def sortPeople(self, names: List[str], heights: List[int]) -> List[str]:
        return [x[0] for x in sorted(zip(names, heights), key=lambda p: p[1], reverse=True)]
```
- Given test cases pass
- Submitting...

![Screenshot 2024-07-21 at 10 34 36 PM](https://github.com/user-attachments/assets/0f148d81-5308-470a-9c39-233e40716304)

Solved!
