# [Problem 3510: Minimum Pair Removal to Sort Array II](https://leetcode.com/problems/minimum-pair-removal-to-sort-array-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This operation is deterministic at each step: you must merge the adjacent pair with the minimum sum (leftmost in ties). Repeating merges collapses the array into fewer elements; we can stop once the current array is non-decreasing. So we need to simulate the forced sequence of merges (but stop early when the array becomes non-decreasing) and return how many merges were required.

Naively simulating by rebuilding the array each time would be O(n^2) in the worst case. A standard technique for merging adjacent elements with a global "min adjacent pair" policy is to keep the adjacent-pair sums in a min-heap and update local neighbors when we actually perform a merge (like maintaining a linked list of elements and a heap of adjacent-pair sums). Also, to quickly know when the current list is non-decreasing we can maintain the number of "bad" adjacent pairs (where left > right) and update that count only for pairs affected by a merge.

So approach: doubly-linked nodes for elements, a heap of (sum, left_index_tie, left_node_id/ptr) to pick the leftmost minimal-sum adjacent pair; when merging two nodes, update prev/next pointers and update the bad-pair count only for affected adjacent pairs. Stop once bad_count == 0.

## Refining the problem, round 2 thoughts
Edge cases:
- Already non-decreasing array -> return 0 immediately.
- Single element -> 0.
- Negative numbers allowed (sums may be negative) — heap supports them.
- Need to ensure we skip stale heap entries (pairs where one of the nodes has been removed or the adjacency changed). Use an "alive" flag in nodes and verify left.next is still the original right node.

Complexity:
- Each merge reduces the number of nodes by 1; at most n-1 merges.
- For each merge we perform O(log n) heap operations (pop and up to two pushes).
- Updating bad-pair count is O(1) per merge.
Overall O(n log n) time and O(n) extra space.

Implementation details:
- Node holds value, original leftmost index (for tie-break), prev, next, alive flag.
- Heap entries: (sum, left_index, id(left), left_node). We include id(left) to detect stale entries if necessary.
- When popping from heap, validate that left.alive and left.next exists and is alive and that id(left) matches.
- When merging (left, right) -> new node with value left.val + right.val and index = left.index (leftmost), splice into the linked list, mark left/right dead, update heap for new adjacencies, and update bad_count by subtracting old bad statuses and adding new ones for pairs (left_prev,left), (left,right), (right,right_next) -> replaced by (left_prev, new), (new, right_next).

## Attempted solution(s)
```python
import heapq

class Node:
    __slots__ = ("val", "idx", "prev", "next", "alive")
    def __init__(self, val, idx):
        self.val = val
        self.idx = idx  # tie-break: leftmost original position
        self.prev = None
        self.next = None
        self.alive = True

class Solution:
    def minimumOperations(self, nums: list[int]) -> int:
        n = len(nums)
        if n <= 1:
            return 0

        # Build doubly linked list of nodes
        nodes = [Node(nums[i], i) for i in range(n)]
        for i in range(n - 1):
            nodes[i].next = nodes[i + 1]
            nodes[i + 1].prev = nodes[i]

        # initial bad (descending) adjacent pair count
        bad = 0
        for i in range(n - 1):
            if nodes[i].val > nodes[i + 1].val:
                bad += 1
        if bad == 0:
            return 0

        # heap of (sum, left_idx, left_id, left_node)
        heap = []
        for i in range(n - 1):
            left = nodes[i]
            right = nodes[i + 1]
            heapq.heappush(heap, (left.val + right.val, left.idx, id(left), left))

        ops = 0
        while heap:
            s, lidx, lid, left = heapq.heappop(heap)
            # validate still a valid adjacent pair
            if not left.alive:
                continue
            right = left.next
            if right is None or (not right.alive):
                continue
            if id(left) != lid:
                # stale entry (left has been replaced)
                continue

            # We will merge left and right
            left_prev = left.prev
            right_next = right.next

            # subtract contributions of old adjacent pairs to bad
            if left_prev is not None and left_prev.alive:
                if left_prev.val > left.val:
                    bad -= 1
            if left.val > right.val:
                bad -= 1
            if right_next is not None and right_next.alive:
                if right.val > right_next.val:
                    bad -= 1

            # create new node as merge of left and right
            new_val = left.val + right.val
            new_node = Node(new_val, left.idx)
            # splice new_node into list
            new_node.prev = left_prev
            new_node.next = right_next
            if left_prev is not None:
                left_prev.next = new_node
            if right_next is not None:
                right_next.prev = new_node

            # mark removed nodes dead
            left.alive = False
            right.alive = False

            # add contributions of new adjacent pairs to bad
            if left_prev is not None and left_prev.alive:
                if left_prev.val > new_node.val:
                    bad += 1
                # push (left_prev, new_node) into heap
                heapq.heappush(heap, (left_prev.val + new_node.val, left_prev.idx, id(left_prev), left_prev))
            if right_next is not None and right_next.alive:
                if new_node.val > right_next.val:
                    bad += 1
                # push (new_node, right_next) into heap
                heapq.heappush(heap, (new_node.val + right_next.val, new_node.idx, id(new_node), new_node))

            ops += 1
            if bad == 0:
                return ops

            # also, new_node could pair with neither side if isolated (single element left), in which case
            # if both neighbors are None -> array size 1 -> it's non-decreasing; but bad would be 0 already.
            # No need to push pair for new_node with left_prev or right_next if neighbor missing.

            # Note: If new_node has both neighbors, both pushes above ensure future merges considered.
        # Should not reach here without bad == 0, but just in case:
        return ops

# For LeetCode style usage:
# class Solution: (the above is already in correct shape)
# Example local test
if __name__ == "__main__":
    sol = Solution()
    print(sol.minimumOperations([5,2,3,1]))  # expected 2
    print(sol.minimumOperations([1,2,2]))    # expected 0
```

- Notes about the solution approach:
  - Use a doubly-linked list of nodes so that when we merge two adjacent nodes we can update neighbors in O(1) time.
  - Maintain a min-heap of adjacent-pair sums with tiebreak by the leftmost original index so we always pick the leftmost minimal-sum adjacent pair.
  - Keep a "bad" counter that tracks the number of adjacent inversions (pairs where left > right). Update only affected pairs when a merge happens, which is O(1) per merge.
  - Skip stale heap entries by validating that the left node is still alive and its next is the expected right node.
  - Time complexity: O(n log n) (at most n-1 merges, each causes at most O(log n) heap operations). Space complexity: O(n) for nodes and heap.