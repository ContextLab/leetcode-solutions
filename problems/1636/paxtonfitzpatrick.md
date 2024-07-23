# [Problem 1636: Sort Array by Increasing Frequency](https://leetcode.com/problems/sort-array-by-increasing-frequency/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- okay, I can think of a few ways to do this. A few of them involve getting a little creative with `collections.Counter`, which seems fun, and one of those uses one of my favorite Python syntax tricks to flatten a nested list using `sum()`. So I'll implement that one.
- `Counter`s have a `.most_common()` method that returns a list of `(element, count)` tuples for each unique element in an iterable, so we can use that to construct the output list. But there are a few tricks we'll need to use to get the right result:
  - `.most_common()` returns element counts sorted in **decreasing** order, but the problem asks for them to be sorted in **increasing** order. So we'll need to loop over this list in reverse.
  - if two elements have the same count, `.most_common()` returns their counts in the order in which the first instance of each element appeared in the input iterable. The problem wants these to be in **decreasing** order, so we'll need to sort the input list (in **increasing** order, since we'll be reversing the counts themselves) before constructing the `Counter`.
    - Note: I'm going to sort the input list in place because it's more memory-efficient, but I'd never do this IRL because it mutates the input.
- Time complexity is $O(n \log n)$ because have to sort `nums` and Python 3.11+'s `powersort` is $O(n \log n)$.
- I suspect we could condense this all down into a rather gross one-liner if we were so inclined.

## Refining the problem, round 2 thoughts

- After figuring out yesterday that leetcode will accept a generator when the problem asks for a list/array, I want to try to optimize this even further by yielding values from a generator instead.

## Attempted solution(s)

### Version 1

```python
class Solution:
    def frequencySort(self, nums: List[int]) -> List[int]:
        ## full loop version:
        # nums.sort()
        # counts = Counter(nums)
        # result = []
        # for val, count in reversed(counts.most_common()):
        #     result.extend([val] * count)
        # return result

        # gross but optimized one-liner:
        return sum(((val,) * count for val, count in reversed(Counter(sorted(nums)).most_common())), ())
```

![](https://github.com/user-attachments/assets/962c1f0a-bde6-4ecb-8326-6881cd03c0a5)

Hooray for nasty one-liners! This might shave a couple ms off the runtime, but I'd probably never do this in real life because the readability trade-off is atrocious and not worth it unless the code needs to be *heavily* optimized... and at that point, just use something faster than Python.

### Version 2

```python
class Solution:
    def frequencySort(self, nums: List[int]) -> List[int]:
        for val, count in reversed(Counter(sorted(nums)).most_common()):
            yield from [val] * count
```

![](https://github.com/user-attachments/assets/6f086773-8e65-4f5d-bf4a-86b38f315d77)
