# [Problem 951: Flip Equivalent Binary Trees](https://leetcode.com/problems/flip-equivalent-binary-trees/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to check whether two binary trees can be made identical by performing any number of flips, where a flip swaps left and right subtrees of a node. The simplest idea is recursive: for two nodes to be flip-equivalent they must have the same value, and either
- their left children are flip-equivalent and their right children are flip-equivalent (no flip at this node), or
- the left child of one is flip-equivalent to the right child of the other and vice versa (flip at this node).

Edge cases: either node could be None. If both None -> True; one None -> False. The node values are unique which simplifies reasoning but isn't strictly required for the recursive check. Depth is limited by ≤100 nodes so recursion depth is safe.

## Refining the problem, round 2 thoughts
Refinement:
- Base cases first: both None -> True; one None -> False; values differ -> False.
- Then check the two recursive possibilities (no flip vs flip).
- Time complexity: each pair of nodes is compared once in the recursion chain; in worst case we may explore both arrangements at many nodes but with unique values and pruning on mismatched values this is efficient. Formal worst-case recurrence yields O(min(n1, n2)) checks with constant work per check, so O(n) time where n is number of nodes.
- Space complexity: recursion stack up to tree height -> O(h) worst-case O(n) for degenerate tree, typically O(log n) for balanced.
- Alternative: canonicalize each tree into a form invariant under flips (e.g., always order children by some key and serialize); then compare serializations. That works too but recursion directly is simpler and readable.
- Consider trees with nodes but different structures/values — recursion handles that.

## Attempted solution(s)
```python
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

from typing import Optional

class Solution:
    def flipEquiv(self, root1: Optional['TreeNode'], root2: Optional['TreeNode']) -> bool:
        # Base cases
        if root1 is None and root2 is None:
            return True
        if root1 is None or root2 is None:
            return False
        if root1.val != root2.val:
            return False

        # Check without flip: left->left and right->right
        no_flip = self.flipEquiv(root1.left, root2.left) and self.flipEquiv(root1.right, root2.right)
        if no_flip:
            return True

        # Check with flip: left->right and right->left
        flip = self.flipEquiv(root1.left, root2.right) and self.flipEquiv(root1.right, root2.left)
        return flip
```
- Notes about the solution:
  - Approach: simple recursive DFS comparing the two trees with two possibilities at each node (flip or not).
  - Correctness: base cases ensure structure/value mismatches are rejected early. The two recursive checks cover all flip/no-flip choices.
  - Time complexity: O(n) in practice (n is number of nodes visited); each node pair triggers constant work plus recursive calls. Worst-case recursion may explore both branches at nodes, but with value checks and limited size (≤100) this is fine. More formally, the algorithm runs in O(min(n1, n2)) comparisons where n1, n2 are sizes of the two trees.
  - Space complexity: O(h) recursion stack where h is the height of the tree (worst-case O(n), average O(log n) for balanced trees).