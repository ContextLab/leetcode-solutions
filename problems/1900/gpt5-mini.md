# [Problem 1900: The Earliest and Latest Rounds Where Players Compete](https://leetcode.com/problems/the-earliest-and-latest-rounds-where-players-compete/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have n players in fixed original positions 1..n. Each round pairs front-to-back: 1 vs n, 2 vs n-1, etc., with the middle auto-advancing if odd. After each round, winners are lined up by their original numbering ascending. Two special players (firstPlayer and secondPlayer) always beat anyone else, so they only can be eliminated by meeting each other. For other vs other matches, outcomes are arbitrary and we can choose them to either accelerate or delay the meeting of the two special players.

We need earliest and latest round they could meet. This suggests exploring possibilities of how matches between non-special players resolve and tracking which players survive to the next round. Because n <= 28, we can encode alive players as a bitmask and do a recursive search (DFS) over possible outcomes of each round, with memoization on the alive-mask.

Key observation: the lineup order for a round is always the alive players sorted by original index. So for a given mask we can compute the pairing deterministically. For each pair: if it contains both special players -> they meet now. If a pair contains one special + other -> special wins deterministically. If a pair is other vs other -> two choices (left wins or right wins). For an odd middle player, they auto-advance. We can enumerate the 2^k choices for non-special-vs-non-special matches (k <= 14), build the next-mask of winners (sorted by original indices implicitly), and recurse. Memoize mask -> (earliest, latest).

This brute-force-with-memo works because worst-case branching per round is limited (2^14 states for a round), and masks visited are limited by n <= 28.

## Refining the problem, round 2 thoughts
Edge cases:
- If the two special players are paired in the current round, earliest=latest=current round for this mask.
- They never lose to others, so they always stay alive unless they face each other, which simplifies assumptions.
- Representing players by their original indices and using a bitmask captures both identity and the ordering rule (winners are resorted ascending by their original indices).

Complexity:
- Each DFS call constructs the alive list (O(n)) and enumerates up to 2^k possible outcomes where k is the number of other-vs-other pairs in that round (k <= floor(n/2) <= 14). The total number of distinct masks reachable is limited, and memoization prevents rework. Practically this is fine for n up to 28.

Now implement the described DFS + memoization.

## Attempted solution(s)
```python
from functools import lru_cache

class Solution:
    def earliestAndLatest(self, n: int, firstPlayer: int, secondPlayer: int):
        # Use 1-based player indices. mask bit i-1 corresponds to player (i).
        FULL_MASK = (1 << n) - 1
        a = firstPlayer
        b = secondPlayer

        @lru_cache(None)
        def dfs(mask: int):
            # Build list of alive players (ascending original index)
            ids = []
            msk = mask
            idx = 1
            while msk:
                if msk & 1:
                    ids.append(idx)
                idx += 1
                msk >>= 1
            m = len(ids)

            # find positions (0-based) of the two special players in current lineup
            # they are guaranteed to be alive here (they never lose to others)
            pos_a = ids.index(a)
            pos_b = ids.index(b)

            # If they meet this round: their positions pair up (i with m-1-i)
            if pos_a + pos_b == m - 1:
                return (1, 1)

            # Otherwise enumerate outcomes of this round
            # We'll backtrack over pairs from outer towards center
            res_min = float('inf')
            res_max = -float('inf')

            winners = []

            def backtrack(i, j):
                nonlocal res_min, res_max
                # i is left index, j is right index in ids
                if i > j:
                    # no more pairs -> compute next mask and recurse
                    next_mask = 0
                    for w in winners:
                        next_mask |= 1 << (w - 1)
                    # Recurse on next round
                    sub_min, sub_max = dfs(next_mask)
                    # add current round
                    res_min = min(res_min, 1 + sub_min)
                    res_max = max(res_max, 1 + sub_max)
                    return

                if i == j:
                    # middle player auto-advances
                    winners.append(ids[i])
                    backtrack(i + 1, j - 1)
                    winners.pop()
                    return

                left = ids[i]
                right = ids[j]

                # If this pair contains both special players, they would have met earlier (caught above).
                # If it contains a special player, that player always wins.
                if left == a or left == b:
                    winners.append(left)
                    backtrack(i + 1, j - 1)
                    winners.pop()
                    return
                if right == a or right == b:
                    winners.append(right)
                    backtrack(i + 1, j - 1)
                    winners.pop()
                    return

                # Otherwise both are "other" players: two choices (left wins or right wins)
                winners.append(left)
                backtrack(i + 1, j - 1)
                winners.pop()

                winners.append(right)
                backtrack(i + 1, j - 1)
                winners.pop()

            backtrack(0, m - 1)

            return (res_min, res_max)

        return list(dfs(FULL_MASK))
```
- Notes on approach:
  - State is a bitmask of alive players; the lineup for a round is the alive players in ascending original index order.
  - For a given mask, if the two special players are paired this round, they meet now -> return (1,1).
  - Otherwise, enumerate outcomes for matches that don't involve the special players (each such match gives two possible winners). For each resulting next-mask of winners, recursively compute earliest/latest, and add 1 for the current round. Memoize results per mask to avoid recomputation.
  - Time complexity: Each state processes up to O(n) to build ids and enumerates up to 2^k outcomes where k <= floor(n/2) (≤14). The total number of distinct masks visited is limited; with memoization this is efficient enough for n ≤ 28.
  - Space complexity: O(number_of_masks) memoization, each mask is an integer key; recursion depth is O(log n) rounds.