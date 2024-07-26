# [Problem 912: Sort an Array](https://leetcode.com/problems/sort-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- No built-in functions?? Noooooooo 😩 ...guess I'm implementing a sorting algorithm today
- the problem specifically asks for $O(n \log n)$ time complexity and "the smallest space complexity possible." I know both merge sort and quicksort take $O(n \log n)$ time in the average case, but I think quicksort can vary between $O(n)$ in the best case and $O(n^2)$ in the worst case, depending on where the pivot is set? Not sure which would be preferable here.
- Also not sure which would be "the smallest space complexity possible"... the one time I implemented each of these (in an intro CS class 8 years ago 😵), the versions of both that I learned were recursive, and I think their space complexity would be pretty similar. But maybe one or the other can be implemented iteratively, like recursive vs. iterative DFS?
- I assume they mean "the smallest space complexity possible *for a sorting algorithm with $O(n \log n)$ time complexity*." The "smallest space complexity possible" *in general* is $O(1)$, but I don't know of any sorting algorithms that are both $O(n \log n)$ time complexity *and* $O(1)$ space complexity (though that doesn't mean one doesn't exist...). Things like bubble sort, insertion sort, selection sort, etc. are $O(1)$ space complexity because they modify the array in place, but those are both $O(n^2)$ time complexity, so that won't work here.
- I guess I'll just try implementing both and see what happens? If nothing else, it'll be good practice.

## Refining the problem, round 2 thoughts

- for merge sort, I think I can reduce the memory usage a bit by not slicing the list and passing copies of the left and right sublists to each recursive call, and instead just passing indicies representing the bounds of the sublists within the full list. Then in the merge step, instead of building up and return a new list of sorted values, I can just index into the full list and overwrite the values directly.
  - I don't think it'd be possible to *truly* do the sorting in place, because I'll still have to temporarily copy the sorted sublists in order to iterate through them when merging them together -- if I tried to do that with indices of the full list, I'd end up changing values in sections of the list I haven't dealt with yet. But it should reduce the total number of copies by more than half.
  - To make this work, I'll need to modify the function signature to accept a `start` and `end` value so I can pass them when I call `self.sortArray` recursively, but also give them defaults so the function works when leetcode calls it on the test cases internally. I'll also need to still return the sorted list explicitly since Leetcode expects it to be returned, but I just won't do anything with the return value during the recurions.
    - Actually, I guess I could just write the merge sort function separately and call it from the `sortArray` method,

## Attempted solution(s)

### Merge sort

```python
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        self._merge_sort(nums, 0, len(nums))
        return nums

    def _merge_sort(self, nums: List[int], start: int, end: int) -> None:
        if end - start > 1:
            # recurse
            mid = (start + end) // 2
            self._merge_sort(nums, start, mid)
            self._merge_sort(nums, mid, end)
            # merge
            left = nums[start:mid]
            right = nums[mid:end]
            left_ix = right_ix = 0
            len_left = len(left)
            len_right = len(right)
            while True:
                if left_ix == len_left:
                    nums[start:end] = right[right_ix:]
                    break
                if right_ix == len_right:
                    nums[start:end] = left[left_ix:]
                    break
                if left[left_ix] < right[right_ix]:
                    nums[start] = left[left_ix]
                    left_ix += 1
                else:
                    nums[start] = right[right_ix]
                    right_ix += 1
                start += 1
```

![](https://github.com/user-attachments/assets/958376c9-6a4d-4657-9455-1f2c756f2c37)

### Quicksort

```python
from random import randrange

class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        self.quicksort(nums, 0, len(nums) - 1)
        return nums

    def quicksort(self, nums: List[int], low: int, high: int) -> None:
        if low < high:
            # partition
            pivot_ix = randrange(low, high+1)
            pivot = nums[pivot_ix]
            nums[pivot_ix], nums[high] = nums[high], nums[pivot_ix]
            lower_elems_ix = low - 1
            for curr_ix in range(low, high):
                if nums[curr_ix] < pivot:
                    lower_elems_ix += 1
                    nums[lower_elems_ix], nums[curr_ix] = nums[curr_ix], nums[lower_elems_ix]
            nums[lower_elems_ix+1], nums[high] = nums[high], nums[lower_elems_ix+1]
            # recurse
            self.quicksort(nums, low, lower_elems_ix)
            self.quicksort(nums, lower_elems_ix+2, high)
```

![](https://github.com/user-attachments/assets/775f3773-f7ba-4a63-ad80-c5c7b21c74c7)

Uh oh, this version timed out on a test case where `nums` was an array containing 50,000 instances of the same value (i.e., `arr = [2] * 50_000`). I think I can deal with this by using a three-way partition instead of a two-way partition. Never tried this before, so this should be interesting...

```python
from random import randrange

class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        self._quicksort(nums, 0, len(nums) - 1)
        return nums

    def _quicksort(self, nums: List[int], low: int, high: int) -> None:
        if low < high:
            # partition
            pivot_ix = randrange(low, high+1)
            pivot = nums[pivot_ix]
            nums[pivot_ix], nums[high] = nums[high], nums[pivot_ix]
            lower_elems_ix = low
            higher_elems_ix = high - 1
            curr_ix = low
            while curr_ix <= higher_elems_ix:
                if nums[curr_ix] < pivot:
                    nums[lower_elems_ix], nums[curr_ix] = nums[curr_ix], nums[lower_elems_ix]
                    lower_elems_ix += 1
                    curr_ix += 1
                elif nums[curr_ix] > pivot:
                    nums[higher_elems_ix], nums[curr_ix] = nums[curr_ix], nums[higher_elems_ix]
                    higher_elems_ix -= 1
                else:
                    curr_ix += 1
            nums[lower_elems_ix], nums[high] = nums[high], nums[lower_elems_ix]
            # recurse
            self._quicksort(nums, low, lower_elems_ix - 1)
            self._quicksort(nums, higher_elems_ix + 1, high)
```

![](https://github.com/user-attachments/assets/e7b0ca9a-8a32-42d9-bb1e-e1fdf2dce3d1)

Well, it's slower than merge sort for these test cases, but it worked! I'll take it.
