# [Problem 350: Intersection of Two Arrays II](https://leetcode.com/problems/intersection-of-two-arrays-ii/description/?envType=daily-question&envId=2024-07-02)

## Initial thoughts (stream-of-consciousness)
- We'll likely need to start by sorting the arrays.  Time needed: $O(n \log n)$, where array lengths are $O(n)$.
- Maintain two counters, $i$ and $j$, to keep track of where we are in each list
- We'll want to loop until at least one list has been exhausted (after that point we can't have any more overlap anyway, so we don't need to do any more computation)
- There are no super long lists, so sorting will (hopefully) be OK
- List elements are all integers, so no specialized equality tests are needed

## Refining the problem
- Probably start with a while loop.  `i` will track our position in `nums1` and `j` will track our position in `nums2`.
- We can maintain a list of matches, `x`
- If `nums1[i] == nums2[j]` append `nums1[i]` to `x` and increment `i` and `j`
- Otherwise...let's see.  If `nums1[i]` is larger than `nums2[j]` then we should increment `j`, and vice versa.
- If `i` is bigger than `len(nums1)` OR if `j > len(nums2)`, return `x`
- Outside of the loop, return `x`

## Attempted solution(s)

```python
class Solution:
    def intersect(self, nums1: List[int], nums2: List[int]) -> List[int]:
        nums1.sort()
        nums2.sort()

        x = []
        i = 0
        j = 0

        while (i < len(nums1)) and (j < len(nums2)):
            if nums1[i] == nums2[j]:
                x.append(nums1[i])
                i += 1
                j += 1
            elif nums1[i] > nums2[j]:
                j += 1
            else:  # nums1[i] < nums2[j]
                i += 1

        return x
```

- Given test cases pass
- New test case: `nums1 = [5]` and `nums2 = [5, 4, 3, 2, 1, 5]` (passed)
- Another test case: `nums1 = [1]` and `nums2 = [2, 3, 4]` (passed; also tried swapping `nums1` and `nums2`

Submitting....

![Screenshot 2024-07-03 at 1 10 18 PM](https://github.com/ContextLab/leetcode-solutions/assets/9030494/a5214183-68bb-4c5f-b3f9-2cd708073806)

Solved!
