# [Problem 2196: Create Binary Tree From Descriptions](https://leetcode.com/problems/create-binary-tree-from-descriptions/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- Okay, I've heard of binary trees but never actually worked with one before... I guess that's what comes from not really having taken CS classes!
- I've dealt with things things that can be represented as trees, like directory structures and hierarchical Docker images, but I've never explicitly created one or written code that conceptually treats those things as trees algorithmically (at least not knowingly...). But maybe thinking about this problem in terms of how I'd deal with one of those examples of trees that I'm familiar with will be helpful?
- I wonder if there's some well known or established "optimal way" of finding a tree's root from any particular node.
- I guess I could start with the first item in the input list and use its "parent" value to look for another item where that value is the "child" value, and then follow that to the top of the tree (when a particular "parent" value isn't the "child" in any entries, that's the root).
  - Once I know the root, I think I could construct the tree basically by doing the opposite of the above -- following parent values down to child values and creating nodes as I go.
  - This reminds me of BFS and DFS. I learned about BFS forever ago in the one CS class I took, but never DFS, though I think I could figure it out if needed. I also don't know when one is better to use than the other.
  - But also I feel like a lot of the operations and traversal needed to construct the tree would end up being redundant with how I'd get "up" to the root... would constructing nodes as I work my way up help? Maybe a bit cause I could check if a particular node exists, but I'd still have to do the full traversal because I won't know if I've already constructed all children of a particular already-constructed node.
- Could I just do this by iterating through the list once and constructing nodes as I go?
  - I wouldn't know all the relevant info about node I encounter, I but I could create nodes with attr values partially filled in based on what I *do* know, then update them with additional info as I learn it from later entries while iterating.
  - Since all nodes have unique values, I could store each node I create in a dict with the values as keys, so I can retrieve nodes to update in $O(1)$.
  - How would I then find the root to return?
    - I don't want to do this by traversing nodes and following parents up the tree, because unfortunately nodes don't store references to their parent, just their children (unless I added this myself?) so it'd require repeatedly iterating over nodes to find each one's parent based on the child attrs each has, and that'd be inefficient.
    - Could I somehow keep track of "candidate" root nodes as I encounter them, and remove them from consideration when I know they're no longer possibly the root?
      - the root node is the one that appears (once or twice) in a "`parent`" position in the input list but never in a "`child`" position. So the first time I encounter a node and create it (i.e., it's not already in the dict I'm using to store nodes), if it's in the "`parent`" position, it's possible that it's the root. But any nodes I encounter in the "`child`" position at any point can't be the root. By the end, there should be only one possible root left.
      - Do I need to add/remove things from consideration every time I encounter them? Or just the first/non-first time?
        - if I encounter a new node for the first time in a parent position, it's possible it's the root
        - if I encounter a previously seen node in the parent position, either (A) I've already encountered it in the parent position and added it to the possible roots, or (B) I've previously encountered it in the child position and it can't be the root
        - if I encounter a new node for the first time in a child position, I'll create it and add it to the dict, and then it'll exist if/when I ever encounter it in the parent position later on so I wouldn't add it for consideration per the rule above
        - if I encounter a previously seen node in the child position, I **must** have previously encountered it in the parent position because each node is the child of only a single other node, so I should remove it from consideration.
    - I'll use a set to keep track of candidate roots. It'll take slightly longer to add new candidate nodes than appending them to a list would, but it'd allow me to do all removals in $O(1)$ time.
  - I'm gonna try implementing this.

## Refining the problem, round 2 thoughts

- My solution runs in $O(n)$ time, and I don't think it's possible to do any better than that, since at minimum we have to create a `TreeNode` object for every node in the tree.

## Attempted solution(s)

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def createBinaryTree(self, descriptions: List[List[int]]) -> Optional[TreeNode]:
        nodes = {}
        possible_roots = set()

        for (parent_val, child_val, is_left) in descriptions:
            if child_val in nodes:
                child_node = nodes[child_val]
                possible_roots.discard(child_val)
            else:
                child_node = TreeNode(child_val)
                nodes[child_val] = child_node
            if parent_val in nodes:
                parent_node = nodes[parent_val]
            else:
                parent_node = TreeNode(parent_val)
                nodes[parent_val] = parent_node
                possible_roots.add(parent_val)
            if is_left:
                parent_node.left = child_node
            else:
                parent_node.right = child_node

        return nodes[possible_roots.pop()]
```

![](https://github.com/user-attachments/assets/5d151aad-aeec-4c92-b3a9-bad1a9bd97eb)
