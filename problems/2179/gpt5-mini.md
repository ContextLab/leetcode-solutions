# [Problem 2179: Count Good Triplets in an Array](https://leetcode.com/problems/count-good-triplets-in-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count triplets of values (x,y,z) that appear in increasing index order in both permutations nums1 and nums2. Both arrays are permutations, so each value has a unique position in each array. If I convert values in nums1 to their positions in nums2, the problem reduces to counting increasing index-only triplets in a single array A (where A[i] = pos_in_nums2[nums1[i]]). So the task becomes: count triples i<j<k with A[i] < A[j] < A[k].

Counting increasing triplets can be done by, for each middle index j, counting how many smaller elements are on the left and how many larger elements are on the right, then summing left_count * right_count over j. Need an efficient way to compute left_count and right_count for all j. Fenwick (BIT) or segment tree can get prefix counts in O(log n). Two passes with a BIT: one right-to-left to compute right_count (how many elements > A[j] to the right), and one left-to-right to compute left_count and accumulate answers.

Edge considerations: n up to 1e5 so O(n log n) is fine. Values are distinct 0..n-1 so indexing for BIT is straightforward.

## Refining the problem, round 2 thoughts
- Build mapping pos2[value] = index in nums2.
- Construct A = [pos2[v] for v in nums1]. Now count increasing triplets in A.
- Right counts: iterate j from n-1 down to 0, keep BIT of counts of seen A[k] (k > j). For A[j] get right_count = number of seen positions greater than A[j] = total_seen - prefix_sum(A[j]) = sum(n-1) - prefix_sum(A[j]).
- Left counts: iterate j from 0 to n-1, with new/cleared BIT, left_count = prefix_sum(A[j]-1) (number of seen values less than A[j]); update after computing left_count.
- Multiply left_count * right_count for each j and sum.

Complexity: two passes each O(n log n). Space O(n) for arrays and BIT.

Edge cases: small n (>=3) trivial; values 0..n-1 guarantee uniqueness so no equal-value handling needed. Result can be large (up to choose(n,3)), Python int handles it.

## Attempted solution(s)
```python
class Fenwick:
    def __init__(self, n):
        # 1-indexed Fenwick tree for n elements (indices 1..n)
        self.n = n
        self.bit = [0] * (n + 1)
    def add(self, idx, val):
        # idx is 1-based
        while idx <= self.n:
            self.bit[idx] += val
            idx += idx & -idx
    def sum(self, idx):
        # prefix sum 1..idx (idx 1-based)
        res = 0
        while idx > 0:
            res += self.bit[idx]
            idx -= idx & -idx
        return res
    def range_sum(self, l, r):
        if r < l:
            return 0
        return self.sum(r) - self.sum(l-1)

class Solution:
    def goodTriplets(self, nums1: list[int], nums2: list[int]) -> int:
        n = len(nums1)
        # map value -> position in nums2
        pos2 = [0] * n
        for i, v in enumerate(nums2):
            pos2[v] = i
        # convert nums1 values to their positions in nums2
        A = [pos2[v] for v in nums1]  # values in range 0..n-1, all distinct

        # Compute right_counts[j] = number of k>j with A[k] > A[j]
        right_counts = [0] * n
        bit = Fenwick(n)
        # We'll use 1-based indices for Fenwick: position p in A maps to p+1
        for j in range(n-1, -1, -1):
            pos = A[j] + 1
            # total seen is sum(n)
            total_seen = bit.sum(n)
            # number of seen <= A[j] is bit.sum(pos)
            leq = bit.sum(pos)
            right_counts[j] = total_seen - leq
            bit.add(pos, 1)

        # Compute left counts on forward pass and accumulate answer
        bit = Fenwick(n)
        ans = 0
        for j in range(n):
            pos = A[j] + 1
            # number of seen < A[j] is sum(pos-1)
            left_smaller = bit.sum(pos - 1)
            ans += left_smaller * right_counts[j]
            bit.add(pos, 1)

        return ans

# For LeetCode compatibility: class name and method name should match problem's expected signature.
# If needed, rename method to countGoodTriplets or adapt to the exact LeetCode signature.
# Example usage (not part of submission):
# s = Solution()
# print(s.goodTriplets([2,0,1,3],[0,1,2,3]))  # expected 1
```
- Notes about the solution:
  - Transforming nums1 values to their indices in nums2 reduces the problem to counting increasing triplets in a single permutation array A.
  - Use a Fenwick (Binary Indexed) tree to count prefix frequencies in O(log n).
  - First pass (right-to-left) computes for each index j how many A[k] > A[j] with k>j.
  - Second pass (left-to-right) computes how many A[i] < A[j] with i<j and accumulates left_count * right_count.
  - Time complexity: O(n log n) due to two passes with BIT operations.
  - Space complexity: O(n) for arrays and BIT.
  - Works for n up to 1e5; Python int handles large answer values.