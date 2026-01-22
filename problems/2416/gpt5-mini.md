# [Problem 2416: Sum of Prefix Scores of Strings](https://leetcode.com/problems/sum-of-prefix-scores-of-strings/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the sum, for each word, of counts of how many words have each non-empty prefix of that word. That is, for every prefix string p of word w, we want the number of words in the list that start with p, and sum those counts.

A straightforward idea: build a map from prefix -> frequency by enumerating all prefixes of every word, then for each word sum the frequencies of its prefixes. That is simple and correct, but in Python repeated slicing to form prefixes may be costly in time/space when strings are long (up to 1000) and many words (up to 1000) — total characters up to ~1e6. Also storing all prefixes as separate strings could blow memory.

A trie (prefix tree) naturally stores prefixes without repeated string copies and lets us maintain a counter at each node of how many words pass through that node (i.e., how many words have that prefix). So: insert every word into a trie and increment node counts; then for each word traverse the trie and sum the node counts for its characters. This gives O(total_chars) time for both build and query phases.

## Refining the problem, round 2 thoughts
- Constraints: n up to 1000, each word length up to 1000, total characters L up to ≈1e6. So solution must be roughly linear in L.
- Implementation detail: a trie node with a fixed-size array of 26 children is convenient but in Python that uses a lot of memory for many nodes (26 references per node). Using dictionaries for children is much more memory-friendly because most nodes have few children.
- Edge cases: single-word list, repeated identical words, long words — the algorithm handles these naturally.
- Complexity: building trie + querying is O(L) time where L is sum of lengths of all words, and O(L) space for trie nodes and counts (with dictionary children storage).

## Attempted solution(s)
```python
class Solution:
    def sumPrefixScores(self, words: list[str]) -> list[int]:
        # Build a trie using dict children to save memory.
        children = [{}]  # children[i] is a dict mapping char -> node_index
        count = [0]      # count[i] is number of words that pass through node i (i.e., prefix occurrences)
        
        # Insert all words, incrementing counts along the path for each character
        for w in words:
            node = 0
            for ch in w:
                nxt = children[node].get(ch)
                if nxt is None:
                    nxt = len(children)
                    children[node][ch] = nxt
                    children.append({})
                    count.append(0)
                node = nxt
                count[node] += 1
        
        # For each word, traverse its path and sum the counts at each node (prefix scores)
        ans = []
        for w in words:
            node = 0
            s = 0
            for ch in w:
                node = children[node][ch]
                s += count[node]
            ans.append(s)
        
        return ans
```
- Notes:
  - We use a list of dicts to represent the trie nodes: children[i] is a dict mapping char -> child node index. count[i] stores how many words include the prefix represented by node i.
  - First pass: insert all words, creating nodes as needed and incrementing counts at the node for each character (non-empty prefixes).
  - Second pass: for each word, traverse characters and sum count at each node encountered to get the required sum of prefix scores for that word.
  - Time complexity: O(L) where L is the sum of lengths of all words (each character processed a constant number of times).
  - Space complexity: O(L) for trie nodes and counts (plus overhead of dictionaries). This is memory-efficient compared to using 26-length arrays per node in Python.