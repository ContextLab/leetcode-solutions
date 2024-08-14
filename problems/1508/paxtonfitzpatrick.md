# [Problem 1508: Range Sum of Sorted Subarray Sums](https://leetcode.com/problems/range-sum-of-sorted-subarray-sums/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- okay I'm guessing that finding the solution the way they describe in the problem setup is going to be too slow, otherwise that'd be kinda obvious... though the constraints say `nums` can only have up to 1,000 elements, which means a maximum of 500,500 sums, which isn't *that* crazy...
- maybe there's a trick to figuring out which values in `nums` will contribute to the sums between `left` and `right` in the sorted array of sums? Or even just the first `right` sums?
- I can't fathom why we're given `n` as an argument... at first I thought it might point towards it being useful in the expected approach, but even if so, we could just compute it from `nums` in $O(1)$ time...
- For the brute force approach (i.e., doing it how the prompt describes), I can think of some potential ways to speed up computing the sums of all subarrays... e.g., we could cache the sums of subarrays between various indices `i` and `j`, and then use those whenever we need to compute the sum of another subarray that includes `nums[i:j]`. But I don't think these would end up getting re-used enough to make the trade-off of having to check `i`s and `j`s all the time worth it, just to save *part* of the $O(n)$ runtime of the already very fast `sum()` function.
- ah, a better idea of how to speed that up: computing the sums of all continuous subarrays would take $O(n^3)$ time, because we compute $n^2$ sums, and `sum()` takes $O(n)$ time. But if I keep a running total for the inner loop and, for each element, add it to the running total and append that result, rather than recomputing the sum of all items up to the newest added one, that should reduce the runtime to $O(n^2)$.
- This gave me another idea about "recycling" sums -- if I compute the cumulative sum for each element in `nums` and store those in a list `cumsums`, then I can compute the sum of any subarray `nums[i:j]` as `cumsums[j] - cumsum[i-1]`. Though unfortunately, I don't think this will actually save me any time since it still ends up being $n^2$ operations.
- Nothing better is coming to me for this one, so I think I'm going to just implement the brute force approach and see if it's fast enough. Maybe I'll have an epiphany while I'm doing that. If not, I'll check out the editorial solution cause I'm pretty curious what's going on here.
  - The complexity for the brute force version is a bit rough... iterating `nums` and constructing list of sums will take $O(n^2)$ time and space, then sorting that list of sums will take $O(n^2 \log n^2)$ time, which is asymptotically equivalent to $O(n^2 \log n)$.

## Refining the problem, round 2 thoughts


## Attempted solution(s)

```python
class Solution:
    def rangeSum(self, nums: List[int], n: int, left: int, right: int) -> int:
        sums = []
        for i in range(n):
            subsum = 0
            for j in range(i, n):
                subsum += nums[j]
                sums.append(subsum)
        sums.sort()
        return sum(sums[left-1:right]) % (1e9 + 7)
```

![](https://github.com/user-attachments/assets/fd4e974b-3abb-443e-ba30-40490e326f75)

Wow, that's a lot better than I expected. Looks like most people actually went with this approach. I'll try the cumulative sum version I mentioned above just quickly too...

```python
class Solution:
    def rangeSum(self, nums: List[int], n: int, left: int, right: int) -> int:
        # accumulate is itertools.accumulate, add is operator.add, both already
        # imported in leetcode environment
        sums = list(accumulate(nums, add)) + nums[1:]
        for i in range(1, len(nums)-1):
            for j in range(i+1, len(nums)):
                sums.append(sums[j] - sums[i-1])
        sums.sort()
        return sum(sums[left-1:right]) % (10**9 + 7)
```

![](https://github.com/user-attachments/assets/8946b8e3-91b0-404d-b131-87fc15a8835d)

Slightly slower, which I guess makes sense since it's doing basically the same thing but with a bit more overhead.
