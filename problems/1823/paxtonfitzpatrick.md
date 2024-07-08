# [Problem 1823: Find the Winner of the Circular Game](https://leetcode.com/problems/find-the-winner-of-the-circular-game/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- pretty sure there's going to be an analytic solution that runs in $O(1)$ time & space for this, but it's not immediately obvious to me what it is...
- interesting that the constraints say `k` will never be larger than `n`, I wonder if that's significant...
- going to try to brute-force this first and see if I can find a pattern in the output
- could do something involving `itertools.cycle` again, but that's probably going to be inefficient since the iterable (remaining players) will change each round
- I think I'll need to keep track of my current index in the players circle (list) and increment/update it each round. That way if I `pop` the `i`th player from the list, `i` will immediately refer to the player to the right (clockwise) of the removed player, which is who I want to start with next round.
- I think I need to use modulo to deal with the wrap-around... how will that help...
- ah, instead of starting to count from the player at the current index `i`, I can start from the 1st player, add my current offset `i` from the start of the players list, and then mod *that* by the current length of the list to get my new player index to remove.
- Since we cound the 1st player as 1, 2nd player as 2, etc., I'll need to subtract 1 from the index I want to remove


## Refining the problem, round 2 thoughts

- How might we go about solving this in constant time...
- I don't see a clear pattern in the output when holding `n` or `k` constant and incrementing the other... maybe it's related to the cumulative sum of the player positions?
- thought through this for a while, broke down and decided to google it. Turns out this is the [Josephus problem](https://en.wikipedia.org/wiki/Josephus_problem) and there isn't a constant-time solution for the general case. There *is* an $O(k \mathrm{log} n)$ solution that involves recursion and memoization, but for the sake of time I'm going to be satisfied with my $O(n)$ version.

## Attempted solution(s)

```python
class Solution:
    def findTheWinner(self, n: int, k: int) -> int:
        players = list(range(1, n+1))
        ix_to_remove = 0

        while len(players) > 1:
            ix_to_remove = (ix_to_remove + k - 1) % len(players)
            players.pop(ix_to_remove)

        return players[0]
```

![](https://github.com/paxtonfitzpatrick/leetcode-solutions/assets/26118297/500020af-9383-4ddc-82c2-b40fa68c3106)
