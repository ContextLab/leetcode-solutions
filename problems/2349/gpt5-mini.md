# [Problem 2349: Design a Number Container System](https://leetcode.com/problems/design-a-number-container-system/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to support two operations: change(index, number) which assigns/replaces the number at an index, and find(number) which returns the smallest index currently holding that number (or -1). The key difficulty is efficiently getting the minimum index for a number while handling replacements (which make previous indices stale). A sorted structure per number (like a min-heap or balanced BST) makes sense. Removing arbitrary stale indices from a heap is costly, so lazy deletion (keep stale entries in the heap and skip them on find) is a common trick. Also maintain a map from index -> current number to validate heap top entries. There are at most 1e5 operations, so O(log n) per operation with lazy cleanup is fine.

## Refining the problem, round 2 thoughts
Use:
- index_to_number: dict mapping index -> current number
- number_to_heap: dict mapping number -> min-heap (list used with heapq) of indices that at some point were assigned that number

On change(index, number):
- If index had an old number, update index_to_number[index] = number (overwriting)
- Push index to number_to_heap[number] (lazy — do not try to remove from old number's heap)

On find(number):
- If number not in number_to_heap or heap empty -> return -1
- While heap is non-empty and the top index either no longer exists in index_to_number or now maps to a different number, pop it (lazy deletion).
- If heap empty after cleanup -> return -1 else return heap[0]

Edge cases:
- Reassigning the same index to the same number: we may push duplicate entries — handled lazily.
- Very large index/number values are fine because we only store at most the number of operations (<=1e5).
Time complexity:
- change: O(log k) for heap push, where k is size of that number's heap
- find: amortized O(log k) over many operations due to lazy deletions (every stale entry is popped at most once)
Space complexity:
- O(m) where m is number of change operations (because we store mapping and heaps with duplicates)

## Attempted solution(s)
```python
import heapq

class NumberContainers:
    def __init__(self):
        # map index -> current number
        self.index_to_number = {}
        # map number -> min-heap of indices that were assigned this number
        self.number_to_heap = {}

    def change(self, index: int, number: int) -> None:
        # Update the current number at index
        self.index_to_number[index] = number
        # Push index into the heap for this number (lazy deletion handles old entries)
        if number not in self.number_to_heap:
            self.number_to_heap[number] = []
        heapq.heappush(self.number_to_heap[number], index)

    def find(self, number: int) -> int:
        if number not in self.number_to_heap:
            return -1
        heap = self.number_to_heap[number]
        # Clean up stale entries: top index must currently map to `number`
        while heap:
            idx = heap[0]
            # If idx maps to number, it's valid; otherwise it's stale and popped
            if self.index_to_number.get(idx) == number:
                return idx
            heapq.heappop(heap)
        return -1
```
- Notes:
  - This uses lazy deletion: when an index is reassigned, we don't remove it from the old number's heap immediately. Instead, find() ignores stale indices by popping them until the top is valid.
  - Each stale index gets popped at most once, so amortized cost over all operations is acceptable.
  - Time complexity: change is O(log n) for pushing into a heap; find is amortized O(log n) for popping stale items (each stale entry popped once).
  - Space complexity: O(q) where q is total number of change calls (heaps may contain duplicates of indices across time).