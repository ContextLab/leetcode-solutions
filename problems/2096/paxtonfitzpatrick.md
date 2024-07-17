# [Problem 2096: Step-By-Step Directions From a Binary Tree Node to Another](https://leetcode.com/problems/step-by-step-directions-from-a-binary-tree-node-to-another/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- I think this is going to involve moving upward from the start (destination?) node through the tree until we either (A) reach the destination (start?) node, (B) reach the closest (furthest from root) node that's a common ancestor of the two, or reach the top of the tree, then working backwards down one of the two paths to the destination (start?) node.
- To find a common ancestor, we could potentially:
  - start from the start node and go all the way to the root, then start from the destination and go until we reach the root or one of the nodes that was in the start node's path to the root.
  - do the same thing except go from the destination node to the root first
    - the worst case for either of these would be if the 2nd node whose path to the root we figure out "below" the first one in the same "branch" of the tree, as in example 2
  - alternate back and forth between moving 1 parent closer to the root from the two until we find one that's in the other's path.

---

- Came back to this the next day and re-read the problem. Realized we're not given the tree as a 2d array like yesterday's problem, just the root node. So we'll have to start searching from there, not the start or destination node.
- I think this is going to involve finding the two nodes, figuring out their closest common ancestor, and constructing the path that way.
- I feel like this is calling for either BFS or DFS to find the nodes... but I'm not sure which would be better. The one heuristic I've heard is to use BFS when trying to find the shortest path between two nodes and DFS when trying to determine whether a path between them exists. But we're not really doing either of those in this case cause we're not starting from one of the two nodes. Plus this is a tree, not a graph, so we already know that (A) a path from the root node to any node *does* in fact exist, and only *one* such path exists. So that heuristic isn't particularly helpful here...
- I've never implemented DFS before so what the heck, let's try it. I think this might end up being a little different from a "classic" DFS implementation cause we want to search until we find *both* the start and destination nodes rather than just one, and we also want to do other things along the way like keep track of the `L`/`R` directions we took to get there. And also we're working with a tree rather than a more general graph so there won't be any cycles.
  - I *could* write a helper function to find a single node from the root node, then call it for the start node and then the destination node. But I thnk that would be less efficient because we'd end up checking some nodes twice and potentially skipping the destination node while looking for the start node.
- I remember BFS uses a queue to store nodes to be searched so that each level of the tree is finished before the next one is started. By that logic I think DFS would need to use a stack.
<!-- - But before starting to think about actual implementation stuff, here's how I generally think this is gonna go: -->
- Here's how I think this is generally gonna go:
  - initialize:
    - variables to hold the start & dest nodes to `None`
    - the stack of nodes to search to `[root]`
  - while 1 or both of the start/dest node variables is `None`:
    - pop the top node off the stack. If it's the start or dest node, set the relevant variable to it
      - at this point I'll need to do something to figure out the directions to get to this node from the root... I should probably record that each iteration
        - actually, how could I do this... I was originally thinking I could maintain a record of `L`s and `R`s, and add to/remove from it based on whether the current node is the left or right child of its parent node... but the nodes don't store references to their parents, and since I'll be popping nodes off the stack to get the next one, the parent won't necessarily have been the previous node we checked.
        - I could set an attr on each node I check that references its parent, and then once I find the start/dest node, backtrack through those. Or I could do a similar thing with a dict that maps nodes to their parents. But either of those would add additional memory usage, which isn't ideal.
        - I was also starting to think that DFS might be better conceptualized as recursive, since when we hit the "bottom" of the tree and run out of child nodes to check, we go "back up a level" like recursion does with a call stack. And since I could recurse all the way down, say, the left branch before starting the right branch (at each given level), then I think I *could* maintain a stack of directions, and push/pop from it as I go down and back up the tree... but I think the problem with the recursive idea is I'm not sure I could easily continue looking for the start/dest node once I've found the other... though actually I guess I could either set those start & dest variables as attrs of the class instance instead of inside the function...
        - I'm running out of time to finish this problem today, so I'll just go with the dict solution for now and maybe try out the recursive version if I have time later.
      - let's say I now have a dict of {node: parent}. I think I'll write a helper function that traces back through the parents dict to create the path from the root to that node. This will probably be a while loop based on encountering the root
        - the recursive version is seeming more and more preferable... I want to get this problem done by EOD so I think I'm just gonna wing it rather than continue on with these thoughts

## Refining the problem, round 2 thoughts

## Attempted solution(s)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def getDirections(self, root: Optional[TreeNode], startValue: int, destValue: int) -> str:
        root_start_path = None
        root_dest_path = None
        curr_node_path = []

        def dfs_find_start_dest(node):
            nonlocal root_start_path, root_dest_path
            if root_start_path is not None and root_dest_path is not None:
                return True
            if node.val == startValue:
                root_start_path = deque(curr_node_path)
            elif node.val == destValue:
                root_dest_path = deque(curr_node_path)
            if node.left is not None:
                curr_node_path.append('L')
                if dfs_find_start_dest(node.left):
                    return True
                curr_node_path.pop()
            if node.right is not None:
                curr_node_path.append('R')
                if dfs_find_start_dest(node.right):
                    return True
                curr_node_path.pop()

        dfs_find_start_dest(root)

        while True:
            if len(root_start_path) == 0:
                return ''.join(root_dest_path)
            if len(root_dest_path) == 0:
                return 'U' * len(root_start_path)
            if root_start_path[0] == root_dest_path[0]:
                root_start_path.popleft()
                root_dest_path.popleft()
            else:
                return 'U' * len(root_start_path) + ''.join(root_dest_path)
```

![](https://github.com/user-attachments/assets/8310dfbc-c990-42ea-8735-34382596a7c3)
