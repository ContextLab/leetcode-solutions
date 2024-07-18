# [Problem 1530: Number of Good Leaf Nodes Pairs](https://leetcode.com/problems/number-of-good-leaf-nodes-pairs/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- One thing I'm sure of is that there has to be a shortcut here, aside from brute-force computing every shortest path
- I'm not seeing any obvious solution off the top of my head
- I'm wondering if it'd be useful to traverse the tree in some way and keep track of the depth of each node.  Then we could...what?
    - If the depth is .... ah, I misread the problem.  We only have to worry about *leaf* nodes.  So actually, this is much easier than I had initially expected (I thought we had to look for paths between *any* pair of nodes)
- Ok, so with this new-found knowledge, let's see what we can do:
    - First, we need to find leaf nodes.  We could do this by traversing the tree and finding nodes with no children (those are the leaves)
    - The shortest path between the nodes involves finding the closest common ancestor.  If the ancestor is $d_1$ nodes above node 1 and $d_2$ nodes above node 2, then the shortest path is $d_1 + d_2$ steps long.  Some observations:
        - If either $d_1$ or $d_2$ is greater than `distance`, we can ignore that pair
- It's not super efficient (but maybe it'll be OK, because the max number of notes is 1024?), but what if we do something like this:
    - Find the leaves (DFS or BFS) and store them in a hash table.  We can add pointers to the parents as we go so that we can easily find the common ancester.  Let's also give each node a unique ID so that we can distinguish it from other nodes with the same value.
    - For each pair of leaves (need to do this in a nested loop):
        - Find the common ancestor (note: need to write this!)
        - Keep track of how many steps it takes to get to the common ancester from each leaf
        - If the sum of those distances is less than or equal to `distance`, increment a counter by 1 for that pair
- Finding the common ancestor could go like this:
    - For the first leaf node, climb the tree back to the root, keeping track of the unique IDs of each node in a hash table (keys: unique ID; values: steps from first leaf node)
    - Now for the second leaf node, keep climbing the tree (keep track of the number of steps) until we find a node with a unique ID in the hash table
    - Then we just return the sum of the distances to the common ancestor (i.e., the length of the shortest path between the nodes)

## Refining the problem, round 2 thoughts
- Lets define a new class for the nodes (that seems to have been working conveniently for these problems).  In addition to value and left/right children, let's add attributes for the node's parent and a unique ID
- Any tricky edge cases to think about?
    - If there's only 1 node, there are no pairs so we just return 0.  But this is fine, since the body of the nested loop that goes through pairs of nodes just won't ever run.
    - If the depths of all leaves are less than half of `distance`, we can just return the total number of pairs (i.e., for `n` leaves this is `(n^2 - n) / 2`).  But I'm not sure it's worth coding in this special case.
- Ok, let's code it!

## Attempted solution(s)
```python
class TreeNodeParID(TreeNode):
    current_ID = 0
    
    def __init__(self, val=0, left=None, right=None, parent=None):
        self.val = val
        self.left = left
        self.right = right
        self.parent = parent
        self.ID = TreeNodeParID.current_ID

        TreeNodeParID.current_ID += 1

class Solution:
    def countPairs(self, root: TreeNode, distance: int) -> int:

        # find the leaves and add parent attributes.  i'll use DFS since i've been using BFS for the past few problems.  gotta keep things interesting!
        stack = [TreeNodeParID(val=root.val, left=root.left, right=root.right)]
        leaves = []
        
        while len(stack) > 0:
            node = stack.pop()
            
            if node.left is not None:
                node.left = TreeNodeParID(val=node.left.val, left=node.left.left, right=node.left.right, parent=node)
                stack.append(node.left)
            
            if node.right is not None:
                node.right = TreeNodeParID(val=node.right.val, left=node.right.left, right=node.right.right, parent=node)
                stack.append(node.right)
            
            # is this a leaf?
            if not node.left and not node.right:
                leaves.append(node)

        # now loop through every pair of leaves and find the common ancestors
        good_node_count = 0
        for i, a in enumerate(leaves):
            # go from node a to the root, tracking depth
            path_to_root = {a.ID: 0}
            
            x = a
            d1 = 1
            while x.parent is not None:
                x = x.parent
                path_to_root[x.ID] = d1
                d1 += 1

            for b in leaves[(i + 1):]:
                # go from node b to anything in path_to_root
                if b.ID in path_to_root:
                    if path_to_root[b.ID] <= distance:
                        good_node_count += 1
                    continue
                                    
                x = b
                d2 = 1
                while (x.parent is not None) and (d2 <= distance): #stop early if path from b to common ancestor is greater than distance
                    x = x.parent
                    if x.ID in path_to_root:
                        if path_to_root[x.ID] + d2 <= distance:
                            good_node_count += 1
                        break
                    d2 += 1

        return good_node_count
```
- Got stuck for a bit there-- I had an extra indent in the `return` statement, which meant the function was returning after the first iteration of the outer loop 😵!
- Ok, now that I've unindented that line, all given test cases pass
- Other tests:
    - `root = [1,2,3,4,5,6,7,8, 9, null, 10, null, 11, 12, null], distance = 3`: pass
    - `root = [1,2,3,null,5,null,7,8, 9, null, 10, null, 11, 12, null], distance = 5`: pass
- Seems to work; submitting...

![Screenshot 2024-07-18 at 12 55 15 AM](https://github.com/user-attachments/assets/bd64170f-8891-41d4-a36d-a45b33e71922)
- Ouch, that's slow!
- But...solved 🥳!


