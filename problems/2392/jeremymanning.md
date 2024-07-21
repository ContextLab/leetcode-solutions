# [Problem 2392: Build a Matrix With Conditions](https://leetcode.com/problems/build-a-matrix-with-conditions/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- My first thought is that we can figure out the "above/below" and "left/right" conditions separately.  So we "just" need a function that takes in a list of conditions and returns an ordering of $1...k$ (or None if there isn't any)
- The brute force solution would be to list all permutations of $1...k$ and then eliminate any that don't satisfy each condition in turn.  However, there's no way this approach would scale: there are $k!$ permutations of the numbers $1...k$, and so this approach would be $O(nk!)$ where $n$ is the number of conditions.
- Another approach would be to start with the first condition, and create all possible placements of those first two numbers that satisfy the first condition:
    - For a $k \times k$ matrix, there are $k - 1$ possibly placements of the "above" or "left' number and for each of those there are up to $k - 1$ placements of the "below" or "right" number.  So if we enumerate all possible placments of those first two numbers, we'd have $O(k^2)$ options.
    - We could do this for each option, and then merge the compatable options somehow.  This would be incredibly inefficient, though-- it'd be $O(nk^2)$ just to enumerate those possibilities, plus who knows how many steps to merge everything. There must be a better way...
- Another approach would be to somehow involve a stack.  We could make a "guess" about the positions of the numbers based on one condition.  Then when we encounter the next condition, if there's no possible way to satisfy it, we'd need to backtrack (pop the stack?) and try placing the previous condition's numbers somewhere else.  I'm not totally sure yet how this would work...
- Something else I'm thinking of is that not all of the conditions necessarily interact.  E.g., suppose we have `[[1, 2], [2, 3], [4, 5], [5, 6]]`.  The placements of 1, 2, and 3 don't depend on the placements of 4, 5, or 6-- so the two sequences can be optimized independently.  One potential way to track this would be using a list of sets.  At first we start a single set of numbers containing just the first condition's numbers.  Then, for each new condition:
    - If either of the numbers are in an existing set, add both numbers to that set
    - If the numbers appear in two different sets (e.g., one appears in one set and the other appears in a different set), we need to merge both sets
    - If neither number appears in any set, we need to start a new set with just those numbers.
    - After looping through all conditions, now we have distinct sets of numbers that can be optimized independently.
    - Note: I'm not totally sure what this would actually buy us...maybe more efficient?  But it might also take any time we would save to do this partitioning.
