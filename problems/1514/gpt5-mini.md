# [Problem 1514: Path with Maximum Probability](https://leetcode.com/problems/path-with-maximum-probability/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the path from start to end that maximizes the product of edge success probabilities. That is like shortest path but with multiplication instead of sum. Two obvious approaches come to mind:

- Convert probabilities by taking log and turn the product into a sum (maximize product -> minimize negative log). Then run standard Dijkstra for shortest path on the transformed weights.
- Or run a modified Dijkstra that directly keeps track of the maximum probability to reach each node and uses a max-priority-queue (greedy relaxation): when we pop the node with the current highest known probability, relax its neighbors by multiplying by edge probability. This is simpler and numerically stable (no log needed).

Because the graph is undirected and edges ≤ 2e4 and nodes ≤ 1e4, a Dijkstra-style approach with a heap is efficient.

## Refining the problem, round 2 thoughts
- Edge cases: if there's no path, return 0. If some succProb are 0, they won't help increase probabilities — that's fine.
- We can stop early when we pop the target node from the heap since the heap always gives the current maximum achievable probability to any node.
- Complexity: using adjacency list and heap, each edge is relaxed at most once (or up to twice for undirected), and each relaxation may push into the heap. Complexity roughly O(E log V).
- Space: adjacency list O(V + E), dist array O(V), heap O(V) worst-case.
- Implementation details: use heapq (min-heap) storing negative probabilities to simulate a max-heap, or store probability and invert comparisons; use float probabilities.

## Attempted solution(s)
```python
import heapq
from typing import List

class Solution:
    def maxProbability(self, n: int, edges: List[List[int]], succProb: List[float], start: int, end: int) -> float:
        # Build adjacency list
        graph = [[] for _ in range(n)]
        for (u, v), p in zip(edges, succProb):
            graph[u].append((v, p))
            graph[v].append((u, p))
        
        # dist[i] will store the maximum probability to reach node i from start
        dist = [0.0] * n
        dist[start] = 1.0
        
        # max-heap using negative probabilities because heapq is a min-heap
        heap = [(-1.0, start)]
        
        while heap:
            neg_prob, node = heapq.heappop(heap)
            prob = -neg_prob
            # If this popped probability is less than the recorded best, skip
            if prob < dist[node]:
                continue
            # Early exit: when we reached end with the highest possible probability
            if node == end:
                return prob
            # Relax neighbors
            for nei, edge_p in graph[node]:
                new_prob = prob * edge_p
                if new_prob > dist[nei]:
                    dist[nei] = new_prob
                    heapq.heappush(heap, (-new_prob, nei))
        
        return dist[end]
```
- Notes:
  - Approach: Modified Dijkstra that maximizes multiplicative probabilities directly using a max-priority queue.
  - Time complexity: O((V + E) log V) in practice, more precisely O(E log V) for sparse graphs with E edges and V nodes.
  - Space complexity: O(V + E) for adjacency list and O(V) for distance array and heap.
  - Important detail: we can stop as soon as we pop the end node from the heap because Dijkstra-like greedy property ensures that's the maximum achievable probability to end.