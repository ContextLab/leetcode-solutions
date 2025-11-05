# [Problem 3321: Find X-Sum of All K-Long Subarrays II](https://leetcode.com/problems/find-x-sum-of-all-k-long-subarrays-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need the x-sum of every k-length sliding window. The x-sum keeps the occurrences of the top x most frequent distinct elements (tie-break by larger value) and sums the resulting array (i.e., sum value * frequency for each chosen distinct value). A sliding window suggests maintaining counts incrementally, and deciding which distinct values belong to the top-x set as the window moves.

We must frequently compare elements by (frequency, value) ordering and maintain the top-x set. This is similar to maintaining two multisets/heaps (top and bottom) like the two-heap approach for sliding-window median. Python doesn't have a balanced tree, but we can use two heaps with lazy deletion and a freq map + an "in_top" marker. Maintain:
- top heap: the chosen top-x distinct values (we must be able to access the worst among them quickly)
- bottom heap: the remaining distinct values (we must be able to access the best among them quickly)
Also keep sum_top = sum(freq[val] * val for val in top-set). Rebalance after each add/remove to ensure top contains exactly t = min(x, distinct_count) best elements.

Lazy deletion: when an element's frequency changes we push a new tuple to its current heap and mark its current in_top. When popping, we skip stale entries by checking the current freq and in_top status.

This should give O(n log m) time where m is number of distinct values (<= n).

