# [Problem 889: Construct Binary Tree from Preorder and Postorder Traversal](https://leetcode.com/problems/construct-binary-tree-from-preorder-and-postorder-traversal/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I know preorder gives root first, then the subtree(s). Postorder gives root last. With distinct values we can identify nodes across both arrays. The first element of preorder is the tree root. The second element of preorder (if exists) must be the root of the left subtree (if there is a left subtree). If I find that value in postorder, I can determine how many nodes are in the left subtree (postorder index gives end of left-subtree block). That tells me how to split preorder into left and right subtree ranges. Then recursively build left and right.

I recall there's an ambiguity when a node has only one child (left or right), but the problem allows returning any valid tree in cases with multiple possible trees. A hashmap from value to index in postorder will let me locate left-root quickly. Recursion with index ranges avoids costly slicing.

## Refining the problem, round 2 thoughts
- Use a helper recursive function that takes index ranges into preorder and postorder arrays.
- Base cases: empty range -> None; single element -> leaf node.
- For a range with more than one element:
  - root = preorder[preL]
  - left_root_val = preorder[preL + 1] (exists because more than one element)
  - left_root_index_in_post = post_index[left_root_val]
  - left_size = left_root_index_in_post - postL + 1
  - Recurse on left: preorder [preL+1 .. preL+left_size], postorder [postL .. left_root_index_in_post]
  - Recurse on right: preorder [preL+left_size+1 .. preR], postorder [left_root_index_in_post+1 .. postR-1]
- Complexity: each node processed a constant number of times, map lookup O(1) -> O(n) time. Space: O(n) for map + recursion stack up to O(n) worst-case.
- Edge cases: single node arrays, skewed tree (recursion depth n), but constraints small (n <= 30) so recursion depth is fine.

## Attempted solution(s)
```python
# Definition for a binary tree node (LeetCode style).
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class Solution:
    def constructFromPrePost(self, preorder, postorder):
        """
        Construct binary tree from preorder and postorder traversals.
        :type preorder: List[int]
        :type postorder: List[int]
        :rtype: TreeNode
        """
        if not preorder:
            return None

        # Map value -> index in postorder for O(1) lookups
        post_index = {val: i for i, val in enumerate(postorder)}

        def build(preL, preR, postL, postR):
            # build tree from preorder[preL:preR+1] and postorder[postL:postR+1]
            if preL > preR:
                return None
            root_val = preorder[preL]
            root = TreeNode(root_val)
            if preL == preR:
                return root  # single node

            # next element in preorder is left subtree's root (if left exists)
            left_root_val = preorder[preL + 1]
            left_root_idx = post_index[left_root_val]
            left_size = left_root_idx - postL + 1

            # build left and right subtrees recursively
            root.left = build(preL + 1, preL + left_size, postL, left_root_idx)
            root.right = build(preL + left_size + 1, preR, left_root_idx + 1, postR - 1)
            return root

        n = len(preorder)
        return build(0, n - 1, 0, n - 1)
```
- Approach: Recursively split preorder and postorder using the fact that preorder[preL+1] is the left subtree's root; find its index in postorder to get left subtree size, then recurse.
- Time complexity: O(n) — each node is created once and map lookups are O(1).
- Space complexity: O(n) for the hashmap + O(n) recursion stack in worst case. Actual extra space (excluding output tree) is O(n).
- Important details:
  - The arrays contain unique values, so the map approach is safe.
  - When there's only one node in the current range, return immediately to avoid accessing preorder[preL+1].
  - The solution returns any valid tree when multiple trees satisfy the traversals (problem allows this).