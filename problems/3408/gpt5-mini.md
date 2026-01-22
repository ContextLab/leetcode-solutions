# [Problem 3408: Design Task Manager](https://leetcode.com/problems/design-task-manager/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need a data structure that supports:
- insert task (userId, taskId, priority),
- update priority of an existing taskId,
- remove a taskId,
- extract the global highest-priority task (tie-break by larger taskId) and return its userId and remove it.

This looks like a priority-queue problem but with updates/removals by taskId. A typical approach is:
- maintain a max-heap keyed by (priority, taskId) with tie-breaker on taskId,
- keep a map from taskId -> (userId, currentPriority) to validate whether a heap entry is up-to-date,
- for edits/removals we lazy-invalidate old heap entries by updating/deleting the mapping and pushing a new entry (for edit) or leaving stale entries to be skipped when popped.

Alternative is a balanced tree keyed by (priority, taskId) plus a map from taskId -> node handle to support O(log n) updates; but Python doesn't have a standard balanced tree with handles. So heap + lazy deletion is simplest and efficient.

## Refining the problem, round 2 thoughts
- Use Python's heapq (min-heap) and push (-priority, -taskId, taskId) so the heap top corresponds to maximum priority and, for equal priority, maximum taskId.
- Maintain dict: taskId -> (userId, priority). On add/edit, update dict and push a new heap entry. On rmv, delete from dict (the heap entry becomes stale).
- On execTop, pop heap entries until we find one whose taskId is present in dict and its priority matches the mapping (so it's current). Then remove it from dict and return its userId. If heap exhausted -> return -1.
- Complexity: each heap push/pop is O(log n). Because we only lazily delete, total heap size could grow up to number of operations (<= 2e5) — still fine.
- Edge cases: execTop when no tasks (return -1). Guarantees in prompt say taskId operations are valid, but we still check existence on rmv defensively.

This approach is memory- and time-efficient for constraints.

## Attempted solution(s)
```python
import heapq

class TaskManager:
    def __init__(self, tasks):
        # heap entries: (-priority, -taskId, taskId)
        self.heap = []
        # mapping: taskId -> (userId, priority)
        self.tasks = {}
        for userId, taskId, priority in tasks:
            self.tasks[taskId] = (userId, priority)
            heapq.heappush(self.heap, (-priority, -taskId, taskId))

    def add(self, userId: int, taskId: int, priority: int) -> None:
        # taskId guaranteed not to exist
        self.tasks[taskId] = (userId, priority)
        heapq.heappush(self.heap, (-priority, -taskId, taskId))

    def edit(self, taskId: int, newPriority: int) -> None:
        # taskId guaranteed to exist
        userId, _ = self.tasks[taskId]
        self.tasks[taskId] = (userId, newPriority)
        heapq.heappush(self.heap, (-newPriority, -taskId, taskId))

    def rmv(self, taskId: int) -> None:
        # taskId guaranteed to exist; remove from mapping to mark stale
        if taskId in self.tasks:
            del self.tasks[taskId]

    def execTop(self) -> int:
        # Pop until we find a non-stale up-to-date entry
        while self.heap:
            negp, negtid, tid = self.heap[0]
            # if tid no longer in tasks -> stale, discard
            if tid not in self.tasks:
                heapq.heappop(self.heap)
                continue
            userId, cur_priority = self.tasks[tid]
            # check if priority matches current priority
            if cur_priority == -negp:
                # valid top
                heapq.heappop(self.heap)
                del self.tasks[tid]
                return userId
            else:
                # stale priority entry, discard
                heapq.heappop(self.heap)
        return -1
```
- Notes about the solution approach:
  - We use a max-heap behavior via tuples (-priority, -taskId, taskId) so the heap top corresponds to the task with highest priority, and among ties the highest taskId.
  - A dictionary taskId -> (userId, priority) stores the current state. Old heap entries become stale after edits/removals; they are lazily skipped when popped.
  - This yields O(log n) time per heap push/pop; each operation (add/edit/rmv/execTop) does at most O(log n) amortized work. Space is O(n + k) where n is current tasks and k is number of stale entries still in heap (bounded by number of operations, <= 2e5).
  - execTop returns -1 when no valid tasks remain.