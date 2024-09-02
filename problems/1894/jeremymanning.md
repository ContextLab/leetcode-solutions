# [Problem 1894: Find the Student that Will Replace the Chalk](https://leetcode.com/problems/find-the-student-that-will-replace-the-chalk/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- I think there are basically two steps to this:
    - First, skip ahead to the last "cycle" through the students.  To do this, we can set `k %= sum(chalk)`.
    - Then we just need to loop through students one at a time until the amount of chalk used is greater than `k`.  Or we could also just subtract `chalk[i]` as we loop through each student `i`, and then return `i` when `k` dips below 0.  This might be slightly better, since it means we can use one fewer variable.

## Refining the problem, round 2 thoughts
- I don't see any obvious edge cases here; I think I'm good to implement this
- Not totally sure why this is a "medium" problem; it seems pretty straightforward.  Maybe I'm missing something...

## Attempted solution(s)
```python
class Solution:
    def chalkReplacer(self, chalk: List[int], k: int) -> int:
        k %= sum(chalk)
        for i, c in enumerate(chalk):
            k -= c
            if k < 0:
                return i
```
- Given test cases pass
- I'll make up one test case:
    - `chalk = [5,1,5,7,2,34,54,76,1,7,34,25,6,9], k = 1005`: pass
- Submitting...

![Screenshot 2024-09-01 at 11 11 40 PM](https://github.com/user-attachments/assets/b9528a9b-81cd-4390-b8c7-be727655010b)

Solved!

