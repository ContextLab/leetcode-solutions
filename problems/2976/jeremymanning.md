# [Problem 2976: Minimum Cost to Convert String I](https://leetcode.com/problems/minimum-cost-to-convert-string-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- The wording of this problem is a bit confusing.  To my reading, we have our `source` and `target` strings, and then `original`, `changed`, and `cost` are all telling us about character change costs.  I'm assuming those character changes are the only operations allowed.  Further, I'm assuming that we might encounter a situation where we have to swap some character `a` to `c` via two (or more) intermediate characters, such as `a --> b --> c`.  So under that framing, this is a shortest paths graph problem:
  - Rows are original letters
  - Columns are changed letters
  - Entries are the costs of moving from the original to changed letters
  - For each character `i` in `source` that doesn't match its corresponding character `j` in `target`, we want to find the shortest path that changes `i` to `j`.
  - Then we'll add up the lengths of the shortest paths and return them.
- One approach would be to re-use our code from [yesterday's problem](https://github.com/ContextLab/leetcode-solutions/blob/main/problems/1334/jeremymanning.md), where we used the Floyd-Warshall algorithm to solve *all* shortest paths.
    - We don't necessarily need to compute *all* paths-- just the ones necessary to get form `source` to `target`.  So instead we could use Dijkstra's algorithm to compute individual shortest paths, and then cache the results so that we don't need to recompute them:

    ![Screenshot 2024-07-26 at 11 33 36 PM](https://github.com/user-attachments/assets/e668dcc9-0f82-4b76-a965-45e35a22a72d)
    
    - If there is *no* path from the current character to the desired target character, we can just return -1 and skip any further computations, because it's impossible to convert the string.

## Refining the problem, round 2 thoughts
- Let's use a helper function to compute shortest paths between two characters, `i` and `j`, using Dijkstra's algorithm
- We'll maintain a hash table of already-computed distances
- Then we can call the helper function as needed, using cached values along the way if possible
- One challenge: what if we encounter some other character, `k` along the path from `i` to `j`.  On one hand, we should be able to use the fact that we've gotten from `i` to `k` in future computations.  On the other hand, how could we know it was the *shortest* path from `i` to `k` if we haven't explored the other nodes yet (e.g., if we terminate Dijkstra's algorithm after reaching the target node)?  It seems like we have two options:
    - We could use the Floyd-Warshall algorithm to compute all shortest paths (between every pair of nodes) and then store that.  The memory cost is high (although...maybe not too bad actually, since we're limited to English lowercase letters-- so in the worst case we're looking at a $26 \times 26$ matrix, which....actually isn't bad at all...)
    - Or we could use Dijkstra's algorithm, but since we can't cache intermediate values effectively (or...at least I can't see off the top of my head out how to do that!) we'd pay an additional *time* cost.
- So actually, in re-thinking this, I now wonder if we should just re-use snippets from yesterday's problem and adapt them here.  I'm going to try that, using the approach described above.

## Attempted solution(s)
```python
import math

class Solution:
    def minimumCost(self, source: str, target: str, original: List[str], changed: List[str], cost: List[int]) -> int:
        letters = list(set(source).union(set(target)).union(set(original)).union(set(changed)))
        n = len(letters)
        
        let2ind = {x: i for i, x in enumerate(letters)}
            
        # Copying from yesterday's code...
        dists = [[float('inf')] * n for _ in range(n)]
        
        # The distance from each letter to itself is zero
        for i in range(n):
            dists[i][i] = 0
        
        # Add the edges
        for a, b, cost in zip(original, changed, cost):
            dists[let2ind[a]][let2ind[b]] = cost
        
        # Fill in the shortest path between all pairs
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dists[i][j] > dists[i][k] + dists[k][j]:
                        dists[i][j] = dists[i][k] + dists[k][j]
        
        # Now add up the change costs
        cost = 0
        for a, b in zip(source, target):
            if a != b:
                next_cost = dists[let2ind[a]][let2ind[b]]
                if math.isinf(next_cost):
                    return -1
                cost += next_cost
        
        return cost
```
- Given test cases pass
- Let's make up some others...
    - `source = "alswefkjhasdfjh", target = "dfskuysdfbjknsd", original = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"], changed = ["o", "c", "n", "j", "v", "x", "b", "d", "s", "w", "f", "q", "e", "h", "u", "l", "k", "t", "r", "m", "g", "z", "i", "a", "p", "y"], cost = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]`: pass!
    - `source = "qnblqsvdpwjdyclxnklfofgrhlzbot", target = "uzboldidkqirqmnwxqdlqhmbeqycvv", original = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"], changed = ["o", "c", "n", "j", "v", "x", "b", "d", "s", "w", "f", "q", "e", "h", "u", "l", "k", "t", "r", "m", "g", "z", "i", "a", "p", "y"], cost = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]`: pass!
- Ok, submitting...

![Screenshot 2024-07-27 at 12 11 09 AM](https://github.com/user-attachments/assets/2cc8a646-f801-47c2-a3a6-c0a55feb3e07)

Oh no!!  Sad trumpet 🎺🎵😿

Looking at the test case that failed (#531), I'm wondering (given the super long source/target/original/changed/cost variables) if maybe there are some paths that are repeated.  So maybe instead of assuming each edge is represented only once, I should instead account for multiple edges (e.g., maybe a given character change from `i` to `j` appears multiple times, but potentially with different costs)?

```python
import math

class Solution:
    def minimumCost(self, source: str, target: str, original: List[str], changed: List[str], cost: List[int]) -> int:
        letters = list(set(source).union(set(target)).union(set(original)).union(set(changed)))
        n = len(letters)
        
        let2ind = {x: i for i, x in enumerate(letters)}
            
        # Copying from yesterday's code...
        dists = [[float('inf')] * n for _ in range(n)]
        
        # The distance from each letter to itself is zero
        for i in range(n):
            dists[i][i] = 0
        
        # Add the edges
        for a, b, cost in zip(original, changed, cost):
            dists[let2ind[a]][let2ind[b]] = min(cost, dists[let2ind[a]][let2ind[b]])
        
        # Fill in the shortest path between all pairs
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if dists[i][j] > dists[i][k] + dists[k][j]:
                        dists[i][j] = dists[i][k] + dists[k][j]
        
        # Now add up the change costs
        cost = 0
        for a, b in zip(source, target):
            if a != b:
                next_cost = dists[let2ind[a]][let2ind[b]]
                if math.isinf(next_cost):
                    return -1
                cost += next_cost
        
        return cost
```

- Submitting this version...

![Screenshot 2024-07-27 at 12 19 48 AM](https://github.com/user-attachments/assets/15660a60-f8b3-402a-b868-405b8d12dec0)

Phew!  I kind of feel like this problem's instructions were annoying and unnecessarily tricky-- the wording is a bit obfuscated, and then there's this strange case where costs are listed multiple times.  I suppose it's technically valid?  Sigh...




