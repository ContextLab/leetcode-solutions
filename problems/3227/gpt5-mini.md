# [Problem 3227: Vowels Game in a String](https://leetcode.com/problems/vowels-game-in-a-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We have Alice (must remove a non-empty substring with an odd number of vowels) and Bob (must remove a non-empty substring with an even number of vowels). Alice moves first. If the current string contains no vowels, Alice immediately loses. If it contains vowels, Alice can at least remove a single vowel (a substring of length 1 with 1 vowel). The game looks like it might depend on positions of vowels and consonants, since Bob can remove consonant-only substrings (0 vowels) and thus "stall". But this kind of combinatorial game often admits a simple invariant or a strategy-stealing argument: if the first player (Alice) has any legal move, she may be able to force a win by an appropriate first move and then "stealing" any hypothetical winning strategy for Bob.

My first thought: check number of vowels parity. If odd, Alice can remove the whole string and win immediately. If zero, she loses. If even and >0, it's less obvious, but consider that Alice can always remove a single vowel; then try to argue she can force a win thereafter. Strategy-stealing often proves that if there is at least one legal move for the first player, the first player has a winning strategy in similar impartial games.

## Refining the problem, round 2 thoughts
Edge cases:
- No vowels -> Alice has no move -> return False.
- Odd vowel count -> Alice can remove whole string -> return True.
- Even vowel count > 0 -> need argument. Rather than build complex DP/Grundy over substrings, the problem admits a simple global reasoning: if a vowel exists, Alice has at least one move. Suppose, for contradiction, that Alice does not have a winning move but Bob does (i.e., Bob has a winning strategy after Alice's first move). Alice can remove a single vowel as her first move. After that removal, if Bob has a winning reply, Alice could instead have begun by performing the first part of that winning reply (strategy stealing): removing a character from the position Bob would have removed in that winning strategy, which is also a legal odd/even-vowel move because removing a single vowel is always legal for Alice. This leads to contradiction. Informally: once there is at least one vowel, Alice can always force a win. So the rule simplifies to: Alice wins iff the string contains at least one vowel.

Time/space: scanning string for any vowel is O(n) time and O(1) extra space.

(This reasoning is the typical strategy-stealing flavor used for many first-player-win proofs: any assumed Bob-winning reply can be subverted since Alice has at least one free legal move at the start — removing one vowel — and can simulate/steal Bob's strategy afterwards. The detailed formalization can be done but is standard.)

## Attempted solution(s)
```python
class Solution:
    def vowelsGame(self, s: str) -> bool:
        vowels = set('aeiou')
        for ch in s:
            if ch in vowels:
                return True
        return False
```
- Notes about the solution approach:
  - We simply check whether the string contains any vowel.
  - If no vowel exists, Alice has no legal first move and loses -> return False.
  - If at least one vowel exists, Alice has a winning strategy -> return True (odd count immediate win or strategy-stealing for other cases).
- Complexity:
  - Time: O(n) where n = len(s), a single pass to check for vowels.
  - Space: O(1) extra space.