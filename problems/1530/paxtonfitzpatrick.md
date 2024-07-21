# [Problem 1530: Number of Good Leaf Nodes Pairs](https://leetcode.com/problems/number-of-good-leaf-nodes-pairs/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- hmmm this one seems kinda tricky... first important thing is that based on the examples, "leaf nodes" apparently refers only to nodes with no children
- naive solution would be to find all the leaf nodes, then find the number of steps between all pairs of leaf nodes, but that'd be very slow.
- Maybe there are some patterns in the relationships between nodes' "relationships" and their distance that we could leverage?
  - "sibling nodes" have a distance of 2
  - a node and its parent's sibling have a distance of 3
  - a node and its "grandparent's" sibling have a distance of 4
  - two "cousin" nodes (i.e., node -> parent -> parent -> child -> child) also have a distance of 4
  - and so on...
- I can't really see how that'll be useful yet. I was initially thinking the distance might have *some* relationship with the difference between the two leaf nodes' "levels" in the tree, and since BFS traverses by levels, maybe I could keep track of the current level I'm on while searching, record the level of each leaf node I find, and then figure out how many "good" pairs there are based on that. But now I don't think so...
- Let's try some other ideas:
- **idea 1)** BFS still seems promising. I'd have to add an attr to each node referencing its parent to do this, but if I started a BFS from each leaf node I found, I could stop searching when I got more than `distance` steps away.
  - I'd need some way to avoid double-counting node pairs though. I could maintain a set of tuples of leaf pairs (i.e., `{(leaf1, leaf2), (leaf1, leaf3),...}`) to check each time.
    - Actually, this wouldn't work. Sets can only contain hashable objects, and tuples are only hashable if their contents are hashable, which means I'd have to use the the nodes' values, and those aren't guaranteed to be unique.
    - And also I don't think this would have been more efficient anyway. Since I'd need to reach each leaf from each other leaf to even do that check against that set, I might as well not eat up the extra memory from maintaining it and accept that I'll count each pair twice, then just divide by 2 at the end.
- **idea 2)** what if I searched for all the leaf nodes, and as I found each one, kept track of how many steps away from it I was as I kept searching for the rest? Then whenever I encountered each subsequent leaf, I could increment my count of good pairs by the number of previously found leaves that are < `distance` away.
  - I'm not sure whether this would be efficient... on one hand, I'd only have to encounter each node once, so just 1 pass through the tree. But to maintain and update this "n steps away" data, I'd have to do number-of-found-leaves operations at every node, so towards the end the runtime would approach something like $O(kn)$ where $n$ is the number of nodes and $k$ is the number of leaves. Plus the logic for figuring out whether to add or subtract 1 from each encountered leaf's current distance value isn't immediately obvious to me.
  - OTOH the "BFS from each leaf" solution would require searching the full tree to find all leaves, which is $O(n)$, plus number-of-leaves BFSes, each of which I think is $O(k)$, so that's an additional $O(k^2)$. But it's like $O(n + k^2)$, not $O(nk^2)$, so I'm not sure how to compare between that and $O(kn)$. I think which would be greater depends on the size of $k$ relative to $n$?
- **idea 3)** what if I adapted my solution to the "shortest path/directions between 2 nodes" problem from the other day where I found the 2 nodes' "least common ancestors"? If I got the path from the root node to each leaf (BFS? DFS?), I could take each pair of paths, discard all shared direction at their beginnings, then sum the remaining non-shared directions.
  - I think this might take longer than necessary because if `distance` is small and the tree is deep, a large % of the directions could be shared and I'd do a lot of unnecessary iterating.
  - okay but if the paths consisted of `TreeNode` objects and I looped over the pairs of paths in reverse, I could add 2 to some counter on each iteration and stop either (A) when I hit the same node in both paths, or (B) when that counter > `distance`.
  - This seems promising.
- **idea 4)** Instead of finding all the leaves and *then* doing BFS from each, if I did each leaf's BFS when I encountered it, could I somehow remove nodes from the tree after I've already searched from them, so that there are fewer nodes to deal with for each subsequent BFS?
  - Could I do a recursive DFS to find the leaves, then after recursing down each left/right "sub-branch", "remove" the node for that side? I think so, and that'd also successfully keep me from having duplicates in the count of "good" pairs -- e.g., after I encounter `leafA` and find `leafB` < `direction` away from it, I'd remove `leafA` (and unless it and `leafB` are siblings, also its parent) from the tree before encountering `leafB`.
  - To "remove" a node, I'd have to set its parent's `left` or `right` attr to something other than `None` to avoid creating additional "fake" leaves.
  - This also seems promising.
  <!-- - No, cause it's still possible for leaves under that node to be < `distance` steps away from leaves down a different branch. -->
  <!-- - But what if I just recorded how many steps down that branch any leaves were before dropping it? I'll come back to this, got another idea -->
