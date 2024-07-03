# [Problem 1509: Minimum difference between largest and smallest value in three moves](https://leetcode.com/problems/minimum-difference-between-largest-and-smallest-value-in-three-moves/description/)

# Initial thoughts (in no particular order, and written in stream-of-consciousness style)

- Minimizing the difference between the largest and smallest values will require determining what those largest and smallest values *are*
- If the list has fewer than 4 elements, the minimum difference will be 0 (so we can just return that without doing anything else)
- I'm thinking we should either use a heap and then enqueue each element of the list in turn, or just sort the list.  Gut: sorting the list will be better, since it'll be useful to have access to both the smallest *and* largest numbers.  But this could be solved by using two heaps (a minheap and maxheap)...although that would double the memory required.
- If we start by sorting the list, that will take $O(n \log n)$ time.  I think that's OK, because the problem definition says that the longest list length we can expect has $10^5$ elements.  So we're not dealing with any crazy-long lists.
- I'm noticing that the values can be negative...that might be important?
- All values are integers, so we don't need to check for non-numerical values, nans, etc.
- Other potential edge cases:
  - Repeated values on the ends or in the middle
  - Everything has the same value (maybe?)
  - We may want to set the smallest number to something other than the second-largest number...we might need to enumerate the possible scenarios we could see

# Refining the problem

After sorting the list, let's call the first three values $x_1$, $x_2$, and $x_3$.  The last three values will be $y_3$, $y_2$, and $y_1$.  Let's also define some other element in the "middle" of the sorted list, $n$,
for convenience.  So using this notation the list will look like $\[x_1, x_2, x_3, ..., n, ..., y_3, y_2, y_1\]$.

We can also immediately see that if the list has fewer than 6 elements, then the $x\mathrm{s}$ and $y\mathrm{s}$ might overlap, and/or $n$ might be equal to some of those $x$ and/or $y$ values.

Before doing any manipulations (since "setting any element to its current value" should still count as "setting any element of the list to 'some' value") the difference between the last and first elements
of the sorted list is the "worst" we could do.  So we might want to track that.

## Enumerating some possible options we might see
- Case 1: change $x_1$, $x_2$, and $x_3$ to $n$.  The new difference is `nums[-1] - nums[3]`.
- Case 2: change $x_1$, $x_2$, and $y_1$ to $n$.  The new difference is `nums[-2] - nums[2]`.
- Case 3: change $x_1$, $y_1$, and $y_2$ to $n$.  The new difference is `nums[-3] - nums[1]`.
- Case 4: change $y_3$, $y_2$, and $y_1$ to $n$.  The new difference is `nums[-4] - nums[0]`.

However, Case 4 can't happen unless the list has at least 5 elements, since otherwise we couldn't refer to `nums[-4]`-- so we should take that case into account.  I don't think there are any other possibilities...

# Attempted solution (attempt 1)
```python
class Solution:
    def minDifference(self, nums: List[int]) -> int:
        if len(nums) <= 3:
            return 0                
        
        nums.sort()
        current_min = nums[-1] - nums[0]

        # 1 2 3 ... c b a
        
        # option 1: 1 2 3
        x = nums[-1] - nums[3]
        if x < current_min:
            current_min = x

        # option 2: 1 2 a
        x = nums[-2] - nums[2]
        if x < current_min:
            current_min = x
        
        # option 3: 1 b a
        x = nums[-3] - nums[1]
        if x < current_min:
            current_min = x

        if len(nums) >= 5:
            # option 4: c b a
            x = nums[-4] - nums[0]
            if x < current_min:
                current_min = x
        
        return current_min
```

## Notes:
  - All test cases pass
  - Created a new test case using `nums = [5,3,2,4,-100, 1000, 40, 20, 10, 6, 5, -1, -1, -1, -1, -1, 0, 0, 0, 0, 0, -100, -100, -100]`.  That passes too.
  - Submitting!
 
  ![Screenshot 2024-07-02 at 10 50 28 PM](https://github.com/ContextLab/leetcode-solutions/assets/9030494/d5160983-16e0-44d0-a16d-68e02519b44e)

Ok, this one has been solved!
