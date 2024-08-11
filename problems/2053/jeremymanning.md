# [Problem 2053: Kth Distinct String in an Array](https://leetcode.com/problems/kth-distinct-string-in-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- This seems straightforward
- Let's keep a `set` containing all of the unique strings
- We'll loop through `arr`, incrementing a counter each time we encounter a new unique string, and then we'll add the unique string to the set
- Once the counter gets to `k` we'll return that string
- If we never reach `k` but we run out of elements of `arr`, we return an empty string

## Refining the problem, round 2 thoughts
- I'm not sure if it'd be faster to use a set or hash table to track unique strings...but I'll go with a set
- I think I'm ready to implement this...

## Attempted solution(s)
```python
class Solution:
    def kthDistinct(self, arr: List[str], k: int) -> str:
        unique_strings = set()
        counter = 0
        for s in arr:
            if s not in unique_strings:
                counter += 1
                if counter == k:
                    return s
                unique_strings.add(s)
        return ""
```
- Ok, the first test case is failing-- I seem to have read the problem incorrectly.  It looks like we also need consider *future* instances of each string (not just the first occurance that is unique *up to that point* in the list).
- So I think we can just use a hash table to count up the number of occurances of each string in `arr`
- Then we can loop through `arr` and increment a counter until we hit the `k`th string with only one occurance:


```python
class Solution:
    def kthDistinct(self, arr: List[str], k: int) -> str:
        counts = {}
        for s in arr:
            if s not in counts:
                counts[s] = 1
            else:
                counts[s] += 1

        counter = 0
        for s in arr:
            if counts[s] == 1:
                counter += 1
                if counter == k:
                    return s
        return ""
```
- Now the test cases pass
- I can't think of any useful edge cases off the top of my head, so I'll just submit 🙂

![Screenshot 2024-08-04 at 9 38 15 PM](https://github.com/user-attachments/assets/5f55ac90-7d67-4a04-8a3f-2cd16b52a3b1)

Solved!
