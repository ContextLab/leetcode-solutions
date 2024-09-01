# [Problem 2022: Convert 1D Array Into 2D Array](https://leetcode.com/problems/convert-1d-array-into-2d-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- A nice and easy one
- There are two clear approaches:
    - We could build up the 2D array in a for loop
    - Or we could use a list comprehension to build it in a single step
- I'll go with the list comprehension approach, since I think we can do it as a one liner (plus a check that `m * n == len(original)`)

## Refining the problem, round 2 thoughts
- Assuming the dimensions work out, I think we can just return `[original[x:(x + n)] for x in range(0, len(original), n)]`

## Attempted solution(s)
```python
class Solution:
    def construct2DArray(self, original: List[int], m: int, n: int) -> List[List[int]]:
        if m * n == len(original):
            return [original[x:(x + n)] for x in range(0, len(original), n)]
        else:
            return []
```
- Given test cases pass
- Submitting...

![Screenshot 2024-08-31 at 9 48 44 PM](https://github.com/user-attachments/assets/f1d0b5ee-380f-4e7e-84f0-33e67ca02af5)

- Solved!
- Out of curiousity, what if I change the list comprehension to a generator?

```python
class Solution:
    def construct2DArray(self, original: List[int], m: int, n: int) -> List[List[int]]:
        if m * n == len(original):
            return (original[x:(x + n)] for x in range(0, len(original), n))
        else:
            return []
```

![Screenshot 2024-08-31 at 9 50 35 PM](https://github.com/user-attachments/assets/e6e9819c-f3e8-4310-b491-953493db8550)

- Interesting; runtime is slightly worse (though maybe still within the margin of error), but memory is slightly better.



