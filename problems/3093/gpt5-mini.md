# [Problem 3093: Longest Common Suffix Queries](https://leetcode.com/problems/longest-common-suffix-queries/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the container string that has the longest common suffix with a given query string. Longest common suffix between strings is the same as longest common prefix after reversing strings. So building a trie over reversed wordsContainer feels natural: for a query, walk down the trie following reversed characters as far as possible — the deepest node reached corresponds to the longest common suffix. However, if multiple container words share that suffix, the tie-breaker is the shortest container word (then earliest index). So at each trie node we should remember, among all container strings in the node's subtree, which one is currently the best according to (length, index). Then for each query we traverse as far as possible and return the stored best index at that node (root covers empty suffix). This yields O(total length) construction and O(total query length) answering.

## Refining the problem, round 2 thoughts
- We will reverse every container word while inserting into trie; at each node store the best candidate index chosen by the pair (word length, index) with lexicographic-style comparison on the tuple (length, index) where smaller is better.
- For queries, reverse and walk; if walk breaks early return best stored at last matched node (including root).
- Edge case: no matched characters (empty common suffix) — root should hold the globally best candidate (shortest word, earliest index) because empty suffix is shared with every container word.
- Complexity: building trie uses sum lengths of wordsContainer; queries sum lengths of wordsQuery.
- Memory: number of trie nodes <= sum lengths of container words. Implementation uses children maps for nodes (sparse representation).
- Implementation detail: store children per node as dict char->node_id, and arrays best_idx and best_len for nodes. Use tuple comparison when updating.

## Attempted solution(s)
```python
class Solution:
    def longestCommonSuffixQueries(self, wordsContainer, wordsQuery):
        """
        Build a trie of reversed wordsContainer. At each node keep the best container index
        among all words in that node's subtree according to (length, index) where smaller is better.
        For each query, traverse reversed query as far as possible and return the node's stored index.
        """
        # Trie using lists for node attributes and dict for children mapping
        children = []  # list of dicts char -> node_id
        best_idx = []  # best container index at node
        best_len = []  # length of that best container word (for tie-breaking)
        
        # initialize root
        children.append({})
        best_idx.append(0)
        INF = 10**9
        best_len.append(INF)
        
        # helper to try update node with candidate (length, index)
        def try_update(node, length, idx):
            # smaller length is better; if equal length smaller index is better
            if length < best_len[node] or (length == best_len[node] and idx < best_idx[node]):
                best_len[node] = length
                best_idx[node] = idx
        
        # Insert all container words (reversed)
        for i, w in enumerate(wordsContainer):
            L = len(w)
            cur = 0
            # update root (empty suffix) with this word candidate
            try_update(cur, L, i)
            for ch in reversed(w):
                nxt = children[cur].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[cur][ch] = nxt
                    children.append({})
                    best_idx.append(0)
                    best_len.append(INF)
                cur = nxt
                try_update(cur, L, i)
        
        # Answer queries
        ans = []
        for q in wordsQuery:
            cur = 0
            # default best is at root
            best = best_idx[0]
            for ch in reversed(q):
                if ch in children[cur]:
                    cur = children[cur][ch]
                    best = best_idx[cur]
                else:
                    break
            ans.append(best)
        return ans
```
- Notes about the solution:
  - We reversed container words and built a prefix trie on the reversed strings. Each node stores the best candidate index among its subtree according to the tie-breakers (shorter length first, then earlier occurrence).
  - For each query we traverse the trie along the reversed query; the deepest node reachable corresponds to the longest common suffix; we return the node's stored best index.
  - Time complexity:
    - Building trie: O(sum len(wordsContainer)).
    - Query answering: O(sum len(wordsQuery)).
    - Total: O(total characters) which is within constraints (sum lengths ≤ 5e5).
  - Space complexity: O(sum len(wordsContainer)) for trie nodes; each node stores a small dict of children and two ints.
  - Implementation detail: root is updated as we insert words so when no matching suffix characters exist the answer is the globally best container index (shortest word, earliest index).