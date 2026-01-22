# [Problem 2410: Maximum Matching of Players With Trainers](https://leetcode.com/problems/maximum-matching-of-players-with-trainers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I see this as a matching / assignment problem where a player can be matched to a trainer if trainer.capacity >= player. The natural greedy that comes to mind is to sort both lists and try to match smallest players first with the smallest trainer that can handle them. That way we don't waste a big-capacity trainer on a small-ability player when a smaller trainer could suffice. Two pointers after sorting seems ideal and linear after the sorts. This reminds me of "Assign Cookies" (LeetCode 455) and indeed the note says it's the same problem.

## Refining the problem, round 2 thoughts
- Sorting both arrays ascending and using two pointers (i for players, j for trainers) is straightforward: if trainers[j] >= players[i] then match and advance both; otherwise advance j (trainer too weak).
- Alternative: sort descending and match largest to largest — also works, but ascending two-pointer is simpler to explain/implement.
- Edge cases: all trainers too weak -> zero matches; more players than trainers or vice versa handled naturally by pointer termination.
- Complexity: sorting dominates -> O(n log n + m log m), scanning is O(n + m). Space: O(1) extra beyond input (or O(n + m) if sorting copies).
- Correctness: greedy of matching smallest feasible trainer to smallest player is optimal (keeps larger trainers available for larger players).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def matchPlayers(self, players: List[int], trainers: List[int]) -> int:
        # Sort both lists ascending
        players.sort()
        trainers.sort()
        
        i = 0  # pointer for players
        j = 0  # pointer for trainers
        matches = 0
        
        n = len(players)
        m = len(trainers)
        
        # Two-pointer greedy: match smallest player with smallest feasible trainer
        while i < n and j < m:
            if trainers[j] >= players[i]:
                matches += 1
                i += 1
                j += 1
            else:
                # trainer too weak for this player, try next trainer
                j += 1
        
        return matches
```
- Notes:
  - Approach: sort both arrays and use two pointers to greedily match the smallest remaining player with the smallest trainer that can handle them.
  - Correctness: Matching the smallest feasible trainer to each smallest player preserves larger trainers for larger players, which is optimal (standard greedy argument as in "Assign Cookies").
  - Time complexity: O(n log n + m log m) due to sorting (n = len(players), m = len(trainers)). Two-pointer scan is O(n + m).
  - Space complexity: O(1) extra (in-place sorting) or O(n + m) if sorts produce copies depending on language/runtime.