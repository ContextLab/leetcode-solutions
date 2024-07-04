Every optimal move is going to consist of moving an extreme value to the center, so you can just take the range of 4 potential subsets starting with index 0, 1, 2, or 3 all of length `len(nums)-3`

```
if len(nums) <=4:
  return 0
nums.sort()
best = nums[-1] - nums[3]
for x in range(3):
  best = min(best, nums[-4+x] - nums[x])
return best
```
