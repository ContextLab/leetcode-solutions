# [Problem 2134: Minimum Swaps to Group All 1's Together II](https://leetcode.com/problems/minimum-swaps-to-group-all-1s-together-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- okay, this one seems pretty easy unless there's a "gotcha" I'm not seeing
- first I'll need to figure out how many 1s there are in the list, which is just the sum of the list since it's all 1s and 0s. Call this $k$
- then I can just move a sliding window of length $k$ across the list and check how many swaps it'd take to make all items within the window 1s. This is just $k$ minus the sum of the window. The smallest sum from any window is the answer.
- the one tricky part might be handling the wrap-around of the circular array. I could probably use something like `itertools.cycle` for this, but since that returns an iterator, that'd make the slicing of the list to get each window trickier. So the simplest thing will be to just stick a few (up to $k$) elements from the beginning of the list onto the end before checking windows, so I can include those early items in windows starting with items towards the end just with regular indexing.
  - or, I could do it without modifying the input list by just checking whether the current index + $k$ is greater than the length of the list, and if so, appending the right number of elements from the beginning to the window. or I could maintain separate index variables for the start and end, and wrap the end one when necessary
    - Either of these would require assigning each window to a variable, which would use a little extra memory, and also a conditional check each iteration (or try/except), which would add a little runtime. But also, increasing the length of the input list would too. Hard to say which would be more efficient at the end of the day, but modifying the input is bad practice so even though that doesn't *really* matter here, I'll go with one of the others

## Refining the problem, round 2 thoughts

- in my approach above, summing the list to find $k$ upfront would take $O(n)$ time, sliding the window across the list would also take $O(n)$ time, and checking the sum of each window would take $O(k)$ time, so the overall time complexity would be $O(n \times k)$, which could be $O(n^2)$ if $k = n$. But I can reduce this to just $O(n)$ if I don't sum each window separately -- instead, when I shift the window by 1 index, I can subtract the left element that's no longer in the next window and add the right element that just entered the window.
- any edge cases to deal with?
  - if $k$ is 0, then there are no 1s in the list and the answer is 0 swaps
  - if $k$ is the length of the full list, then the list is all 1s and the answer is also 0 swaps
  - actually the first case above also applies if there's only one 1 ($k$ is 1), and the second also applies if there's only one 0 ($k$ is the length of the list minus 1)

## Attempted solution(s)

```python
class Solution:
    def minSwaps(self, nums: List[int]) -> int:
        len_nums = len(nums)
        k = sum(nums)
        if k < 2 or k > len_nums - 2:
            return 0

        max_ones = window_ones = sum(nums[:k])
        start_ix = 1
        end_ix = k
        while start_ix < len_nums:
            window_ones += nums[end_ix] - nums[start_ix - 1]
            if window_ones > max_ones:
                max_ones = window_ones
            start_ix += 1
            end_ix += 1
            if end_ix == len_nums:
                end_ix = 0
        return k - max_ones
```

![](https://github.com/user-attachments/assets/7e1f9869-a314-4caf-a249-cf206d875f44)
