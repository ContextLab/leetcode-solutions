# [Problem 2014: Longest Subsequence Repeated k Times](https://leetcode.com/problems/longest-subsequence-repeated-k-times/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This asks for the longest subsequence `seq` such that `seq * k` (seq repeated k times) is a subsequence of `s`. Brute force over all subsequences is impossible. Observations:
- The length of any valid `seq` is at most n // k (because seq repeated k times must fit into s as subsequence).
- We need the longest length, and if ties, lexicographically largest.
- A common pattern: generate candidate subsequences in increasing length layers, validate whether `seq * k` is a subsequence of s. BFS by length gives us increasing lengths; the last non-empty layer are the longest valid sequences. To satisfy lexicographic tie-breaking, within a layer choose the lexicographically largest.
- Efficient subsequence checking for many candidates suggests precomputing "next occurrence" (next_pos) so we can test quickly whether a string is a subsequence.
- Also we can prune using character frequencies: if s doesn't contain enough of some character to cover k times the count in seq, seq cannot be valid.

So approach: BFS layer-by-layer, extend candidates by one character at a time (try 'z'->'a' preference for lexicographic priority), use next_pos to validate seq*k, and use frequency pruning.

## Refining the problem, round 2 thoughts
Refinements and important details:
- Build next_pos array of size (n+1) x 26, where next_pos[i][c] = earliest index >= i where char c appears, or -1. This allows checking subsequence membership in O(k * len(seq)) steps by simulating matching `seq` repeated k times.
- Use BFS layer expansion: start with [''] (empty), then for each sequence in current layer attempt to append characters 'z' down to 'a' (so when selecting lexicographically largest among same length, we can easily choose max at the end). Keep next layer only with strings that pass the subsequence test.
- Prune quickly by counting occurrences: precompute freq of s, and for a sequence candidate new_seq, if for any char c, freq[c] < k * count_in_new_seq[c], skip subsequence check.
- Complexity: next_pos precompute O(26*n). Each subsequence check costs O(k * len(seq)). The number of validated candidates is typically small because frequency and subsequence constraints restrict branching strongly; worst-case behavior is mitigated by constraints (n <= 2000 and n < k*8 cap).
- Edge cases: If no non-empty subsequence qualifies, return empty string.

Now provide the implementation.

## Attempted solution(s)
```python
from collections import Counter

class Solution:
    def longestSubsequenceRepeatedK(self, s: str, k: int) -> str:
        n = len(s)
        # build next_pos table: next_pos[i][c] = earliest index >= i where char c appears, else -1
        next_pos = [[-1] * 26 for _ in range(n + 1)]
        for c in range(26):
            next_pos[n][c] = -1
        for i in range(n - 1, -1, -1):
            # copy from i+1
            row_next = next_pos[i + 1]
            cur_row = next_pos[i]
            for c in range(26):
                cur_row[c] = row_next[c]
            cur_row[ord(s[i]) - 97] = i

        # quick function: check if seq * k is a subsequence of s using next_pos
        def is_valid(seq: str) -> bool:
            if not seq:
                return True
            pos = 0
            for _ in range(k):
                for ch in seq:
                    cidx = ord(ch) - 97
                    idx = next_pos[pos][cidx]
                    if idx == -1:
                        return False
                    pos = idx + 1
                    if pos > n:
                        # can't match more
                        return False
            return True

        # frequency pruning: precompute freq of s
        freq = Counter(s)

        # BFS by length layers
        cur = ['']  # start with empty
        best = ''   # best (longest) found; empty if none valid non-empty
        while cur:
            next_layer = []
            # For lexicographic preference, try 'z' down to 'a' when appending
            for seq in cur:
                # For each possible character, append and test
                # iterate from 'z' to 'a' to bias lexicographically larger strings earlier
                for c_ord in range(25, -1, -1):
                    ch = chr(c_ord + 97)
                    new_seq = seq + ch
                    # pruning by frequency: each character needed in new_seq must be available k * count_in_new_seq in s
                    need = Counter(new_seq)
                    feasible = True
                    for cc, cnt in need.items():
                        if freq[cc] < cnt * k:
                            feasible = False
                            break
                    if not feasible:
                        continue
                    # actual subsequence check
                    if is_valid(new_seq):
                        next_layer.append(new_seq)
            if not next_layer:
                break
            # keep lexicographically largest among this length (we want longest length first, BFS ensures length growth)
            best = max(next_layer)  # lexicographically largest among sequences of this (max) length
            cur = next_layer
        return best
```
- Notes about the approach:
  - We layer-by-layer grow candidate subsequences; BFS ensures we find maximal length sequences when no further extension is possible.
  - Using next_pos makes the subsequence check efficient (we step through s via precomputed next indices).
  - The frequency pruning avoids many needless subsequence checks: if s doesn't have enough of a character to support k times the occurrences in the candidate, skip it.
  - Time complexity: building next_pos is O(26 * n). The cost of validation for a candidate seq is O(k * len(seq)). The number of validated candidates is constrained heavily by character availability and the subsequence structure; worst-case theoretical branching is 26^L but practically constrained by the problem limits (n <= 2000 and n < k * 8).
  - Space complexity: O(26 * n) for next_pos plus storage for current/next layer of candidates.