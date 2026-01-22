# [Problem 1233: Remove Sub-Folders from the Filesystem](https://leetcode.com/problems/remove-sub-folders-from-the-filesystem/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to remove any folder that is a sub-folder of another folder in the list. A sub-folder has the property that it starts with the parent folder path followed by a '/'. The simplest idea that comes to mind is sorting the list lexicographically so that parent folders come before their children (e.g., "/a" before "/a/b"). Then iterate through the sorted list and keep a "current root" folder; if the next folder starts with current_root + "/" then it's a sub-folder and should be skipped. Otherwise it's a new root to keep. This is straightforward and avoids building an explicit trie.

Potential pitfalls: ensuring we check the '/' after the prefix (so "/a" doesn't incorrectly mark "/aa" as a subfolder). Also account for ordering: sorting gives the needed grouping.

## Refining the problem, round 2 thoughts
Refinement and edge cases:
- Sorting lexicographically is safe because folder names have '/' and lowercase letters; parents precede children (e.g., "/a" < "/a/b").
- Use startswith(prefix + "/") to distinguish "/a" from "/aa".
- Keep in mind constraints: up to 4e4 strings, length up to 100 — sorting and string comparisons are fine.
- Alternative: build a trie of path components and mark top-level nodes, but that's more code and not necessary for acceptable complexity.
- Complexity: sorting O(n log n) with comparisons cost proportional to string length; then a single O(total_length) pass.

I'll implement the sorted-and-scan approach. It returns the kept folders in any order; since we sorted, result will be lexicographically ordered (acceptable).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def removeSubfolders(self, folder: List[str]) -> List[str]:
        # Sort folders so parent paths come before their children
        folder.sort()
        res = []
        # current_root holds the most recently added folder that could be a parent
        current_root = ""
        for f in folder:
            # If current_root is a prefix of f and followed by '/', f is a subfolder
            # Example: current_root = "/a", f = "/a/b" -> "/a/" is prefix of f
            if current_root and f.startswith(current_root + "/"):
                continue
            # Otherwise f is not a subfolder of current_root; add it and update current_root
            res.append(f)
            current_root = f
        return res
```
- Notes:
  - Approach: sort the folder list and scan once, keeping the last accepted root. For each folder, check if it starts with current_root + "/". If yes, it's a subfolder and skipped; otherwise it's retained and becomes the new current_root.
  - Time complexity: O(n log n * L) for sorting (n = number of folders, L = average length for string comparison), plus O(total_length) for the scan.
  - Space complexity: O(n * L) for sorting storage and output (excluding input). The extra auxiliary space is O(1) aside from output.
  - This solution is simple, efficient, and handles edge cases like "/a" vs "/aa" correctly due to the explicit "/" check.