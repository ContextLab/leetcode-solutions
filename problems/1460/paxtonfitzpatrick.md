# [Problem 1460: Make Two Arrays Equal by Reversing Subarrays](https://leetcode.com/problems/make-two-arrays-equal-by-reversing-subarrays/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- okay my first thought is: as long as all of the elements in `target` and `arr` are the same, regardless of their order, is it possible to do some series of reversals to make them equal?
- I'm pretty sure it is... and the fact that this is an "easy" problem, while coming up with an algorithm for determining what subarrays to reverse in order to check for this seems challenging, also makes me think that.
- I can't come up with a counterexample or logical reason why this wouldn't be the case, so I'll go with it.

## Refining the problem, round 2 thoughts

- I think the simplest way to do this will to be to sort both arrays and then test whether they're equal. That'll take $O(n\log n)$ time, which is fine.
- Even though `return sorted(arr) == sorted(target)` would be better practice in general, for the purposes of this problem I'll sort the arrays in place since that'll cut cut the memory used in half.

## Attempted solution(s)

```python
class Solution:
    def canBeEqual(self, target: List[int], arr: List[int]) -> bool:
        target.sort()
        arr.sort()
        return target == arr
```

![](https://github.com/user-attachments/assets/d6c036c2-d3f9-4d4d-9521-82ad96ceebed)

## Refining the problem further

- okay I just realized there's actually a way to do this in $O(n)$ time instead of $O(n\log n)$. I'm not sure it'll *actually* be faster in practice, since my first solution was pretty fast -- and it'll definitely use more memory (though still $O(n)$) -- but it's super quick so worth trying.
- basically as long as the number of occurrences of each element in the two arrays is the same, then they'll be the same when sorted. So we can skip the sorting and just compare the counts with a `collections.Counter()`:

```python
class Solution:
    def canBeEqual(self, target: List[int], arr: List[int]) -> bool:
        return Counter(target) == Counter(arr)
```

![](https://github.com/user-attachments/assets/d902d70d-1725-4816-a099-a1e10a82eb10)

So basically identical runtime and memory usage. I guess the upper limit of 1,000-element arrays isn't large enough for the asymptotic runtime improvement to make up for the overhead of constructing the `Counter`s, and the upper limit of 1,000 unique array values isn't large enough for the additional memory usage to make much of a difference.
