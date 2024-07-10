# [Problem 1598: Crawler Log Folder](https://leetcode.com/problems/crawler-log-folder/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
  - We could solve this with a stack:
      - Start with an empty stack (main folder)
      - changing the directory pushes the new folder onto the top of the stack
      - `'../'` pops the top folder of the stack (if empty, do nothing)
      - `'./'` does nothing
      - Then return the length of the stack at the end
  - We can also see that it doesn't actually matter _which_ folders we visit.  So we can use less memory by just keeping track of the depth:
      - If the next operation starts with `'..'` and `depth > 0` subtract one from the depth
      - If the next operation is (`'./'`) do nothing
      - Otherwise add one to the depth
      
## Refining the problem, round 2 thoughts
- I'm seeing that folders "consist of lowercase letters and digits"-- so they may not always start with `'d'` like in the examples
- Also: testing for `depth > 0` should happen in a nested statement so that `'../'` with `depth == 0` doesn't get counted as a "directory"
- Let's just go with this solution; it seems straightforward

## Attempted solution(s)
```python
class Solution:
    def minOperations(self, logs: List[str]) -> int:
        depth = 0
        for x in logs:
            if x == '../':
                if depth > 0:
                    depth -= 1
            elif x == './':
                continue
            else:
                depth += 1
        return depth
```
- given test cases pass
- verifying folders can start with other characters using `logs = ["e1/","d2/","../","d21/","./","../"]`: pass
- submitting...

- ![Screenshot 2024-07-09 at 9 39 46 PM](https://github.com/ContextLab/leetcode-solutions/assets/9030494/1d640a2b-6490-4c3f-a7f4-849e72885c6e)

Solved!

