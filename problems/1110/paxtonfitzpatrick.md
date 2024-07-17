# [Problem 1110: Delete Nodes And Return Forest](https://leetcode.com/problems/delete-nodes-and-return-forest/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- this one seems much easier than yesterday's tree problem (thank goodness)
- I think the key here is going to be to make sure we check whether a node's children (and their children, and so on...) are in the `to_delete` list before disconnecting the node from its parent so we don't lose the reference to it
- that initially makes me think we should do this recursively so we can just make the recursive call before disconnecting the node, but I think BFS would also work as well as long as we add the children to the queue before disconnecting
  - DFS might also work? I'm just not as familiar with it so I don't have an immediate intuition...
    - actually, is what I was calling "doing this recursively" really just DFS? I think it is...
    - in the DFS I wrote for yesterday's problem, I checked the "current" node before recursing down to its children... but I don't think there's necessarily a reason I *have* to do that.
    - in fact, recursing first means we'd functionally be checking nodes in the tree from bottom to top, which seems potentially useful here since we're disconecting children from their parents.
- Let's think about why BFS or DFS might be preferable here:
  - with BFS I'd encounter a node by popleft-ing it off the queue, then for each of its left/right children, I'd check whether the child exists, and if so, append it to the queue. Also, if the current node is in `to_delete`, I'd append its children to the list of new roots
    - hmmm but what if one of those children is also in `to_delete`? I'd have to check that it wasn't before appending it to the list of new roots, but then I'd also have to check this again when I popleft it off the queue later on to determine whether to add *its* children to the list of new roots. This would be slightly inefficient.
  - with DFS, I'd encounter a node (by either popping it from a stack or calling a recursive function on it), then for each of its left/right children, I'd check whether that child exists and and if so... quick aside: I'm realizing that I'd probably want to do this recursively rather than with a stack so I could recurse first and deal with lower-down nodes before operating on the "current" node. So I'd call the recursive function on its children (if any), and then if the current node is in `to_delete`, I'd append those children to the list of new roots to return
    - ah, I forgot I also need to set the left/right child attr on each deleted node's parent to `None`... that'd be challenging with recursion, cause I won't have access to the parent node in the recursive call on the child, so I'd have to check child attrs again, one level up. So that'd be inefficient just like the BFS approach.
    - oh -- or, I could return `True` from the recursive call if the node passed to it should be deleted, and `False` otherwise, and then use that to determine whether to set the "current" node's child attrs to `None`.
- another important point: each time we encounter a node, we have to check whether it's in `to_delete`. We have to check each node once, so the complexity of just that part is $O(n)$. But since `to_delete` is given to us as a `list` and the constraints say it can contain up to the total number of nodes in the tree, the worst-case complexity is actually going to be $O(n^2)$. But if I convert `to_delete` to a `set` up front, it'll bring the complexity back down to $O(n)$. So I definitely wanna do that.
- also, the constraints say the tree can consist of at most 1000 nodes, but not that it will consist of at least 1. So I should account for the possibility of root being `None` and return early

## Refining the problem, round 2 thoughts

- after starting to try to implement the recursive DFS version, I'm realizing I still end up with some duplicate checks, which I was hoping to try to avoid. I'm not sure how many of them can be condensed to a single check, but

## Attempted solution(s)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def delNodes(self, root: Optional[TreeNode], to_delete: List[int]) -> List[TreeNode]:
        if not root:
            return []

        def del_nodes_dfs(node):
            node_in_to_delete = node.val in to_delete
            if node.left:
                if del_nodes_dfs(node.left):
                    node.left = None
                elif node_in_to_delete:
                    new_roots.append(node.left)
            if node.right:
                if del_nodes_dfs(node.right):
                    node.right = None
                elif node_in_to_delete:
                    new_roots.append(node.right)
            return node_in_to_delete

        to_delete = set(to_delete)
        new_roots = []
        if not del_nodes_dfs(root):
            new_roots.append(root)
        return new_roots
```

![](https://github.com/user-attachments/assets/01a8c23b-874b-4bad-b234-4db131644be7)
