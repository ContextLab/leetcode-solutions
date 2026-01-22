# [Problem 1625: Lexicographically Smallest String After Applying Operations](https://leetcode.com/problems/lexicographically-smallest-string-after-applying-operations/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We can apply two operations any number of times: (1) add a to all digits at odd indices (mod 10), (2) rotate right by b. We want the lexicographically smallest reachable string.

Brute-forcing all possible strings is impossible in general, but the operations have structure:
- Rotation by b just permutes indices; repeating rotation cycles through a set of rotations of s (at most n distinct).
- Adding a to odd indices cycles each affected digit through at most 10 values (mod 10).
- Whether even indices can be changed by addition depends on b: if b is odd, rotating mixes parity, so by combining rotations and odd-index additions we can effectively alter even indices as well; if b is even, parity is preserved and only odd indices can ever be changed.

So strategy: enumerate all distinct rotations reachable via repeated right-rotations by b. For each rotation, try all 10 possibilities of adding to odd indices (0..9 times). If b is odd, for each of those results also try all 10 possibilities of adding to even indices. Track the lexicographically smallest string found.

This yields a manageable search: at most n rotations, and for each rotation at most 100 (10*10) add combinations, with O(n) cost to build strings — fine for n <= 100.

## Refining the problem, round 2 thoughts
Edge cases:
- b might equal n/2 etc. But rotation cycle detection handles that.
- If a % 10 == 0 then addition does nothing; handled by loops (they'll produce identical strings).
- When b is even we should not try adding to even indices — no sequence yields that.
- We can short-circuit some repetition, but the loops are small constants (10) so no need.

Complexity:
- Let n = len(s). Number of distinct rotations <= n.
- For each rotation we do up to 10 (odd) * 10 (even if b odd) string constructions, each O(n). So worst-case time O(n * 100 * n) = O(100 n^2) -> fine for n <= 100.
- Space: O(n) for building strings and O(n) for storing rotations set.

## Attempted solution(s)
```python
class Solution:
    def findLexSmallestString(self, s: str, a: int, b: int) -> str:
        n = len(s)
        # generate all distinct rotations reachable by repeatedly rotating right by b
        rotations = []
        seen = set()
        cur = s
        while cur not in seen:
            seen.add(cur)
            rotations.append(cur)
            cur = cur[-b:] + cur[:-b]

        def add_to_parity(base: str, times: int, parity: int) -> str:
            # add (times * a) mod 10 to positions with index parity (0 for even, 1 for odd)
            inc = (times * a) % 10
            if inc == 0:
                return base
            lst = list(base)
            for i in range(parity, n, 2):
                lst[i] = str((int(lst[i]) + inc) % 10)
            return ''.join(lst)

        best = s
        for rot in rotations:
            # try all 10 possibilities of adding to odd indices
            for t_odd in range(10):
                s1 = add_to_parity(rot, t_odd, 1)
                if b % 2 == 1:
                    # if b is odd, even indices can be affected via rotations, so try 0..9 adds to even indices
                    for t_even in range(10):
                        s2 = add_to_parity(s1, t_even, 0)
                        if s2 < best:
                            best = s2
                else:
                    # parity preserved: only odd indices can change
                    if s1 < best:
                        best = s1
        return best
```

- Notes on approach: enumerate all reachable rotations; for each, try additive offsets on odd indices (10 possibilities). If b is odd, also try additive offsets on even indices (10 possibilities) because rotations mix parity and allow changes there. Keep lexicographically smallest result.
- Time complexity: O(n * 100 * n) = O(100 n^2) worst-case (n = len(s)), practical given n <= 100.
- Space complexity: O(n) extra (strings/lists and sets for rotations).