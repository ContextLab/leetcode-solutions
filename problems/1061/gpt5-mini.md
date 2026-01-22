# [Problem 1061: Lexicographically Smallest Equivalent String](https://leetcode.com/problems/lexicographically-smallest-equivalent-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see we are given pairwise equivalences between characters from s1 and s2. Those equivalences form equivalence classes (disjoint sets). For any character in baseStr we can replace it by any character in its equivalence class. To get the lexicographically smallest overall string, each character should be replaced by the smallest letter in its equivalence class. That suggests building connected components of the equivalence relation and mapping each character to the smallest element of its component.

Union-Find (disjoint set union) is a natural fit: union characters that are equivalent, then for each set keep or pick the smallest representative. One easy trick: always union by making the parent the lexicographically smaller root, so the root of each set becomes the smallest char. Then mapping baseStr is just find(char) -> root -> smallest char.

Edge cases: all lowercase letters only (26), lengths up to 1000 — small. No tricky extra cases.

## Refining the problem, round 2 thoughts
Implementation details:
- Represent characters as indices 0..25.
- Use union-find with path compression. To ensure the root is lexicographically smallest, when unioning two roots set the parent of the larger root to the smaller root (no need for rank).
- After processing all pairs, for each character in baseStr find its root and map to the corresponding smallest char.
Time complexity: each union/find is nearly constant (inverse Ackermann), effectively O(n + m) where n = len(s1) and m = len(baseStr). Space: O(26) for parent array plus O(m) for result.

Alternative approaches: build adjacency graph and do DFS/BFS for components and compute min char per component — more code and slightly heavier but equivalent complexity. Union-Find is simpler and efficient here.

## Attempted solution(s)
```python
class Solution:
    def smallestEquivalentString(self, s1: str, s2: str, baseStr: str) -> str:
        # Union-Find over 26 lowercase letters, ensure root is the lexicographically smallest char
        parent = list(range(26))
        
        def find(x: int) -> int:
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            # attach the larger root to the smaller root so root is always smallest char
            if ra < rb:
                parent[rb] = ra
            else:
                parent[ra] = rb
        
        # build equivalences
        for ca, cb in zip(s1, s2):
            union(ord(ca) - ord('a'), ord(cb) - ord('a'))
        
        # build resulting string by mapping each char to its set's smallest representative
        res_chars = []
        for ch in baseStr:
            r = find(ord(ch) - ord('a'))
            res_chars.append(chr(r + ord('a')))
        
        return "".join(res_chars)
```
- Approach: Use union-find on the 26 letters. When unioning two letters, always set the parent to the smaller lexicographic root so each set's root equals the smallest letter in that set. After unions, map each character in baseStr to the root (smallest equivalent) and build the answer.
- Time complexity: O(n α(26) + m α(26)) ≈ O(n + m), where n = len(s1) (== len(s2)) and m = len(baseStr). α is inverse Ackermann, effectively constant.
- Space complexity: O(1) extra (parent array of size 26) plus O(m) for the output string.
- Implementation notes: path compression in find keeps operations fast. No need for union-by-rank because we decide parent based on lexicographic order to guarantee smallest representative.