- Another idea: what if we maintain a hash table where the keys are the numbers $1...k$ and the values are lists of numbers that need to appear below/right of the given key.  (Note: or maybe we want to do this in the opposite way by tracking numbers that need to be above/left of the given key?  Come back to this...)
    - Creating this would be straightforward:
        - Start with `requirements = {i: [] for i in range(1, k + 1)}`
        - For each condition `c`, update the hash table using: `requirements[c[0]].append(c[1]]`  (Note: to do the "reverse" tracking we'd just use `requirements[c[1]].append(c[0]]`)
    - Now maybe we start with...what?  Just go in order from $1...k$?  Let's say we start a list as `order = [1]`.
        - Next, maybe we go through each key, `i`, but going through the `order` list and placing it at the earliest position where the given constraints are satisfied?
        - Checking those constraints might be expensive...e.g., if `a` is in `requirements[x]`, then we know we want to place `a` after `x`.  But how *much* after `x`?  Can we mark in some way that `x` is the "early bound" of where `a` can be shifted?  Or...maybe it's fine if we only allow prepending, inserting, or appending operations, since the relative positions of anything already placed in the list will remain unchanged.
        - Maybe we want to do some sort of updating operation...like if `a` needs to be before `b` and `b` needs to be before `c`, then even though it might not appear in the conditions, it might be useful to have `c` in the list of numbers that `a` needs to be in front of.  This also makes me realize that we should use sets, not lists-- because each number only needs to appear in the values for some key at most once.
            - Then again, this could be expensive...every time we add a new instruction, we need to go through the full hash table, which takes $O(k)$ steps.  But...maybe it's necessary?  Or maybe it'll save time in some other part of the algorithm?
- Ok, so what about something like this:
```
<Create the requirements hash table as described above>
order = [1]
for k in range(2, k + 1):
    i = 0  # everything to the left of this has k in its requirements
    while i < len(orders) - 1:
        if k in requirements[orders[i]]:
            i += 1
    <insert k into orders at position i>
<now we need to do some sort of check to verify that no conditions are violated...this could potentially involve going through another k^2 steps to check whether anything prior to the position of k appears in requirements[k]-- if so, return None>
return order
```
- Another thought: suppose that a given number, `n` *never* appears in an instruction.  Then it doesn't matter where it goes.  It'd have `len(requirements[n])` equal to 0.
- Once we've placed a number, .... ah.  Actually: I'm pretty sure this is a [topological sort problem](https://en.wikipedia.org/wiki/Topological_sorting).  I'm going to cheat a bit and look up the algorithm on wikipedia...
  
![Screenshot 2024-07-20 at 11 46 39 PM](https://github.com/user-attachments/assets/db68d6ac-b2b8-4fee-aa00-f3894f4b4688)
- Ok, so this is actually sort of similar to what I came up with.  The key thing I was stuck on is what happens once we place a number-- do we then have to keep track of it?  Or can we ignore it when placing the other numbers?  Topological sort says we can just ignore it.
- So I think (for each set of instructions) we just need to apply topological sort.  If that fails, there is no solution so we return an empty matrix.
             
## Refining the problem, round 2 thoughts
- Once we have the sort order for the rows and columns, we just initialize a matrix of zeros.
- Then, for each row (`i`) and column (`j`) we fill in the entries of the matrix with the corresponding values.

## Attempted solution(s)
```python
class Solution:
    def buildMatrix(self, k: int, rowConditions: List[List[int]], colConditions: List[List[int]]) -> List[List[int]]:
        def topologicalSort(conds, k):
            # after some experimenting, i'm realizing we need to track both a before *and* an after requirements
            before = {i: set() for i in range(1, k + 1)}
            after = {i: set() for i in range(1, k + 1)}
            for key, val in conds:
                before[key].add(val)
                after[val].add(key)
            
            order = []
            queue = [key for key, val in after.items() if len(val) == 0]

            while len(queue) > 0:
                x = queue.pop(0)
                order.append(x)
                # remove all references from x to its neighbors
                for y in before[x]:
                    after[y].remove(x)
                    if len(after[y]) == 0:
                        queue.append(y)
            
            return None if len(order) < k else order

        row_order = topologicalSort(rowConditions, k)
        if row_order is None:
            return []

        col_order = topologicalSort(colConditions, k)
        if col_order is None:
            return []

        matrix = [[0 for _ in range(k)] for _ in range(k)]

        row_pos = {num: i for i, num in enumerate(row_order)}
        col_pos = {num: i for i, num in enumerate(col_order)}

        for num in range(1, k + 1):
            matrix[row_pos[num]][col_pos[num]] = num

        return matrix
```
- ok...not shown is a bunch of trying an failing.  In the topological sort implementation, I thought I just needed to track a single dictionary with lists (sets) of numbers that had to come *after* each given item (building this up from the list of conditions).  But actually, once we place an item, we also have to know if that item is referenced in *other* number's sets as needed to come *before* the other number.  So to solve this, I needed to use two hash tables (one listing requirements of $a$ coming *before* $b$ and the other listing requirements of $b$ coming *after* $a$).  I could have instead solved this by looping through every key's list repeatedly, but that would have been very inefficient.
- after that confusion, the test cases now pass.  and...I'm out of time to work on this, so i'm just going to cross my fingers and submit 🤞... 😬

![Screenshot 2024-07-21 at 12 46 24 AM](https://github.com/user-attachments/assets/6a7db5ec-4542-444e-9f85-7c6972c6d9be)
- Meh...slow again 🙃
- Some things one "could" optimize (if one were so inclined):
    - Using the `deque` object instead of a list as the queue.  Actually...that's not so bad to implement.  Out of curiousity, let's see if that "just works"...

### Revised solution using `dequeue`
```python
from collections import deque

class Solution:
    def buildMatrix(self, k: int, rowConditions: List[List[int]], colConditions: List[List[int]]) -> List[List[int]]:
        def topologicalSort(conds, k):
            # after some experimenting, i'm realizing we need to track both a before *and* an after requirements
            before = {i: set() for i in range(1, k + 1)}
            after = {i: set() for i in range(1, k + 1)}
            for key, val in conds:
                before[key].add(val)
                after[val].add(key)
            
            order = []
            queue = deque([key for key, val in after.items() if len(val) == 0])

            while len(queue) > 0:
                x = queue.popleft()
                order.append(x)
                # remove all references from x to its neighbors
                for y in before[x]:
                    after[y].remove(x)
                    if len(after[y]) == 0:
                        queue.append(y)
            
            return None if len(order) < k else order

        row_order = topologicalSort(rowConditions, k)
        if row_order is None:
            return []

        col_order = topologicalSort(colConditions, k)
        if col_order is None:
            return []

        matrix = [[0 for _ in range(k)] for _ in range(k)]

        row_pos = {num: i for i, num in enumerate(row_order)}
        col_pos = {num: i for i, num in enumerate(col_order)}

        for num in range(1, k + 1):
            matrix[row_pos[num]][col_pos[num]] = num

        return matrix
```

![Screenshot 2024-07-21 at 12 49 47 AM](https://github.com/user-attachments/assets/c3e5a93e-9ac0-4f71-82bd-a96b093e4fb0)

Huh, ok, so it does seem to make a difference.  Good to know!  Other things to optimize:
  - There's definitely a way to improve memory use (by not "double storing" both the `before` and `after` hash tables).  That would roughly halve memory use.
  - I can't think of a non-topological sort solution, but maybe there's something?



