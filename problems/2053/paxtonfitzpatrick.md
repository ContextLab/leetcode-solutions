# [Problem 2053: Kth Distinct String in an Array](https://leetcode.com/problems/kth-distinct-string-in-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- this seems pretty straightforward. Though there might be a slightly more optimal way than what I'm thinking of. My plan is to:
  - use a `collections.Counter()` to get the number of occurrences of each string in `arr`. This takes $O(n)$ time and space.
  - I then want to find the items that have a count of 1, and get the $k$th one of those. There are a few ways I could do this:
    - initialize a variable `n_dist` to 0, then loop over `arr` and check if each item's count is 1. If yes, increment `n_dist` by 1. If `n_dist == k`, return the item. If I exhaust the list, return `""`. This would take $O(n)$ time.
    - `Counter`s preserve insertion order, so I could instead loop over its items and increment `n_dist` by 1 each time I encounter a key whose value is 1, and return the key when `n_dist == k` (or `""` if I exhaust the `Counter`). This would take $O(m)$ time where $m$ is the number of unique items in `arr`, which could be all of them, so it'd be $O(n)$ in the worst case.
    - use `Counter.most_common()` to get a list of `(item, count)` tuples in descending order of count, with tied counts appearing in insertion order. Index this with `-k` to get the $k$th least common item and its count. If its count is 1, return the item; otherwise return `""`. I initially thought this might be the best approach, but I think it's actually the worst one because `.most_common()` has to sort the items by count internally, which would could take up to $O(n \log n)$ time if all items in `arr` are unique.
    - Given this, I'll go with the second option... though I might also try the 3rd one to compare, because my intuition is that for small $n$s (`arr` contains at most 1,000 items), an $O(n \log n)$ operation in C might end up being faster than an $O(n)$ operation in Python.
    - actually, never mind -- I can't index it with `-k`, I'd have to iterate over the `most_common()` list in reverse to find the total number of elements with a count of 1 (`n_distincts`), then index it with `-(n_distincts - k)` to get the $k$th item with a count of 1. That makes it not worth it, I think.

## Refining the problem, round 2 thoughts

- This won't change the asymptotic complexity, but I thought of a way to do this in $O(n)$ time instead of $O(2n)$, at the cost of some additional (less than $O(n)$) space. I could:
  - initialize a dict `distincts` to store distinct items as keys with values of `None`
    - this basically acts as a set that provides $O(1)$ lookup, insertion, and deletion, but also preserves insertion order
  - initialize a set `non_distincts` to store items that are not distinct
  - for each item in `arr`:
    - if it's in `non_distincts`, continue on. If it's not, then check whether it's in `distincts`
      - if so, remove it from `distincts` and add it to `non_distincts`
      - otherwise, add it to `distincts`
  - if the length of `distincts` is $\lt k$, return `""`. Otherwise, use `itertools.islice` to return the $k$th key
- I might try this as well, just to compare.

## Attempted solution(s)

### Approach #1

```python
class Solution:
    def kthDistinct(self, arr: List[str], k: int) -> str:
        counts = Counter(arr)
        n_distincts = 0
        for item, count in counts.items():
            if count == 1:
                n_distincts += 1
                if n_distincts == k:
                    return item
        return ""
```

![](https://github.com/user-attachments/assets/d5cdb924-29a6-451f-9798-8016ced24060)

### Approach #2

```python
class Solution:
    def kthDistinct(self, arr: List[str], k: int) -> str:
        distincts = {}
        non_distincts = set()
        for item in arr:
            if item not in non_distincts:
                if item in distincts:
                    del distincts[item]
                    non_distincts.add(item)
                else:
                    distincts[item] = None
        if len(distincts) < k:
            return ""
        return next(islice(distincts.keys(), k-1, None))
```

![](https://github.com/user-attachments/assets/b6f4e593-ada0-4e97-9353-410cf1933e84)

Huh, I'm surprised both that this one was slower and that it used less memory. I think with a sufficiently large `arr`, the result would be the opposite.
