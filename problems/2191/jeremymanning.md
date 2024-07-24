# [Problem 2191: Sort the Jumbled Numbers](https://leetcode.com/problems/sort-the-jumbled-numbers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- I think we can do the following:
    - Convert each number in `nums` to a string
    - Then replace the characters: `''.join([str(mapping[int(i)]) for i in str(n)])`
    - After converting each number in `nums`, sort the values by the given array

## Refining the problem, round 2 thoughts
- We could also solve this as a 1-liner:
    - `return [m[0] for m in sorted(zip(nums, [int(''.join([str(mapping[int(i)]) for i in str(n)])) for n in nums]), key=lambda x: x[1])]`

## Attempted solution(s)
```python
class Solution:
    def sortJumbled(self, mapping: List[int], nums: List[int]) -> List[int]:
        return [m[0] for m in sorted(zip(nums, [int(''.join([str(mapping[int(i)]) for i in str(n)])) for n in nums]), key=lambda x: x[1])]
```
- Given test cases pass
- I can't think of any critical edge cases; submitting...

![Screenshot 2024-07-23 at 11 36 22 PM](https://github.com/user-attachments/assets/7ddc4646-2f68-4e64-991b-7b4944bcef76)

Solved!
