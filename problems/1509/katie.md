Every optimal move is going to consist of moving an extreme value to the center, so you can just take the range of 4 potential subsets starting with index 0, 1, 2, or 3 all of length `len(nums)-3`

```
class Solution(object):
    def minDifference(self, nums):
        """
        :type nums: List[int]
        :rtype: int
        """
        if len(nums) <=4:
            return 0
        nums.sort()
        best = nums[-1] - nums[3]
        for x in range(3):
            best = min(best, nums[-4+x] - nums[x])
        return best
```
<img width="604" alt="Screen Shot 2024-07-04 at 4 17 17 PM" src="https://github.com/KatieONell/leetcode-solutions/assets/12962290/e691f187-1c77-4ce2-92f4-0056bce4762a">
