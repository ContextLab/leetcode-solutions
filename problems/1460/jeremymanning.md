# [Problem 1460: Make Two Arrays Equal by Reversing Subarrays](https://leetcode.com/problems/make-two-arrays-equal-by-reversing-subarrays/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- There are two ways to solve this:
    - We could sort both arrays and then compare each corresponding element in turn.  This would take $O(n \log n)$ time.
    - We could count the number of occurances of each unique element, store in a hash table, and ensure that the keys/values all match.  This would take $O(n)$ time (i.e., faster).  So let's go with this approach.

## Refining the problem, round 2 thoughts
- No special cases to deal with...

## Attempted solution(s)
```python
class Solution:
    def canBeEqual(self, target: List[int], arr: List[int]) -> bool:
        target_count = {}
        arr_count = {}
        for t, a in zip(target, arr):
            if t in target_count:
                target_count[t] += 1
            else:
                target_count[t] = 1

            if a in arr_count:
                arr_count[a] += 1
            else:
                arr_count[a] = 1

        for t, t_count in target_count.items():
            if (t not in arr_count) or (target_count[t] != arr_count[t]):
                return False

        return True
```
- Given test cases pass; submitting...

![Screenshot 2024-08-02 at 8 12 24 PM](https://github.com/user-attachments/assets/0d1fd1fe-1937-4d81-8a2e-d55f3ce42dab)

Solved!
