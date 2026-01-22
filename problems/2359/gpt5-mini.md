# [Problem 2359: Find Closest Node to Given Two Nodes](https://leetcode.com/problems/find-closest-node-to-given-two-nodes/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have a directed graph where each node has at most one outgoing edge — that means every node's forward traversal is a simple walk that either ends at -1 or enters a cycle. For each start node (node1 and node2) we can walk forward once, recording distances to every visited node. After we have two distance arrays, the candidate nodes reachable from both are those with distances != -1 in both arrays. For each candidate compute max(dist1[i], dist2[i]) and pick the node with the minimal such value (ties broken by smallest index). The traversal from a node is linear in the number of visited nodes; because edges are at most one per node, total work is O(n).

Potential pitfalls: cycles must be handled to avoid infinite loops — marking visited (or using distance array as visited) handles that. Need to return -1 if no common reachable node.

## Refining the problem, round 2 thoughts
Refinements:
- Use two arrays dist1 and dist2 initialized to -1. Walk from node1 and node2 separately; on the first visit to a node fill its distance. Stop walking when next is -1 or node already seen (dist != -1).
- After both traversals, iterate all nodes (0..n-1) and evaluate only nodes where both distances are != -1. Keep track of the minimum maximum distance and index.
- Time complexity: O(n) because each node is visited at most once in each traversal; overall O(n). Space complexity: O(n) for two distance arrays.
- Edge cases: node1 == node2 (the algorithms still works), unreachable nodes (remain -1), cycle reachable from one start but not the other — handled by checks.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def closestMeetingNode(self, edges: List[int], node1: int, node2: int) -> int:
        n = len(edges)
        
        def build_dist(start: int) -> List[int]:
            dist = [-1] * n
            cur = start
            d = 0
            while cur != -1 and dist[cur] == -1:
                dist[cur] = d
                d += 1
                cur = edges[cur]
            return dist
        
        dist1 = build_dist(node1)
        dist2 = build_dist(node2)
        
        best_node = -1
        best_dist = float('inf')
        for i in range(n):
            d1 = dist1[i]
            d2 = dist2[i]
            if d1 != -1 and d2 != -1:
                m = max(d1, d2)
                if m < best_dist or (m == best_dist and i < best_node):
                    best_dist = m
                    best_node = i
        return best_node
```
- Notes:
  - Approach: compute distance arrays from node1 and node2 by following the single outgoing edge repeatedly, marking distances on first visit. Then choose the node minimizing the maximum of the two distances, tie-breaking by smallest index.
  - Time complexity: O(n) — each node is visited at most once per start node, so at most 2n visits.
  - Space complexity: O(n) — two distance arrays of size n.
  - Implementation detail: using dist array entries initialized to -1 both records distances and acts as visited markers to stop on cycles or repeated visits.