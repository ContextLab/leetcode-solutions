# [Problem 2976: Minimum Cost to Convert String I](https://leetcode.com/problems/minimum-cost-to-convert-string-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- okay, so this is going to be another shortest path problem. Letters are nodes, corresponding indices in `original` and `changed` are directed edges, and those same indices in `cost` give their weights.
- I was originally thinking I'd want to find all min distances between letters using something similar to yesterday's problem (Floyd-Warshall algorithm), but i actually think it'll be more efficient to figure out what letters we need to convert first and then searching just for those. So I think this is calling for Djikstra's algorithm.
- so I'll loop through `source` and `target`, identify differences, and store source-letter + target-letter pairs.
  - if a source letter isn't in `original` or a target letter isn't in `changed`, I can immediately `return -1`
  - actually, I think I'll store the source and target letters as a dict where keys are source letters and values are lists (probably actually sets?) of target letters for that source letter. That way if I need to convert some "a" to a "b" and some other "a" to a "c", I can save time by combining those into a single Djikstra run.
- then I'll run Djikstra's algorithm starting from each source letter and terminate when I've found paths to all target letters for it.
- I'll write a helper function for Djikstra's algorithm that takes a source letter and a set of target letters, and returns a list (or some sort of container) of minimum costs to convert that source letter to each of the target letters.

---

- after thinking through how to implement Djikstra here a bit, I wonder if Floyd-Warshall might actually be more efficient... Floyd-Warshall's runtime scales with the number of nodes, but since nodes here are letters, we know there will always be 26 of them. So that's essentially fixed. Meanwhile Djikstra's runtime scales with the number of nodes *and* edges, and since the constraints say there can be upto 2,000 edges, we're likely to have a large number of edges relative to the number of nodes. That also means we're much more likely to duplicate operations during different runs of Djikstra than we would be if the graph were large and sparse. So I think I'll actually try Floyd-Warshall first.

## Refining the problem, round 2 thoughts

- we could reduce the size of the distance matrix for the Floyd-Warshall algorithm by including only the letters in `original` and `changed` instead of all 26. But I doubt this would be worth it on average, since it'd only sometimes reduce the number of nodes in the graph and always incur overhead costs of converting `original` and `changed` to sets, looping over letters and converting them to indices instead of looping over indices directly, etc.
  - speaking of which, I'll still have to loop over letters and convert them to indices in order to extract the conversion costs for mismatched letters, and I can think of two ways to do this:
    - store a letters/indices mapping in a `dict`, i.e. `{let: i for i, let in enumerate('abcdefghijklmnopqrstuvwxyz')}` and index it with each letter
    - use `ord(letter)` to get the letter's ASCII value and subtract 97 (ASCII value of "a") to get its index in the alphabet

    Both operations would take constant time, but constructing the `dict` will use a little bit of additional memory so I think I'll go with the latter.
  - hmmm actually, if I can just use a dict as the letter/index mapping, that might make reducing the size of the distance matrix worth it. Maybe I'll try that if my first attempt is slow.
- hmmm the problem notes that "*there may exist indices `i`, `j` such that `original[j] == original[i]` and `changed[j] == changed[i]`*". But it's not totally clear to me whether they're (A) simply saying that nodes may appear in both the `original` and `changed` lists multiple times because they can have multiple edges, or (B) saying that ***edges*** may be duplicated, potentially with different `cost` values -- i.e., `(original[j], changed[j]) == (original[i], changed[i])` but `cost[j] != cost[i]`. My guess is that it's the latter because the former seems like a sort of trivial point to make note of, so I'll want to account for this when I initialize the distance matrix.

## Attempted solution(s)

```python
class Solution:
    def minimumCost(self, source: str, target: str, original: List[str], changed: List[str], cost: List[int]) -> int:
        # setup min distance/cost matrix
        INF = float('inf')
        min_costs = [[INF] * 26 for _ in range(26)]
        for orig_let, changed_let, c in zip(original, changed, cost):
            orig_ix, changed_ix = ord(orig_let) - 97, ord(changed_let) - 97
            if c < min_costs[orig_ix][changed_ix]:
                min_costs[orig_ix][changed_ix] = c
        # run Floyd-Warshall
        for via_ix in range(26):
            for from_ix in range(26):
                for to_ix in range(26):
                    if min_costs[from_ix][via_ix] + min_costs[via_ix][to_ix] < min_costs[from_ix][to_ix]:
                        min_costs[from_ix][to_ix] = min_costs[from_ix][via_ix] + min_costs[via_ix][to_ix]
        # compute total cost to convert source to target
        total_cost = 0
        for src_let, tgt_let in zip(source, target):
            if src_let != tgt_let:
                src_ix, tgt_ix = ord(src_let) - 97, ord(tgt_let) - 97
                if min_costs[src_ix][tgt_ix] == INF:
                    return -1
                total_cost += min_costs[src_ix][tgt_ix]
        return total_cost
```

![](https://github.com/user-attachments/assets/2df1bdf7-8f66-4d28-90f8-12998425b3ba)

Not bad. But I'm curious whether creating a graph from only the letters in `original` and `changed` would be faster. It's a quick edit, so I'll try it. Biggest change will be an additional `return -1` condition in the last loop to handle letters in `source` and `target` that can't be mapped to/from anything.

```python
class Solution:
    def minimumCost(self, source: str, target: str, original: List[str], changed: List[str], cost: List[int]) -> int:
        # setup min distance/cost matrix
        INF = float('inf')
        letters = set(original) | set(changed)
        letters_ixs = {let: i for i, let in enumerate(letters)}
        len_letters = len(letters)
        min_costs = [[INF] * 26 for _ in range(len_letters)]
        for orig_let, changed_let, c in zip(original, changed, cost):
            if c < min_costs[letters_ixs[orig_let]][letters_ixs[changed_let]]:
                min_costs[letters_ixs[orig_let]][letters_ixs[changed_let]] = c
        # run Floyd-Warshall
        for via_ix in range(len_letters):
            for from_ix in range(len_letters):
                for to_ix in range(len_letters):
                    if min_costs[from_ix][via_ix] + min_costs[via_ix][to_ix] < min_costs[from_ix][to_ix]:
                        min_costs[from_ix][to_ix] = min_costs[from_ix][via_ix] + min_costs[via_ix][to_ix]
        # compute total cost to convert source to target
        total_cost = 0
        try:
            for src_let, tgt_let in zip(source, target):
                if src_let != tgt_let:
                    if (change_cost := min_costs[letters_ixs[src_let]][letters_ixs[tgt_let]]) == INF:
                        return -1
                    total_cost += change_cost
        except KeyError:
            return -1
        return total_cost
```

![](https://github.com/user-attachments/assets/263ad81c-900d-40d1-8602-ee5012e4b47e)

Wow, that made a much bigger difference than I expected!
