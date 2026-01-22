# [Problem 1948: Delete Duplicate Folders in System](https://leetcode.com/problems/delete-duplicate-folders-in-system/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to detect identical folders in a folder tree defined by many absolute paths. Identical folders have the same set of subfolders (by name) and those corresponding subfolders are themselves identical recursively. This suggests building a tree/trie representing the filesystem and then computing a canonical representation (signature) of each subtree so identical subtrees map to the same signature. After finding signatures that occur more than once we should mark those subtrees for deletion (and delete all their descendants too). Finally, return all remaining paths.

Key details:
- The signature must encode child name + child's subtree signature so that names matter.
- The problem text says "same non-empty set of identical subfolders", so a folder with zero subfolders should not be considered identical for deletion even if there are many empty folders.
- Only folders marked in the initial pass are removed, i.e., do the marking based on the initial signatures, then delete marked subtrees (not iteratively).

A classic approach: build trie -> postorder compute subtree signatures (using dictionary-to-unique-id compression) -> count signatures -> mark/delete nodes whose signature appears >1 and node has at least one child -> collect remaining paths.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- Must ensure child names are considered in the signature, so two folders with different child names but identical child structures are not considered identical.
- Leaves (no children) produce an "empty" signature, but the deletion condition should require that the folder's subfolder set be non-empty, otherwise empty folders are not deleted even if identical.
- Use a mapping from a tuple of (childName, childSigId) sorted by childName to a unique integer id; using integers keeps signatures compact and comparisons fast.
- Complexity: Building trie is O(total number of components in all paths). Computing signatures touches each node once; sorting child keys at each node costs sum over nodes of O(c_i log c_i) where c_i is number of children of node i, which overall is acceptable since sum c_i = number of edges ~ nodes. Space: O(number of nodes) for the trie and maps.

I'll implement a concise, clear Python solution with these steps:
1. Build trie.
2. Postorder compute subtree signature ids and counts.
3. Mark nodes whose signature id count > 1 and node has children (non-empty set).
4. Traverse to collect remaining paths skipping marked subtrees.

## Attempted solution(s)
```python
from collections import defaultdict
from typing import List

class TrieNode:
    def __init__(self):
        self.children = {}  # name -> TrieNode
        self.sig_id = None
        self.deleted = False

class Solution:
    def deleteDuplicateFolder(self, paths: List[List[str]]) -> List[List[str]]:
        root = TrieNode()
        # 1. Build trie
        for path in paths:
            node = root
            for name in path:
                if name not in node.children:
                    node.children[name] = TrieNode()
                node = node.children[name]

        # 2. Postorder compute signatures
        sig2id = {}
        id_count = defaultdict(int)
        next_id = [1]

        def dfs_sig(node: TrieNode) -> int:
            # build a signature as tuple of (name, child_sig_id) sorted by name
            if not node.children:
                sig = ()  # empty children
            else:
                items = []
                for name in sorted(node.children.keys()):
                    child = node.children[name]
                    child_id = dfs_sig(child)
                    items.append((name, child_id))
                sig = tuple(items)
            if sig not in sig2id:
                sig2id[sig] = next_id[0]
                next_id[0] += 1
            sid = sig2id[sig]
            id_count[sid] += 1
            node.sig_id = sid
            return sid

        dfs_sig(root)

        # 3. Mark duplicates for deletion (only nodes with non-empty children and count>1)
        def mark(node: TrieNode, is_root: bool = False):
            # if not root and node has children and its signature occurs more than once -> delete entire subtree
            if (not is_root) and node.children and id_count[node.sig_id] > 1:
                # mark subtree
                def mark_subtree(n: TrieNode):
                    n.deleted = True
                    for c in n.children.values():
                        mark_subtree(c)
                mark_subtree(node)
                return
            # otherwise, recurse into children
            for child in node.children.values():
                mark(child, False)

        mark(root, True)

        # 4. Collect remaining paths (every non-root non-deleted node contributes a path)
        res = []
        def collect(node: TrieNode, path: List[str]):
            for name, child in node.children.items():
                if child.deleted:
                    continue
                new_path = path + [name]
                res.append(new_path)
                collect(child, new_path)

        collect(root, [])
        return res
```
- Notes on approach:
  - We build a trie to represent the filesystem.
  - For each node we compute a signature based on its children's names and their subtree signatures; identical subtrees get the same integer signature id through a dictionary compression (sig2id).
  - We count how many times each signature id appears. According to the problem statement, only folders that contain a non-empty set of identical subfolders should be deleted: hence we only delete nodes that have at least one child and whose signature id count is greater than 1.
  - Once a node is marked for deletion, its whole subtree is marked (deleted) and will not be included in the result. The deletion determination is made based on the initial signatures (single pass).
  - Complexity:
    - Let N be total number of nodes across the trie (sum of lengths of all paths). Building the trie is O(N).
    - Computing signatures visits each node once; at each node we sort its child names — the total cost of sorting across all nodes is sum O(c_i log c_i) where c_i are child counts; this is bounded reasonably by N log D in practice (D small average), acceptable for constraints.
    - Overall time: roughly O(N log K) where K is average branching factor; space O(N) for the trie and maps.