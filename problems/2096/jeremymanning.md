# [Problem 2096: Step-By-Step Directions From a Binary Tree Node to Another](https://leetcode.com/problems/step-by-step-directions-from-a-binary-tree-node-to-another/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- I think we can do something like this:
    - Do a breadth-first search to find the start and end nodes
    - As we traverse the tree, we'll copy it-- but instead of using the `TreeNode` class, we'll define a new class that lets us store both the parent of each node (like [yesterday's daily problem](https://leetcode.com/problems/create-binary-tree-from-descriptions/description/?envType=daily-question)) *and* whether the current node is the left or right child of its parent.
    - Once we find both the start and end nodes, we can stop this process (but in the worst case, we'll need to traverse the full tree, which will take $O(n)$ time, where $n$ is the number of nodes-- i.e., we need to visit each node up to one time)
    - Next we need to find a common ancester of both nodes:
        - Lets start from the starting node.  Just keep following parents until we get to the root.  Store the value of (parent) node that we pass and also its depth (e.g., number of levels up from the starting node).
        - Next let's start from the ending node.  Again, keep following parents until we get to the root (in the worst case).  But this time, things work a little differently:
            - each time we visit a node, check if it's on the path from the starting node back to the root.  once we hit a common ancestor we can stop looking.
            - we'll need to construct the path from the common ancestor down to the end node in reverse order (we could just prepend instructions as we go).  if the current node is the right child of its parent, we prepend an "R" to the directions, and so on, until we get to the common ancestor.
        - Finally, prepend $n$ `U`s to the directions, where $n$ is the number of "levels up" from the starting node to the common ancestor.
    - Now we can just return the directions.

## Refining the problem, round 2 thoughts
- We will need to account for the possibility that the start and end nodes are the same, and/or that one (or both) is the root of the tree (in which case "0" `'U'` instructions are needed)
- Ok, let's go with this...

## Attempted solution(s)
```python
class TreeNodeWithParentAndDirection(TreeNode):
    def __init__(self, val=0, left=None, right=None, parent=None, dir=None):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent
        self.dir = dir

class Solution:
    def getDirections(self, root: Optional[TreeNode], startValue: int, destValue: int) -> str:
        start_node = None
        dest_node = None
        
        # breadth-first search
        queue = [TreeNodeWithParentAndDirection(val=root.val, left=root.left, right=root.right)]
        while (len(queue) > 0) and (start_node is None or dest_node is None):
            next_node = queue.pop(0)
            if next_node.val == startValue:
                start_node = next_node

            if next_node.val == destValue:
                end_node = next_node

            #enqueue the left and right children
            if next_node.left is not None:
                queue.append(TreeNodeWithParentAndDirection(val=next_node.left.val, left=next_node.left.left, right=next_node.left.right, parent=next_node, dir='L'))
            if next_node.right is not None:
                queue.append(TreeNodeWithParentAndDirection(val=next_node.right.val, left=next_node.right.left, right=next_node.right.right, parent=next_node, dir='R'))

        # find a path from the start_node back to the root (store in a hash table-- i think this will be better than a list)
        start_to_root = {}
        node = start_node
        count = 0
        while node.parent is not None:
            start_to_root[node.val] = count
            node = node.parent
            count += 1
        
        start_to_root[node.val] = count

        # now find a path from end_node back to the closest node in start_to_root
        node = end_node
        directions = ''
        while node.val not in start_to_root:
            directions = node.dir + directions
            node = node.parent

        return 'U' * start_to_root[node.val] + directions
```
- Given test cases pass
- Let's make up another (larger) tree:
    - `root = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]`, `startValue = 3`, `destValue = 6`: pass
    - `root = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]`, `startValue = 21`, `destValue = 14`: pass
- Ok, I think we've got this; submitting...

![Screenshot 2024-07-15 at 11 59 00 PM](https://github.com/user-attachments/assets/1f860f6c-8f50-4a55-a1ba-f9e588db4d25)

- Solved!  I'm a little surprised that (a) the runtime is worse than most other solutions-- I'm pretty sure this solution is $O(n)$, and also that (b) the memory use is *better* than most solutions (since we end up potentially copying the entire tree).  But (like with yesterday's puzzle) maybe there's an overhead to creating new instances of a class?
