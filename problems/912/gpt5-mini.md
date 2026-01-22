# [Problem 912: Sort an Array](https://leetcode.com/problems/sort-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to sort an integer array in ascending order without using built-in sort and in O(n log n) time. The classic choices are quicksort, mergesort, and heapsort. Mergesort gives guaranteed O(n log n) time but needs O(n) extra space. Quicksort can be in-place and average O(n log n) but worst-case O(n^2) unless randomized pivot is used. Heapsort is in-place with guaranteed O(n log n) and only O(1) extra space, which matches the "smallest space complexity possible" requirement. So heapsort is a good fit here.

## Refining the problem, round 2 thoughts
I'll implement an in-place heapsort:
- Build a max-heap in O(n) by sifting down from the last non-leaf node backwards.
- Repeatedly swap the heap root (largest element) with the last element, reduce heap size by 1, and sift down the new root to restore max-heap property.
Edge cases: arrays of length 0 or 1 (already sorted). Negative numbers or duplicates are handled naturally. Time complexity: O(n log n) for the sort phase, and O(n) to build the heap ⇒ overall O(n log n). Space complexity: O(1) auxiliary space (in-place), aside from the input array.

I could also implement randomized quicksort to avoid worst-case behavior, but heapsort's guaranteed bounds and constant extra space make it the preferred choice here.

## Attempted solution(s)
```python
class Solution:
    def sortArray(self, nums: list[int]) -> list[int]:
        """
        In-place heapsort: build a max-heap then extract max repeatedly.
        Returns the sorted list in ascending order.
        """
        n = len(nums)
        if n <= 1:
            return nums

        def sift_down(i: int, heap_size: int) -> None:
            # Sift node at index i down the heap until heap property restored.
            while True:
                left = 2 * i + 1
                if left >= heap_size:
                    break
                right = left + 1
                largest = i
                if nums[left] > nums[largest]:
                    largest = left
                if right < heap_size and nums[right] > nums[largest]:
                    largest = right
                if largest == i:
                    break
                nums[i], nums[largest] = nums[largest], nums[i]
                i = largest

        # Build max-heap (heapify)
        for i in range((n // 2) - 1, -1, -1):
            sift_down(i, n)

        # Extract elements from heap one by one
        for end in range(n - 1, 0, -1):
            # Move current max to the end
            nums[0], nums[end] = nums[end], nums[0]
            # Restore heap property for the reduced heap
            sift_down(0, end)

        return nums
```
- Notes:
  - Approach: In-place heapsort. Build a max-heap in O(n) then repeatedly swap root with last element and sift down to restore heap, producing a sorted array in ascending order.
  - Time complexity: O(n log n) in the worst, average, and best practical cases for the sort phase; building the heap is O(n), so overall O(n log n).
  - Space complexity: O(1) auxiliary space (in-place), aside from the input array.
  - Implementation details: sift_down uses 0-based indexing (left child = 2*i + 1). The heapify loop starts from (n//2 - 1) down to 0 to cover all non-leaf nodes. This implementation handles duplicates and negative numbers naturally.