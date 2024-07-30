# [Problem 2045: Second Minimum Time to Reach Destination](https://leetcode.com/problems/second-minimum-time-to-reach-destination/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- okay, this one looks tricky. One initial thought I have is that a path that involves revisiting some node will be the second shortest path only if there aren't two paths that *don't* involve revisiting a node. So I think I can ignore that outside of those specific cases.
- It sounds like we'll need to use some algorithm that finds *all* paths between a target and destination node. I know Djikstra's algorithm can be modified to terminate early upon encountering a target node, so maybe there's a way to modify it such that it terminates when it encounters that node a second time?

## Refining the problem, round 2 thoughts

### Other notes

## Attempted solution(s)

```python
class Solution:
    def secondMinimum(self, n: int, edges: List[List[int]], time: int, change: int) -> int:

```
