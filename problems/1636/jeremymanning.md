# [Problem 1636: Sort Array by Increasing Frequency](https://leetcode.com/problems/sort-array-by-increasing-frequency/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- We can make a hash table with the counts of each item
- Then we'll make an array `x = [[counts[i], i] for i in nums]`
- Then we can return `[n[1] for n in sorted(x, key=lambda x: [x[0], -x[1]])]`

## Refining the problem, round 2 thoughts
- No special cases to account for that I can think of...

## Attempted solution(s)
```python
class Solution:
    def frequencySort(self, nums: List[int]) -> List[int]:
        counts = {}
        for n in nums:
            if n in counts:
                counts[n] += 1
            else:
                counts[n] = 1
        
        x = [[counts[i], i] for i in nums]
        return [n[1] for n in sorted(x, key=lambda x: [x[0], -x[1]])]
```
- Given test cases pass
- Submitting...

![Screenshot 2024-07-22 at 8 13 33 PM](https://github.com/user-attachments/assets/2a22346c-4997-486e-a79d-8e473d4b78b3)

Solved!

- Actually: Maybe we can save some memory by not re-storing the counts:
```python
class Solution:
    def frequencySort(self, nums: List[int]) -> List[int]:
        counts = {}
        for n in nums:
            if n in counts:
                counts[n] += 1
            else:
                counts[n] = 1
        
        return [n for n in sorted(nums, key=lambda x: [counts[x], -x])]
```

![Screenshot 2024-07-22 at 8 16 25 PM](https://github.com/user-attachments/assets/db39e587-23c4-4974-bcd6-7ca5ab2c48c0)

Nope, not helpful 🙃!