- **idea 5)** combine **idea 1** and **idea 4** to "jump between leaves." What if I ran DFS just until I found the first leaf, then stopped. Then from that leaf, I could do BFS (or DFS?) to find all other leaves within `distance` steps of it and add them to the queue/stack (if they're not in some sets of "leaves already checked"), and keep going with that? Then I basically have the $O(k)$ search over leaves from **idea 1** but I can basically skip the initial $O(n)$ search over all nodes to find the leaves.
  - I'd still have to add an attr to each node pointing to its parent the first time I encounter it, which I don't think would be a problem since I'll still always encounter nodes for the first time as I'm going "down" the tree rather than "up" it.
    - It's still not ideal, but shouldn't take *that* much extra memory cause I'm just pointing to an existing object rather than creating one.
  - Nope, this wouldn't work 😕. I was thinking it'd be okay to potentially leave some leaves unfound if they don't contribute to the number of "good" pairs anyway, but I realized it's not guaranteed that we'll have a continuous string of leaves within `distance` to traverse -- e.g., there could be 2 groups of leaves where the leaves within each group are < `distance` from each other, but > `distance` from the other pair.
- **idea 6)** combine **idea 3** and **idea 4**. What if instead of finding the full path from the root to each leaf and *then* looping through those at the end to find the least common ancestor between each pair of leaves, I basically did the equivalent of that as I searched for leaves? A given node is the least common ancestor between leaves in its left and right subtrees, so if I did a recursive DFS down the left and right branches, I could return the number of steps to each leaf node (if any) and check if any left subtree distances + right subtree distances were < `distance`.
  - I think I'd represent this as a list of distances to leaves, so I'd get a list of distances for the left subtree and one for the right subtree. So this could still involve a lot of looping to compare each leaf the left list to each in the right list, but less than **idea 3** would. Also I think I could reudce the number of total comparisons by removing leaves from consideration once they are > `distance - 1` steps down one branch from the current node.
  - I'd also then need to merge these lists together and increment each leaf's distance to return a new list of distances for the current recursive call. Also in the base case (node is a leaf) I'd want to return `[1]`, or something like that.
  - Is there a more efficient way I could represent these so the comparing and/or merging would be more efficient? Since I just care about the number of leaves in the end, maybe I could have a dict of `{to-leaf distance: count}` instead of separate entries in a list for each leaf. A dict would take a bit more memory and be slower to construct, but it'd get rid of duplicates in the lists and also allow me to drop multiple leaves with distances > `distance - 1` at once. Hard to say whether or not this would pay off...
  - actually, I think I could use a list & its indices to track leaf-distance counts instead of a dict. I could have each recursive call return a list of length `distance - 1` where each index refers to the "number of steps from the current node" and the values are the number of leaves that many steps down the left/right subtree (actually, index 0 would be 1 step, index 1 would be 2 steps, etc.).
    - This would contain a large % of 0's in cases where `distance` is large, I think. But since `distance` is guaranteed to be <= 10, that'll never be *too* many. And it'd condense multiple leaves the same distance away into the same value like using a dict would, plus it'd also make the logic of what to do when a node has one child but not the other much easier, I think.
    - It also makes the conditional check for removing leaves from consideration much easier -- I only care about leaves <= `distance - 1` steps down the left or right subtree, because it'll take at least 1 step down the other subtree to reach any node with which they could be paired (and haven't been already via a lower recursive call). So each time I need to merge and increment the counts from a node's left and right subtrees, I can just drop the last value from those two lists and increment all other values' indices by 1
    - edge case: what happens if `distance == 1`? I don't even need to worry about this because it's impossible for 2 leaves to be < 2 steps away from each other, so I can just return 0 immediately in that case.
- Okay, I think I'm going to try implementing a few of these.

## Refining the problem, round 2 thoughts

## Attempted solution(s)

