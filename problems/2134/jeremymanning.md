# [Problem 2134: Minimum Swaps to Group All 1's Together II](https://leetcode.com/problems/minimum-swaps-to-group-all-1s-together-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
  - I think there are two steps to solving this:
      - First, we have to detect when a block of 1s is surrounded (on either side) by 0s.  If that happens, we need to perform swaps to "fill in" the holes
      - Second, we (might?) need to account for the circularity property.
          - I'm not fully certain that this matters, though, if the way we're detecting "ungrouped 1s" is to look for blocks of 1s that are surrounded on *both* sides by 0s.  E.g., for the third provided example (`nums = [1, 1, 0, 0, 1]`), neither block of 1s would be in need of filling in, since neither has 0s on *both* sides.
          - So...maybe we just need to:
              - Identify islands of 1s
              - Count up the numbers of 0s in between (this tells us how many swaps are needed)
  - I suspect we could solve this in $O(n)$ time if we just go from left to right through `nums`.  We need to keep track of:
      - The `count` of the number of swaps needed (initialize to 0)
      - Whether we've encountered 0s yet
      - Whether we've encountered 1s after encountering 0s
      - Then we keep *count* of any subsequent 0s we see.  This is important to track since it might get added to `count`.
      - If we encounter 1s after that, we'll need to add the temporary count to `count`.  Then we reset all of our "state" flags.

## Refining the problem, round 2 thoughts
- Start by initializing:
    - `swaps = 0` (track the minimum number of swaps needed)
    - `leadingZeros = False`: have we encountered 0s yet?
    - `onesAfterLeadingZeros = False`: have we encountered 1s after encountering (leading) 0s?
    - `zerosAfterOnes = False`: have we encountered 0s after encountering 1s (after encountering 0s)?  Once this turns to `True` we need to start a temporary counter (also initialize `temp_count = 0`).
    - `onesAfterTrailingZeros = False`: have we encountered 1s after the 0s that came after 1s that came after 0s?  If we hit this condition, we add the temprary count to `swaps` and reset all flags.
- Let's loop through `nums`.  The current element is `i`
    - If `i == 0`:
        - If `not leadingZeros`:
            - `leadingZeros = True`
        - Else if `onesAfterLeadingZeros`:
            - `temp_count += 1`
            - `zerosAfterOnes = True`
    - If `i == 1`:
        - If `zerosAfterOnes`:
            - `onesAfterTrailingZeros = True` -- note: we may not actually need to track this...
            - `leadingZeros, onesAfterLeadingZeros, zerosAfterOnes = False, False, False`
            - `swaps += temp_count`
            - `temp_count = 0`
        - Else if `leadingZeros`:
            - `onesAfterLeadingZeros = True`
- Now return `swaps`
- Let's implement this...

## Attempted solution(s)
```python
class Solution:
    def minSwaps(self, nums: List[int]) -> int:
        swaps, tmp_count = 0, 0
        leadingZeros, onesAfterLeadingZeros, zerosAfterOnes = False, False, False

        for i in nums:
            if i == 0:
                if not leadingZeros:
                    leadingZeros = True
                elif onesAfterLeadingZeros:
                    tmp_count += 1
                    zerosAfterOnes = True
            if i == 1:
                if zerosAfterOnes:
                    leadingZeros, onesAfterLeadingZeros, zerosAfterOnes = False, False, False
                    swaps += tmp_count
                    tmp_count = 0
                elif leadingZeros:
                    onesAfterLeadingZeros = True

        return swaps
```
- All given test cases pass
- Let's make up some new arrays with random 0/1 sequences:
    - `nums = [0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 1, 0, 0, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 1, 1, 0, 0]`: wrong answer!  So...what's going on?  Let's maybe try with a shorter random sequence:
    - `nums = [1, 0, 1, 0, 0, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0]`: eh...that passes.  Another?
    - `nums = [0, 0, 1, 1, 1, 0, 1, 1, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0]`: that passes too... 🤔
    - `nums = [1, 1, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 0, 1, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 0]`: this one fails too!  This gives me an idea...
    - `nums = [0, 1, 1, 0, 0, 1, 0, 1]`: great, this fails too.  So I think I know what's happening: my heuristic for counting the minimum number of swaps doesn't work in all cases.  E.g., if we swap positions 0 and 5 (producing the array `[1, 1, 1, 0, 0, 0, 0, 1]`), the new array is now OK (all 1s are grouped, given the circularity property).  So we need a different approach for solving this.  Back to the drawing board...
 
## Another round of brainstorming...
- How about thinking up some edge cases and other things we know about the problem:
    - If the elements are all 0s or all 1s, the minimum number of swaps is 0 (no calculations needed)
    - The length of the final contiguous block of 1s is equal to the number of 1s in `nums`
    - The final block could start at any position (note: maybe this is a sliding windows problem?).  And we need to account for the possibility that the block could start near the end of the array and wrap around to the beginning (leveraging the circular property of `nums`).  Wrapping is easy to simulate; if we ever go "past" the end of the array we can find the equivalent "circularly shifted" position using `nums[i % len(nums)]`
    - For a given "attempt" at making the current "block" into a contiguous block of 1s, the number of swaps needed is equal to the number of 0s in that block
- What if we do something like this:
    - Count up the total number of 1s.  This is simply `n = sum(nums)`
    - Looping through each possible start (`i`) of a sliding window of length `n`, count up the number of 0s.  Whichever window has the fewest 0s (let's say there are `x` 0s in that window) tells us that we need `x` swaps to make a contiguous block of 1s starting at position `i`.
- Things to solve:
    - How do we deal with the circular property of `nums`?  We can loop up to an additional `n` elements *past* the `len(nums)` (or...maybe `n - 1`?) and use circular indexing instead of absolute indexing.
    - Can we count the numbers of zeros efficiently?  This will be an $O(n^2)$ algorithm if we "re-count" the 0s from scratch for every sliding window.  But (after the very first window) we actually know that the count will only change by a max of 2:
        - If the first element of the previous window was a 0, the new count decrements by 1
        - If the last element of the current window is a 0, the new count increments by 1
- Let's put this all together...

## Next attempted solution
```python
class Solution:
    def minSwaps(self, nums: List[int]) -> int:
        n = sum(nums)

        # compute number of 0s in "first" sliding window
        n_zeros = n - sum(nums[:n])

        # initialize the minimum number of swaps to n_zeros.  then loop through the array (using circular indexing)
        swaps = n_zeros
        for i in range(1, len(nums) + n):
            # update n_zeros
            if nums[(i - 1) % len(nums)] == 0:
                n_zeros -= 1                
            if nums[(i + n - 1) % len(nums)] == 0:
                n_zeros += 1

            swaps = min(swaps, n_zeros)

        return swaps
```
- All test cases + additional cases now pass!
- Submitting...

![Screenshot 2024-08-02 at 12 04 08 AM](https://github.com/user-attachments/assets/7fd8c342-c77b-423e-945c-fcaa6a51c037)

Solved!

