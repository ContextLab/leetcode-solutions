# [Problem 1381: Design a Stack With Increment Operation](https://leetcode.com/problems/design-a-stack-with-increment-operation/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need a stack with push, pop, and an increment(k, val) that increments the bottom k elements. A naive approach is to store the stack in a list and when increment(k, val) is called, loop over the first k elements and add val — that would be O(k) per increment. Given constraints (maxSize and number of calls up to 1000) that might pass, but it's not ideal if increments are frequent and k is large.

I recall a trick: apply increments lazily. Keep an auxiliary array inc[] where inc[i] stores an extra value to add to stack[i] and propagate when popping. For increment(k, val) we can just do inc[min(k, size)-1] += val. When popping index i, we add inc[i] to the popped value and pass inc[i] down to inc[i-1] so the accumulated increments affect the remaining items. That makes increment O(1) and pop O(1).

Edge cases: calling increment when stack is empty (do nothing), pushing when at maxSize (ignore), popping when empty returns -1. Need to ensure propagation of increments happens correctly and clear used inc entries.

## Refining the problem, round 2 thoughts
The lazy increment approach yields O(1) push, pop, and increment, which is optimal here. Memory usage is O(maxSize) for both the stack and the inc array. Implementation details:
- Use a list for values and a list of same length for pending increments.
- push: if current size < maxSize, append value and append 0 to inc (or keep inc fixed length and set by index).
- pop: let i = size-1, pop value and its inc[i]; add inc[i] to the value; if i > 0 propagate inc[i] to inc[i-1]; set inc[i] = 0 (if using fixed-size array) to avoid stale data.
- increment(k, val): if size == 0 do nothing; otherwise inc[min(k, size)-1] += val.

Consider using a fixed-size inc array initialized to zeros for simplicity, but simply appending zeros when pushing also works. Make sure to handle the min(k, size) correctly.

Time complexity: push O(1), pop O(1), increment O(1). Space complexity: O(maxSize).

## Attempted solution(s)
```python
class CustomStack:
    def __init__(self, maxSize: int):
        # store values in a list
        self.maxSize = maxSize
        self.stack = []
        # inc[i] stores extra increment to apply to stack[i] and below
        self.inc = [0] * maxSize

    def push(self, x: int) -> None:
        if len(self.stack) < self.maxSize:
            self.stack.append(x)
        # else ignore as per problem statement

    def pop(self) -> int:
        if not self.stack:
            return -1
        idx = len(self.stack) - 1
        # apply pending increment for this index
        res = self.stack.pop() + self.inc[idx]
        # propagate increment downwards
        if idx > 0:
            self.inc[idx - 1] += self.inc[idx]
        # clear this slot's increment
        self.inc[idx] = 0
        return res

    def increment(self, k: int, val: int) -> None:
        size = len(self.stack)
        if size == 0:
            return
        idx = min(k, size) - 1
        if idx >= 0:
            self.inc[idx] += val
```
- Approach: Use a stack list for values and a fixed-size inc array to record lazy increments. increment(k, val) updates inc[min(k, size)-1] by val so all bottom k elements logically get val. On pop, the increment for the popped position is added to the popped value and propagated to the next lower index so remaining elements retain the increment.
- Time complexity: push O(1), pop O(1), increment O(1).
- Space complexity: O(maxSize) for the stack storage and inc array.
- Important details: Always propagate the inc for the popped index to the next lower index before clearing the slot, otherwise the increment would be lost for remaining items. Guard against empty stack on pop and increment.