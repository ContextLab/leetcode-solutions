# [Problem 703: Kth Largest Element in a Stream](https://leetcode.com/problems/kth-largest-element-in-a-stream/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- Kind of a fun one!
- Inside the class, let's keep a running (sorted) list of the $k$ largest elements
- When the class is initialized, we'll need to sort `nums` in descending order and set `self.k_largest` to the $k$ largest numbers (from largest to smallest)
- When a number is added:
    - If the number is less than or equal to the smallest number in `self.k_largest` (i.e., `self.k_largest[-1]`), return `self.k_largest[-1]`
    - If the number is (strictly) greater than the smallest number in `self.k_largest`:
        - Drop the current $k^\mathrm{th}$ largest number (`self.k_largest = self.k_largest[:-1]`)
        - Loop through each element in the sequence until we find a place to insert `val`:
        ```python
        inserted = False
        for i, x in enumerate(self.k_largest):
            if x <= val:
                self.k_largest = [*self.k_largest[:i], val, *self.k_largest[i:]]
                inserted = True
                break
        if not inserted:
            self.k_largest.append(val)
        return self.k_largest[-1]
        ```

## Refining the problem, round 2 thoughts
- One thing I'm not sure of: are we guaranteed to get at least $k$ numbers when the class is intialized? I'll account for this (by appending -1's) just in case
- Nothing particularly tricky here...let's just implement the solution

## Attempted solution(s)
```python
class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k_largest = list(sorted(nums, reverse=True))[:k]
        if len(self.k_largest) < k:
            self.k_largest.extend([-1] * (k - len(nums)))

    def add(self, val: int) -> int:
        if val <= self.k_largest[-1]:
            return self.k_largest[-1]
        self.k_largest.pop()

        inserted = False
        for i, x in enumerate(self.k_largest):
            if x <= val:
                self.k_largest = [*self.k_largest[:i], val, *self.k_largest[i:]]
                inserted = True
                break
        if not inserted:
            self.k_largest.append(val)
        return self.k_largest[-1]
```
- The given test case passes
- It's somewhat annoying to create new test cases, but let's see...
    - `["KthLargest","add","add","add","add","add"], [[5,[4,5,8,2]],[3],[5],[10],[9],[4]]`: pass
    - `["KthLargest","add","add","add","add","add","add","add"], [[6,[0,20,4,5,8,2]],[3],[21],[3],[5],[10],[9],[4]]`: pass
- I think we're good...submitting...

![Screenshot 2024-08-11 at 10 07 16 PM](https://github.com/user-attachments/assets/1c0e4751-5c7d-4c94-82e3-561630121aa4)

🤦 Ah-- I misread the instructions (I thought we couldn't have negative numbers).  Easy fix...

```python
class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k_largest = list(sorted(nums, reverse=True))[:k]
        if len(self.k_largest) < k:
            self.k_largest.extend([-float("inf")] * (k - len(nums)))

    def add(self, val: int) -> int:
        if val <= self.k_largest[-1]:
            return self.k_largest[-1]
        self.k_largest.pop()

        inserted = False
        for i, x in enumerate(self.k_largest):
            if x <= val:
                self.k_largest = [*self.k_largest[:i], val, *self.k_largest[i:]]
                inserted = True
                break
        if not inserted:
            self.k_largest.append(val)
        return self.k_largest[-1]
```

![Screenshot 2024-08-11 at 10 09 06 PM](https://github.com/user-attachments/assets/90a446aa-9d5e-4501-862a-c0658fa55603)

Hah!  Did I win the prize for the slowest solution?  In any case, I'll take it: solved 🥳!

- Note: a heap is definitely the way to solve this efficiently.  I could have used the built-in `heapq` (from the `heapq` module).
- Let's see if I can get it to work quickly...

```python
import heapq

class KthLargest:
    def __init__(self, k: int, nums: List[int]):
        self.k = k
        self.k_largest = nums
        heapq.heapify(self.k_largest)
        while len(self.k_largest) > self.k:
            heapq.heappop(self.k_largest)

    def add(self, val: int) -> int:
        heapq.heappush(self.k_largest, val)
        while len(self.k_largest) > self.k:
            heapq.heappop(self.k_largest)
        return self.k_largest[0]
```
- That took a some hacking around based on the [heapq documentation](https://docs.python.org/3/library/heapq.html) but I got it to run...
- Given test cases pass; submitting...

![Screenshot 2024-08-11 at 10 18 27 PM](https://github.com/user-attachments/assets/737aaadb-8bfe-4c08-8a27-238d815fa96a)

There we go-- quite a lot faster!


