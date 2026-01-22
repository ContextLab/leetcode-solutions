# [Problem 2040: Kth Smallest Product of Two Sorted Arrays](https://leetcode.com/problems/kth-smallest-product-of-two-sorted-arrays/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the k-th smallest product from all pairs nums1[i] * nums2[j]. Both arrays are sorted, lengths up to 5e4 so brute force O(n*m) to build all products is impossible. Typical approach for "k-th smallest" in product / sum problems is to binary-search the value and count how many pairs produce product <= mid. So: do a value-binary-search and for each mid compute count of pairs with product <= mid. The difficulty is counting efficiently and correctly across negatives, zeros, positives because sign flips inequality when dividing. Also be careful with integer division rounding.

I can split logic by sign of a (element from one array). For a>0, condition a*b <= x becomes b <= floor(x/a), we can use bisect_right on sorted other array. For a==0, product is 0 (counted if x>=0). For a<0, a*b <= x becomes b >= ceil(x/a) (inequality flips), so count = len(other) - bisect_left(other, ceil(x/a)). Must implement ceil(x/a) for negative a carefully with integer math. Also to reduce work iterate over the shorter array and bisect in the longer array.

Binary-search range can be derived from extreme products of endpoints.

## Refining the problem, round 2 thoughts
Edge cases:
- zeros: a==0 handles many pairs at once.
- negative division rounding: use identity ceil(p/q) = -floor(-p/q). For a < 0 we can compute ceil(x / a) as - ((-x) // a) in Python (since // is floor division).
- choose the shorter array as the outer loop to lower count complexity: O(min(n,m) * log(max(n,m))) per count call.
- Binary search over possible product values between min_product and max_product inclusive. Use while low < high to find first value with count >= k.

Complexity: Each count computation costs O(min(n,m) * log(max(n,m))). Binary search over value range uses about log(V) steps where V ~ 2e10 (values up to 1e5*1e5 = 1e10) so ~ 34 steps. So overall ~ O(min(n,m) * log(max(n,m)) * log(V)). With constraints this is acceptable in Python.

Now the implementation.

## Attempted solution(s)
```python
from bisect import bisect_left, bisect_right

class Solution:
    def kthSmallestProduct(self, nums1, nums2, k):
        # Ensure iterate over the smaller array for efficiency
        if len(nums1) > len(nums2):
            nums1, nums2 = nums2, nums1

        # helper to count pairs with product <= x
        def count_le(x):
            cnt = 0
            m = len(nums2)
            for a in nums1:
                if a == 0:
                    if x >= 0:
                        cnt += m
                    # else contribute 0
                elif a > 0:
                    # b <= floor(x / a)
                    bound = x // a
                    # number of b in nums2 <= bound
                    cnt += bisect_right(nums2, bound)
                else:  # a < 0
                    # need b >= ceil(x / a)
                    # ceil(x / a) = - floor(-x / a) -> in integer math:
                    # ceil_div = - ((-x) // a)
                    # Note: here a < 0 so (-x)//a is valid floor of (-x)/a
                    ceil_div = - ((-x) // a)
                    idx = bisect_left(nums2, ceil_div)
                    cnt += m - idx
            return cnt

        # determine search range from extremes (products of endpoints)
        candidates = [
            nums1[0] * nums2[0],
            nums1[0] * nums2[-1],
            nums1[-1] * nums2[0],
            nums1[-1] * nums2[-1],
        ]
        low = min(candidates)
        high = max(candidates)

        # binary search for smallest value such that count_le(value) >= k
        while low < high:
            mid = (low + high) // 2
            if count_le(mid) >= k:
                high = mid
            else:
                low = mid + 1
        return low
```
- Notes:
  - We iterate over the shorter array (nums1 after possible swap) and use bisect in the longer one (nums2) to keep each count operation efficient.
  - For a>0: count elements in nums2 <= floor(x/a) via bisect_right.
  - For a==0: product is zero; it contributes len(nums2) to count iff x >= 0.
  - For a<0: we need b >= ceil(x/a). Use ceil(x/a) = -((-x) // a) (valid because a < 0 and Python's // is floor division). Then count indices >= that threshold via len - bisect_left.
  - Binary search range is taken from 4 endpoint products (min/max possible product).
  - Time complexity: O(min(n,m) * log(max(n,m)) * log(V)), where V ~ 1e10 (value range). In practice acceptable for n,m <= 5e4.
  - Space complexity: O(1) extra (excluding input).