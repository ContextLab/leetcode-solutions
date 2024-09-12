# [Problem 1684: Count the Number of Consistent Strings](https://leetcode.com/problems/count-the-number-of-consistent-strings/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- The "trivial" solution would be: `sum([all([c in allowed for c in word]) for word in words])`
- However, we can do a little better using sets, which have constant lookup time
- If the intersection between `set(allowed)` and `set(word)` has the same length as `set(word)`, then we know that `word` is consistent.  Particularly if there are repeated characters, set intersection should be faster than `all([c in allowed for c in word])`

## Refining the problem, round 2 thoughts
- Here's a faster approach (I think):
```python
count = 0
allowed = set(allowed)
for word in words:
    word = set(word)
    count += len(allowed.intersection(word)) == len(word)
return count
```
- Let's try it...

## Attempted solution(s)
```python
class Solution:
    def countConsistentStrings(self, allowed: str, words: List[str]) -> int:
        count = 0
        allowed = set(allowed)
        for word in words:
            word = set(word)
            count += len(allowed.intersection(word)) == len(word)
        return count
```
- All given test cases pass
- Submitting...

![Screenshot 2024-09-11 at 10 10 52 PM](https://github.com/user-attachments/assets/532fa423-d8b9-4657-8f84-d8fc27c9930d)

Solved!  Although...I'm a little surpised it's so slow...what about the "trivial" version?

```python
class Solution:
    def countConsistentStrings(self, allowed: str, words: List[str]) -> int:
        return sum([all([c in allowed for c in word]) for word in words])
```

![Screenshot 2024-09-11 at 10 12 19 PM](https://github.com/user-attachments/assets/c2834f6c-4500-4ff8-a8e3-54c7f3c126ac)

Huh...actually, that's faster!?  🤷  Maybe it's because `all` returns `False` at the very first match.  What if we change `allowed` to a `set`?

```python
class Solution:
    def countConsistentStrings(self, allowed: str, words: List[str]) -> int:
        allowed = set(allowed)
        return sum([all([c in allowed for c in word]) for word in words])
```

![Screenshot 2024-09-11 at 10 14 05 PM](https://github.com/user-attachments/assets/1cd3a44e-20c1-446c-8a21-16c6dfdfff44)

Ok, maybe a tiny speed up...

In any case, another one completed! 🥳


        
