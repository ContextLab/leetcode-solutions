# [Problem 350: Intersection of Two Arrays II](https://leetcode.com/problems/intersection-of-two-arrays-ii/description/)

## Initial thoughts (stream-of-consciousness)
first order of business is figuring out which elements are present in both; second is getting the number of times

## Refining the problem

## Attempted solution(s)
```
class Solution(object):
    def intersect(self, nums1, nums2):
        """
        :type nums1: List[int]
        :type nums2: List[int]
        :rtype: List[int]
        """
        intersection = []
        for x in set(nums1).intersection(set(nums2)):
            intersection.extend([x]*min(nums1.count(x), nums2.count(x)))
        return intersection
```
<img width="611" alt="Screen Shot 2024-07-04 at 4 27 44 PM" src="https://github.com/KatieONell/leetcode-solutions/assets/12962290/eda945af-174a-4b98-b6b2-0332b9db4fd6">
