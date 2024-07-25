# [Problem 912: Sort an Array](https://leetcode.com/problems/sort-an-array/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- My first thought was that we could just return `sorted(nums)`
- But...I'm seeing that we're supposed to solve this with no built in functions.  They want an algorithm with $O(n \log n)$ time complexity and "the smallest space complexity possible," which would be $O(1)$ space.  Off the top of my head, I remember a few sorting algorithms:
    - Bubble sort, which has $O(n^2)$ time complexity and $O(1)$ space complexity-- so it's out, because time complexity is too poor
    - Merge sort, which I believe has $O(n \log n)$ time complexity and...maybe $O(n)$ space complexity?
    - Quick sort, which I think *also* has $O(n \log n)$ time complexity and $O(n)$ space complexity
- So none of these are going to work.  We need something with $O(n \log n)$ time complexity and $O(1)$ space complexity.
- I'm just going to look up a list of sorting algorithms.  I found a list [here](https://www.bigocheatsheet.com/):

![Screenshot 2024-07-24 at 11 26 07 PM](https://github.com/user-attachments/assets/614e6a15-0f52-4378-b435-fc006b3f06da)

## Refining the problem, round 2 thoughts
- It looks like what we need is heapsort.  Other than remembering that I've learned about heapsort at some point (e.g., I remember the name) I have absolutely no recollection of how it works.  I'm guessing we need to build a heap (though I can't remember how to do this).  And I think the "point" of a heap is that as you "pop" from a heap you always get the maximum (for a max heap) or minimum (for a min heap) value, so sorting is just a matter of "heapifying" the list and then popping from it until all elements are gone.  But I'm going to need to look up how to implement this.  From [Wikipedia](https://en.wikipedia.org/wiki/Heapsort):

![Screenshot 2024-07-24 at 11 30 16 PM](https://github.com/user-attachments/assets/d6391a65-bbe5-4574-b4e2-323e15480daa)

- Ok...so let's turn this into Python!
    - Note 1: I'll replace `a` with `nums` and compute `count` as `len(nums)` rather than passing it in as input; otherwise I'll do a straight copy of the pseudocode.
    - Note 2: In the same Wikipedia page, the `iLeftChild` function is defined as follows (so I'll write this up too):
![Screenshot 2024-07-24 at 11 40 25 PM](https://github.com/user-attachments/assets/66f75bb0-3514-463b-ab69-d821ba7f4adc)

## Attempted solution(s)
```python
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        def iLeftChild(i):
            return 2 * i + 1
        
        count = len(nums)
        start = count // 2
        end = count
    
        while end > 1:
            if start > 0:
                # Heap construction
                start -= 1
            else:
                # Heap extraction
                end -= 1
                nums[end], nums[0] = nums[0], nums[end]
    
            # SiftDown(nums, start, end)
            root = start
            while iLeftChild(root) < end:
                child = iLeftChild(root)
                if child + 1 < end and nums[child] < nums[child + 1]:
                    child += 1
                if nums[root] < nums[child]:
                    nums[root], nums[child] = nums[child], nums[root]
                    root = child
                else:
                    break

        return nums
```

- Given test cases pass
- I'm just going to submit...

![Screenshot 2024-07-24 at 11 41 48 PM](https://github.com/user-attachments/assets/2cb51d71-846a-43ba-b312-96e8e5d23d78)

- Out of curiosity, how much better is the "built-in" version?
```python
class Solution:
    def sortArray(self, nums: List[int]) -> List[int]:
        return sorted(nums)
```

![Screenshot 2024-07-24 at 11 42 53 PM](https://github.com/user-attachments/assets/1f23f599-4dcc-45f1-a230-8fefcbc92326)

Well then...




