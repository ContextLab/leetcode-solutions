# [Problem 1110: Delete Nodes And Return Forest](https://leetcode.com/problems/delete-nodes-and-return-forest/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- Another binary tree problem 🥳🌲🌳!
- Let's keep a list of the roots as we traverse the tree (breadth-first)
- If the current node is in `to_delete`, add both of its children to the "root list" (maybe...but what if they're *also* in the delete list?) and then either remove the node right away, or potentially add it to a list of to-be-deleted nodes
    - I think we can just delete it, as long as we enqueue its children (if they exist).  To delete the node, we want to set its parent's appropriate child to null...so I think we might want to resurect the `TreeNodeWithParentAndDirection` class from [yesterday's solution](https://github.com/ContextLab/leetcode-solutions/blob/main/problems/2096/jeremymanning.md).  I'll use a shorter name this time...that one was a bit clunky.
- Once all of the requested nodes are deleted, we can stop
- If the original root is *not* in `to_delete`, add that to the roots list too
- To account for the "children could be in the delete list too" issue, what about something like this:
  - In an initial pass through all nodes, convert to the updated tree structure (with parent/dir fields for each node)
  - Also create a hash table (keys: values; values: nodes)
  - Now loop through each value in `to_delete`:
      - Set the children's parents to None
      - Remove the pointer from that node's parent to the node
      - Remove the node from the hash table
  - Now loop through every node in the hash table one last time.  If its parent is None, add it to the root list

## Refining the problem, round 2 thoughts
- potential edge cases:
    - non-unique values: this is explicitly disallowed in the problem definition
    - repeated values in `to_delete`: this is also explicitly disallowed
    - delete every node in the tree: make sure this returns an empty list
    - deleting all but one node: make sure this returns the remaining node
    - deal with empty list-- not sure what the right syntax is...maybe `root` would be `None`?
- I think we can go with this solution...

## Attempted solution(s)
```python
class TreeNodePlus(TreeNode):
    def __init__(self, val=0, left=None, right=None, parent=None, dir=None):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent
        self.dir = dir

class Solution:
    def delNodes(self, root: Optional[TreeNode], to_delete: List[int]) -> List[TreeNode]:        
        if root is None:
            return []

        nodes = {}        
        # breadth-first search: convert nodes to TreeNodePlus instances and fill in the hash table
        queue = [TreeNodePlus(val=root.val, left=root.left, right=root.right)]
        while len(queue) > 0:
            node = queue.pop(0)
            nodes[node.val] = node

            # enqueue children
            if node.left is not None:
                left = TreeNodePlus(val=node.left.val, left=node.left.left, right=node.left.right, parent=node, dir='L')
                node.left = left
                queue.append(left)
            if node.right is not None:
                right = TreeNodePlus(val=node.right.val, left=node.right.left, right=node.right.right, parent=node, dir='R')
                node.right = right
                queue.append(right)
            
        # now delete all nodes in to_delete
        for val in to_delete:
            node = nodes[val]
            if node.parent is not None:
                if node.dir == 'L':
                    node.parent.left = None
                else:
                    node.parent.right = None

            if node.left is not None:
                node.left.parent = None
                node.left.dir = None

            if node.right is not None:
                node.right.parent = None
                node.right.dir = None

            nodes.pop(val)

        # now see which nodes are roots
        roots = []
        for node in nodes.values():
            if node.parent is None:
                roots.append(node)

        return roots
```
- Given test cases pass
- Let's try a few edge cases:
    - Empty tree: pass
    - Delete nodes that aren't in the actual tree: pass
    - Delete all nodes: pass
- Looks ok...submitting!

![Screenshot 2024-07-16 at 11 26 25 PM](https://github.com/user-attachments/assets/0446e1bd-b4cd-4869-a77a-75435cfed489)

- Solved!
- I'm guessing all of that copying is what's so slow...

