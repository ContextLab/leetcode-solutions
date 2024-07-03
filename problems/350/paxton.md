# [Problem 350: Intersection of Two Arrays II](https://leetcode.com/problems/intersection-of-two-arrays-ii/description/?envType=daily-question&envId=2024-07-02)

## Initial thoughts (stream-of-consciousness)
- easiest way would probably be to sort both arrays and then iterate through them in the same loop, check the current value in one against the current value in the other, etc...
- but the sorting upfront is going to take $O(n \log n)$ (Timsort)... I think there's a way to do it in $O(n)$, where we just run through each list one time. Roughly:
  - loop through one list, get counts of each unique value, store counts in a dict (keys=unique values, values=counts)
    - does it matter which one? Don't think so?...
    - does leetcode let you import standard library modules? If so, could use `collections.Counter` instead, or `collections.defaultdict(int)` + loop (former would be faster, I think?)
      - actually... if we can use standard library modules `collections.Counter` would make this problem trivial since it supports multiset operations. *Probably* would be faster than implementing manually? But let's compare to see...
  - create 2nd dict of counts for 2nd list, loop through 2nd list
    - For each item in 2nd list, if the item is a key in the first dict and its count in the 1st dict is > its current count in the 2nd dict, then:
      - append the item to the output list
      - increment the item's count in the 2nd dict by 1
  - return the output list

## Refining the problem

## Attempted solution(s)
If we can use standard library modules, the simplest solution is:

**Solution 1:**
```python
from collections import Counter

class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        nums1_counts = Counter(nums1)
        nums2_counts = Counter(nums2)
        nums_intersection = nums1_counts & nums2_counts
        return list(nums_intersection.elements())
```

If not, then we can do:

**Solution 2:**
```python
class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        nums1_counts = {}
        for num in nums1:
            nums1_counts[num] = nums1_counts.get(num, 0) + 1

        nums2_counts = {}
        nums_intersection = []
        for num in nums2:
            try:
                count_in_nums1 = nums1_counts[num]
            except KeyError:
                continue
            if count_in_nums1 > nums2_counts.setdefault(num, 0):
                nums_intersection.append(num)
                nums2_counts[num] += 1

        return nums_intersection
```

Comparing the two solutions:

**Solution 1:**
![](https://github.com/paxtonfitzpatrick/leetcode-solutions/assets/26118297/400c5e17-8608-4804-afd8-4c3229c7c55e)

**Solution 2:**
![](https://github.com/paxtonfitzpatrick/leetcode-solutions/assets/26118297/83dd6ff9-77ca-4b98-acd9-c8da08262e6b)


Looks like Solution 1 is *slightly* faster...

...though I clicked submit for each of these multiple times and the variability in the runtime was surprisingly high relative to the total runtime -- one of the times I submitted Solution 1, it took 59ms and beat only 12.30% of other submissions. I assume each submission runs against the same test cases, so the difference is probably just inherent variability in code execution and/or whatever overhead is added by the leetcode runner. Given that, any "real" difference between these two solutions is probably negligible. And in fact, the runtime savings of these two solutions versus the $O(n \log n)$ solution might not even be worth it, since both of these two solutions need to allocate additional memory to store the counts dicts.
