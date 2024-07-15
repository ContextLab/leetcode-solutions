# [Problem 2196: Create Binary Tree From Descriptions](https://leetcode.com/problems/create-binary-tree-from-descriptions/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- I think we can do this in a straightforward way
- Let's create a hash table to store the nodes:
    - Each time a new node is created, add it to the hash table
    - Each time an existing node is mentioned, update it accordingly
- At the end, we can find the root node by picking a node at random (maybe just the first one in the hash table?) and repeatedly following parents until the parent is `None`

## Refining the problem, round 2 thoughts
- Note that we'll need to add a "parent" attribute to the `TreeNode` definition.  I think this is OK...
    - Update: actually, I couldn't get it to run without re-defining a new class (I called it `TreeNodeWithParent`) that extends the `TreeNode` class.
- How should the "updating" work?
    - If the new `parent` is in the hash table, set its (left or right) child to the specified `child` node and update `child`'s parent.  If the `child` node is not in the hash table, create it.  (If the `parent` isn't in the hash table, create it first.)
    - This might be all that's needed...

## Attempted solution(s)
```python
# Definition for a binary tree node.
class TreeNodeWithParent(TreeNode):
    def __init__(self, val=0, left=None, right=None, parent=None):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent

class Solution:
    def createBinaryTree(self, descriptions: List[List[int]]) -> Optional[TreeNode]:
        table = {}
        for parent, child, isLeft in descriptions:
            if parent not in table:
                table[parent] = TreeNodeWithParent(val=parent)

            if child not in table:
                table[child] = TreeNodeWithParent(val=child)

            table[child].parent = table[parent]
            if isLeft:
                table[parent].left = table[child]
            else:
                table[parent].right = table[child]

        # get the first node in the description list
        node = table[descriptions[0][0]]
        while node.parent is not None:
            node = node.parent

        return node
```
- Given test cases pass
- Submitting...

![Screenshot 2024-07-14 at 10 44 32 PM](https://github.com/user-attachments/assets/e94b4947-ce9c-4131-8d61-d38d3ab2256a)

I'm a little surprised this is so slow, because I'm pretty sure it's an $O(n)$ solution (where $n$ is the number of nodes)...but oh well 🤷!

