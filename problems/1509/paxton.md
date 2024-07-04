# [Problem 1509: Minimum difference between largest and smallest value in three moves](https://leetcode.com/problems/minimum-difference-between-largest-and-smallest-value-in-three-moves/description/)

## Initial thoughts (stream-of-consciousness)
- reducing the difference between the largest and smallest values requires changing one of those values to something else
- sounds like we'll need to sort `nums`, which takes $O(n \log n)$ time
  - could get away without sorting by finding `min(nums)` and `max(nums)`, `pop`ping one from the list, and repeating
    - probably not worth it... I think modifying the list in place multiple times would be slower than just doing it once with `.sort()`, and the solution doesn't actually ask for the list containing the min difference after 3 moves, just what that min difference *would* be.
- How do we decide what to change a selected value to?
  - shouldn't specifically matter as long as the new value doesn't become the min or max for a subsequent step, or the final list -- so something towards the "center" of the values
    - best choice might theoretically be the median? I think the mean would be a bad choice (e.g., we oculd have `[1, 2, 3, 1000]`). But again, we don't actually have to return the final list, so we can be hand-wavey about that.
- How do we decide whether it's better to change the min or the max?
  - Maybe whichever is further from the median? Once the list is sorted, median is easy to find (index with `len(nums) // 2`)
  - actually, if we can only make 3 moves, and each move entails changing the either the min or max, there aren't that many combinations of moves we could make... rather than coming up with a way to figure out the "optimal" move 3 times, can we just test all possibilities? Possible combinations (order of moves shouldn't matter):
    - change min 3 times
    - change max 3 times
    - change min 2 times, change max 1 time
    - change min 1 time, change max 2 times
  - So it's definitely worth sorting the list, because that will make the values of interest easy to access as the 1st 3 and last 3 items.
- Also, if the list contains <= 4 items, the answer is 0 because we can change all the values to the same thing. So we can short circuit that case.
  - hmm... actually, this is also true if it contains > 4 items, and all but 3 are the same value (e.g., `[1, 2, 5, 5, 5, 5, 5, 9]`)... do we need to check for this?
    - I think not, because if all but 3 items are the same value, then any possible case of that shoudl be covered by checking the possible combinations listed above. E.g.:
      - `[1, 1, 1, 1, 1, 2, 3, 4]`: optimal moves are changing max 3x
      - `[1, 2, 2, 2, 2, 2, 3, 4]`: optimal moves are changin min once and max twice
      - `[1, 2, 3, 4, 4, 4, 4, 4]`: optimal moves are changing min 3x
- To test all possible combinations of moves, we just need to use the indices in the sorted list of the resulting min and max values after making all 3 moves from each possibility:
    - change min 3 times
      - new min would be `nums[3]`; new max would be `nums[-1]`
    - change max 3 times
      - new min would be `nums[0]`; new max would be `nums[-4]`
    - change min 2 times, change max 1 time
      - new min would be `nums[2]`; new max would be `nums[-2]`
    - change min 1 time, change max 2 times
      - new min would be `nums[1]`; new max would be `nums[-3]`

## Refining the problem

## Attempted solution(s)
```python
class Solution:
    def minDifference(self, nums: List[int]) -> int:
        if len(nums) <= 4:
            return 0

        # note: in reality, should really copy the list and sort the copy so we
        # don't modify the input... but since that'd take a tiny bit extra time
        # and memory, and best practices aren't part of the criteria, I skipped
        # it
        nums.sort()
        return min(
            nums[-1] - nums[3],  # change min 3x
            nums[-4] - nums[0],  # change max 3x
            nums[-2] - nums[2],  # change min 2x, max 1x
            nums[-3] - nums[1]   # change min 1x, max 2x
        )
```

![](https://github.com/paxtonfitzpatrick/leetcode-solutions/assets/26118297/9b7a1f40-c018-43dd-aa42-65888463af51)