## Refining the problem, round 2 thoughts
Edge cases:
- k == x: x-sum equals full window sum (algorithm still handles this since top will include all distinct or x distinct).
- frequencies hitting zero: must remove distinct and update t and top_size. If an element is in top and gets removed (freq 0), we must update sum_top and top_size immediately (can't wait for lazy pops).
- tie-breaker: when freq equal, larger value is considered more frequent. So ordering is by (freq, value) descending. For comparisons, I'll treat pair (freq, value) and compare lexicographically.

Implementation details:
- top heap should let us access worst among top (min by (freq, value)), so top_heap uses (freq, value, val) as min-heap.
- bottom heap should let us access best among bottom (max by (freq, value)), so bottom_heap stores (-freq, -value, val).
- Maintain freq dict and in_top dict (bool), top_size int, D distinct count, sum_top integer.
- Provide helper functions to get/pop valid entries from heaps and to rebalance.

Complexities:
- Each add/remove pushes at most one new entry and each rebalance step moves/pops elements; each pop processes at least one stale entry or valid element, so overall number of heap operations is O(n log m). Space O(m).

## Attempted solution(s)
```python
import heapq
from typing import List

class Solution:
    def xSum(self, nums: List[int], k: int, x: int) -> List[int]:
        n = len(nums)
        # Heaps and data structures:
        # top_heap: min-heap of (freq, value, val) -> worst among top is top_heap[0]
        # bottom_heap: min-heap used as max-heap storing (-freq, -value, val) -> best among bottom is bottom_heap[0]
        top_heap = []
        bottom_heap = []
        freq = {}        # current freq of value in window
        in_top = {}      # whether value is considered in top set
        D = 0            # number of distinct elements with freq > 0
        top_size = 0     # number of distinct elements currently in top set
        sum_top = 0      # sum of freq[val] * val over elements in top set

        def push_top(v):
            # push current tuple for v into top heap.
            f = freq.get(v, 0)
            if f <= 0:
                return
            heapq.heappush(top_heap, (f, v, v))
            in_top[v] = True

        def push_bottom(v):
            # push current tuple for v into bottom heap.
            f = freq.get(v, 0)
            if f <= 0:
                return
            heapq.heappush(bottom_heap, (-f, -v, v))
            in_top[v] = False

        def pop_valid_top():
            # pop until a valid top entry is found and return (f, v)
            while top_heap:
                f, val_key, v = heapq.heappop(top_heap)
                # valid if current freq matches and in_top is True
                if freq.get(v, 0) == f and in_top.get(v, False) == True:
                    return f, v
                # else stale, continue popping
            return None

        def peek_valid_top():
            while top_heap:
                f, val_key, v = top_heap[0]
                if freq.get(v, 0) == f and in_top.get(v, False) == True:
                    return f, v
                heapq.heappop(top_heap)  # drop stale
            return None

        def pop_valid_bottom():
            while bottom_heap:
                nf, nval, v = heapq.heappop(bottom_heap)
                f = -nf
                # valid if current freq matches and in_top is False
                if freq.get(v, 0) == f and in_top.get(v, True) == False:
                    return f, v
                # else stale, continue popping
            return None

        def peek_valid_bottom():
            while bottom_heap:
                nf, nval, v = bottom_heap[0]
                f = -nf
                if freq.get(v, 0) == f and in_top.get(v, True) == False:
                    return f, v
                heapq.heappop(bottom_heap)
            return None

        def rebalance():
            nonlocal top_size, sum_top
            tgt = min(x, D)
            # 1) Grow top if needed
            while top_size < tgt:
                # move best from bottom to top
                item = pop_valid_bottom()
                if not item:
                    break
                f, v = item
                # move v to top
                in_top[v] = True
                heapq.heappush(top_heap, (f, v, v))
                top_size += 1
                sum_top += f * v
            # 2) Shrink top if needed (some elements died or D decreased)
            while top_size > tgt:
                item = pop_valid_top()
                if not item:
                    break
                f, v = item
                # move v to bottom (or remove if freq==0)
                in_top[v] = False
                top_size -= 1
                sum_top -= f * v
                if freq.get(v, 0) > 0:
                    heapq.heappush(bottom_heap, (-freq[v], -v, v))
            # 3) Ensure ordering invariant: every top element >= every bottom element
            while True:
                top_peek = peek_valid_top()
                bottom_peek = peek_valid_bottom()
                if not top_peek or not bottom_peek:
                    break
                ft, vt = top_peek
                fb, vb = bottom_peek
                # if bottom's best is better than top's worst -> swap
                # compare (fb, vb) > (ft, vt)
                if fb > ft or (fb == ft and vb > vt):
                    # pop both and swap membership
                    pop_valid_bottom()  # removes bottom best
                    pop_valid_top()     # removes top worst
                    # move bottom best to top
                    in_top[vb] = True
                    heapq.heappush(top_heap, (fb, vb, vb))
                    sum_top += fb * vb
                    # move top worst to bottom (if still >0 freq)
                    in_top[vt] = False
                    sum_top -= ft * vt
                    if freq.get(vt, 0) > 0:
                        heapq.heappush(bottom_heap, (-freq[vt], -vt, vt))
                    # top_size unchanged
                    continue
                else:
                    break

        # add one value to the window
        def add_val(v):
            nonlocal D, sum_top
            prev = freq.get(v, 0)
            freq[v] = prev + 1
            if prev == 0:
                # new distinct
                D += 1
                # start in bottom
                in_top[v] = False
                heapq.heappush(bottom_heap, (-freq[v], -v, v))
            else:
                # existing
                if in_top.get(v, False):
                    # its contribution in top increases by v
                    sum_top += v
                    heapq.heappush(top_heap, (freq[v], v, v))
                else:
                    heapq.heappush(bottom_heap, (-freq[v], -v, v))

        # remove one value from the window
        def remove_val(v):
            nonlocal D, top_size, sum_top
            prev = freq.get(v, 0)
            if prev == 0:
                return
            curr = prev - 1
            freq[v] = curr
            if in_top.get(v, False):
                # element was in top: reduce contribution by v
                sum_top -= v
                if curr == 0:
                    # element removed entirely
                    in_top[v] = False
                    top_size -= 1
                    D -= 1
                    # do not push any tuple
                else:
                    # still present and still considered in top (we'll push updated tuple)
                    heapq.heappush(top_heap, (curr, v, v))
            else:
                # element was in bottom
                if curr == 0:
                    D -= 1
                    # nothing to push
                else:
                    heapq.heappush(bottom_heap, (-curr, -v, v))

        # initialize first window
        for i in range(k):
            add_val(nums[i])
        rebalance()
        ans = [sum_top]

        # slide
        for i in range(k, n):
            add_val(nums[i])
            remove_val(nums[i - k])
            rebalance()
            ans.append(sum_top)

        return ans

# Example usage wrapper for LeetCode-style:
class SolutionWrapper:
    def findXsum(self, nums: List[int], k: int, x: int) -> List[int]:
        return Solution().xSum(nums, k, x)

# If you want, you can test with the examples:
if __name__ == "__main__":
    s = Solution()
    print(s.xSum([1,1,2,2,3,4,2,3], 6, 2))  # [6,10,12]
    print(s.xSum([3,8,7,8,7,5], 2, 2))      # [11,15,15,15,12]
```

- Notes about the solution:
  - We maintain two heaps (top and bottom) and a frequency map with lazy deletion to avoid expensive arbitrary deletions from heaps.
  - top_heap stores tuples (freq, value, value) so the root is the worst among top (lowest freq, and lower value in tie) — we can pop the worst to move it down quickly.
  - bottom_heap stores (-freq, -value, value) so the root is the best among bottom (highest freq, and larger value in tie) — we can pop the best to move it up quickly.
  - in_top marks current membership; lazy entries are ignored when they become stale because their stored freq or in_top status does not match the current state.
  - sum_top is maintained incrementally on adds/removes and during moves between heaps so we can output the x-sum in O(1) per window after rebalancing.
  - Time complexity: O(n log m) where m is the number of distinct elements encountered (<= n). Each add/remove causes a few heap operations; lazy deletions ensure every stale entry is popped once.
  - Space complexity: O(m) for heaps and maps.