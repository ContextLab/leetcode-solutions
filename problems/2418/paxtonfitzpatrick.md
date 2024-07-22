# [Problem 2418: Sort the People](https://leetcode.com/problems/sort-the-people/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- great, this seems easy. I know there's a concise syntax for sorting one list by another in Python; let's see if I can remember it...
- I very much doubt we'll be able to beat Python's built-in sorting algorithm with some creative approach here, since [`powersort`](https://docs.python.org/release/3.11.0/whatsnew/changelog.html#id100:~:text=bpo%2D34561%3A%20List,strategy%20did%20better.) is $O(n \log n)$, implemented in C, and heavily optimized

## Refining the problem, round 2 thoughts

## Attempted solution(s)

```python
class Solution:
    def sortPeople(self, names: List[str], heights: List[int]) -> List[str]:
        return [name for _, name in sorted(zip(heights, names), reverse=True)]
```

![](https://github.com/user-attachments/assets/8782eafa-49d9-4730-ac9d-34f2c7d2caa3)

Huh, I'm surprised that only beat ~50% of submissions. Someone must've found a faster way... let me try something real quick...

```python
class Solution:
    def sortPeople(self, names: List[str], heights: List[int]) -> List[str]:
        return (name for _, name in sorted(zip(heights, names), reverse=True))
```


![](https://github.com/user-attachments/assets/cc74f20d-e7f0-4f74-83df-7ad6656e02aa)

Aha -- whatever code Leetcode runs on the backend to evaluate submissions will accept a generator when the question calls for a list/array. That's a cheesy but kinda neat trick to remember for the future. Let's try one more thing just for curiosity's sake:

```python
class Solution:
    def sortPeople(self, names: List[str], heights: List[int]) -> List[str]:
        for _, name in sorted(zip(heights, names), reverse=True):
            yield name
```

![](https://github.com/user-attachments/assets/40258f4e-e24c-49a9-8e0d-a9bcebd75945)

Cool, that's what I kinda expected would happen -- better memory performance since we now aren't even constructing the generator object in memory, but slightly slower runtime because the function itself is now a Python-level generator instead of a built-in/internally optimized generator expression.
