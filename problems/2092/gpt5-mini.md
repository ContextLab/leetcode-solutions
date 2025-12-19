# [Problem 2092: Find All People With Secret](https://leetcode.com/problems/find-all-people-with-secret/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to simulate secret spread across meetings, but meetings can happen at same time and the secret spreads instantaneously across connected meetings at that same time. That suggests grouping meetings by time and processing time-by-time. Within a single time, multiple meetings form a graph (or connected components): if any node in a component already knows the secret at that time, the secret spreads to the whole component instantly. So for each time, build the connectivity among participants, determine which components contain a knower, and mark all nodes in those components as knowing the secret. Sorting meetings by time or grouping by time is necessary. Union-Find or BFS/DFS on the per-time graph both work.

## Refining the problem, round 2 thoughts
Refinements:
- Maintain a global set "know" initially containing 0 and firstPerson (0 shares to firstPerson at time 0).
- Sort meetings by time or bucket them; then process each time's meetings together.
- For the meetings at a single time t: create a subgraph among participants of those meetings. Use union-find (fast) to group components, or adjacency list + BFS from known nodes in that time. Using union-find is concise: union every pair in the time group, then check which roots contain any knower.
- After processing a time, only nodes that become known remain known for later times (do not carry forward edges).
- Time complexity: sorting meetings O(m log m), processing unions/finds O(m α(n)). Space O(n + m) for grouping.
- Edge cases: If none of the participants in a time group know the secret at that time, nobody in that group becomes known. Multiple meetings can involve same person; union-find handles that.

## Attempted solution(s)
```python
from collections import defaultdict

class Solution:
    def findAllPeople(self, n: int, meetings: list[list[int]], firstPerson: int) -> list[int]:
        # Group meetings by time
        time_map = defaultdict(list)
        for x, y, t in meetings:
            time_map[t].append((x, y))
        # Process times in increasing order
        times = sorted(time_map.keys())
        # Initially, person 0 and firstPerson know the secret
        know = {0, firstPerson}

        for t in times:
            pairs = time_map[t]
            # collect all participants in this time
            participants = set()
            for x, y in pairs:
                participants.add(x)
                participants.add(y)
            # build union-find for participants only
            parent = {p: p for p in participants}
            rank = {p: 0 for p in participants}

            def find(a):
                # path compression
                while parent[a] != a:
                    parent[a] = parent[parent[a]]
                    a = parent[a]
                return a

            def union(a, b):
                ra, rb = find(a), find(b)
                if ra == rb:
                    return
                if rank[ra] < rank[rb]:
                    parent[ra] = rb
                else:
                    parent[rb] = ra
                    if rank[ra] == rank[rb]:
                        rank[ra] += 1

            for x, y in pairs:
                union(x, y)

            # Determine which components have at least one knower
            roots_with_secret = set()
            for p in participants:
                if p in know:
                    roots_with_secret.add(find(p))

            # Those in components whose root is in roots_with_secret get the secret
            newly_known = set()
            if roots_with_secret:
                for p in participants:
                    if find(p) in roots_with_secret:
                        newly_known.add(p)

            # update global known set
            know |= newly_known

        return list(know)
```
- Approach notes: We group meetings by time and process each time separately. For each time group we perform unions among participants to form connected components. If any participant in a component already knows the secret before processing this time, everyone in that component learns it immediately. We then update the global known set and proceed to the next time.
- Complexity:
  - Let m = number of meetings, n = number of people.
  - Time: O(m log m) for sorting times + O(m α(n)) for union/find across all meetings (α is inverse-Ackermann, effectively constant).
  - Space: O(n + m) for grouping and per-time structures (parents/ranks only for participants of that time).