### Idea 6

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def countPairs(self, root: TreeNode, distance: int) -> int:
        if distance == 1:
            return 0

        self.n_good_pairs = 0
        self.dist_minus_one = distance - 1
        self._dfs_leaf_dists(root)
        return self.n_good_pairs

    def _dfs_leaf_dists(self, node):
        # could be simplified but structured to avoid duplicate checks
        if node.left is None:
            if node.right is None:
                # base case: node is a leaf
                steps_away = [0] * self.dist_minus_one
                steps_away[0] = 1
                return steps_away
            return [0] + self._dfs_leaf_dists(node.right)[:-1]
        if node.right is None:
            return [0] + self._dfs_leaf_dists(node.left)[:-1]

        left_subtree_dists = self._dfs_leaf_dists(node.left)
        right_subtree_dists = self._dfs_leaf_dists(node.right)
        steps_away = [0]
        for left_ix, left_n_leaves in enumerate(left_subtree_dists[:-1]):
            steps_away.append(left_n_leaves + right_subtree_dists[left_ix])
            if left_n_leaves:
                for right_n_leaves in right_subtree_dists[:self.dist_minus_one-left_ix]:
                    if right_n_leaves:
                        self.n_good_pairs += left_n_leaves * right_n_leaves

        self.n_good_pairs += left_subtree_dists[-1] * right_subtree_dists[0]
        return steps_away
```

![](https://github.com/user-attachments/assets/ac7f6c80-ceda-4685-baa2-c989756a3679)

Nice -- I think it's unlikely any of my other ideas will beat that, but I still want to see how they do.

### Idea 3

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def countPairs(self, root: TreeNode, distance: int) -> int:
        if distance == 1:
            return 0

        leaf_paths = self._dfs_leaf_paths(root)
        n_good_pairs = 0
        for ix, path in enumerate(leaf_paths):
            leaf_paths[ix] = set(path)
        for path1_ix, path1 in enumerate(leaf_paths):
            for path2 in leaf_paths[path1_ix+1:]:
                if len(path1 ^ path2) + 2 <= distance:
                    n_good_pairs += 1
        return n_good_pairs

    def _dfs_leaf_paths(self, node):
        if node.left is None:
            if node.right is None:
                return [[]]
            else:
                leaf_paths = self._dfs_leaf_paths(node.right)
                for path in leaf_paths:
                    path.append(node)
                return leaf_paths
        if node.right is None:
            leaf_paths = self._dfs_leaf_paths(node.left)
            for path in leaf_paths:
                path.append(node)
            return leaf_paths
        leaf_paths = self._dfs_leaf_paths(node.left)
        leaf_paths.extend(self._dfs_leaf_paths(node.right))
        for path in leaf_paths:
            path.append(node)
        return leaf_paths
```

![](https://github.com/user-attachments/assets/f35726a0-fbd2-4541-988f-8d7284f891bf)

Yep, that's pretty slow.

### Idea 4

```python
class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Solution:
    def countPairs(self, root: TreeNode, distance: int) -> int:
        if distance == 1:
            return 0

        root.parent = None
        self.n_good_pairs = 0
        self.dist_plus_one = distance + 1
        self._dfs_find_leaves(root)
        return self.n_good_pairs

    def _dfs_find_leaves(self, node):
        if node.left is None:
            if node.right is None:
                return self._dfs_find_good_pairs(node.parent, node, 1)
            else:
                node.right.parent = node
                self._dfs_find_leaves(node.right)
                node.right = 0
                return
        node.left.parent = node
        self._dfs_find_leaves(node.left)
        node.left = 0
        if node.right is None:
            return
        node.right.parent = node
        self._dfs_find_leaves(node.right)
        node.right = 0

    def _dfs_find_good_pairs(self, node, prev, steps_away):
        if steps_away == self.dist_plus_one:
            return
        if node.left is node.right is None:
            self.n_good_pairs += 1
            return
        if node.left and node.left is not prev:
            node.left.parent = node
            self._dfs_find_good_pairs(node.left, node, steps_away + 1)
        if node.right and node.right is not prev:
            node.right.parent = node
            self._dfs_find_good_pairs(node.right, node, steps_away + 1)
        if node.parent and node.parent is not prev:
            self._dfs_find_good_pairs(node.parent, node, steps_away + 1)
```

![](https://github.com/user-attachments/assets/95a130f3-f0bf-48b3-8c37-d4f84a3c29e7)

Interesting, so this one's also slower than **idea 6** but it's a lot more memory efficient. Probably because I'm not creating and storing that list of distances for each node.
