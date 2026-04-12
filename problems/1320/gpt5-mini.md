# [Problem 1320: Minimum Distance to Type a Word Using Two Fingers](https://leetcode.com/problems/minimum-distance-to-type-a-word-using-two-fingers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I can’t share internal stream-of-consciousness, but here is a concise summary of the approach instead:

- We want the minimum total Manhattan distance to type the given word using two fingers, where initial finger positions are free (no cost).
- Model the state by the positions of the two fingers (including a special "not placed yet" state). For each next letter, we choose which finger to move to that letter and add the movement cost (0 if that finger was "not placed" yet).
- Use dynamic programming over the sequence of letters, keeping a DP table for all possible pairs of finger positions. This leads to an efficient solution with manageable state size.

## Refining the problem, round 2 thoughts
- Represent letters A..Z as indices 0..25 with coordinates (r = idx // 6, c = idx % 6). Use index 26 as the "not placed" sentinel.
- dp[i][j] = minimum cost after typing some prefix where finger1 is at i and finger2 is at j. Initialize dp[26][26] = 0.
- For each next character k (index cur), build a new dp' by moving finger1 to cur (cost = dist(i, cur) unless i == 26 => 0) or moving finger2 to cur similarly.
- After processing all characters, answer = min(dp[i][j]) over all i,j.
- Complexity: O(n * 27 * 27) time (n = len(word)), O(27 * 27) space — easily fits given constraints (n <= 300).

## Attempted solution(s)
```python
class Solution:
    def minimumDistance(self, word: str) -> int:
        # Map letter index to (r, c) on the keyboard
        def coord(idx):
            return (idx // 6, idx % 6)
        
        def dist(a, b):
            # a or b can be 26 which means "not placed yet" -> zero cost to place from there
            if a == 26 or b == 26:
                return 0
            ra, ca = coord(a)
            rb, cb = coord(b)
            return abs(ra - rb) + abs(ca - cb)
        
        n = len(word)
        if n == 0:
            return 0
        
        # Convert word to indices 0..25
        arr = [ord(c) - ord('A') for c in word]
        
        # Use 26 as "not placed yet"
        SENTINEL = 26
        SIZE = 27  # 0..25 letters + 26 sentinel
        
        INF = 10**9
        # dp[i][j] = min cost where finger1 at i and finger2 at j
        dp = [[INF] * SIZE for _ in range(SIZE)]
        dp[SENTINEL][SENTINEL] = 0
        
        for cur in arr:
            newdp = [[INF] * SIZE for _ in range(SIZE)]
            for i in range(SIZE):
                for j in range(SIZE):
                    if dp[i][j] == INF:
                        continue
                    base = dp[i][j]
                    # Move finger1 to cur
                    cost1 = base + dist(i, cur)
                    if cost1 < newdp[cur][j]:
                        newdp[cur][j] = cost1
                    # Move finger2 to cur
                    cost2 = base + dist(j, cur)
                    if cost2 < newdp[i][cur]:
                        newdp[i][cur] = cost2
            dp = newdp
        
        # Answer is minimum over all finger positions after typing all chars
        ans = INF
        for i in range(SIZE):
            for j in range(SIZE):
                if dp[i][j] < ans:
                    ans = dp[i][j]
        return ans
```
- Notes:
  - The DP state size is small (27x27) so iterating over all pairs for each character is efficient.
  - dist(a, b) returns 0 if either position is the sentinel (unplaced finger), capturing the "initial placement is free" rule.
  - Time complexity: O(n * 27 * 27) = O(n) with a modest constant (n <= 300). Space complexity: O(27 * 27) = O(1) in practice.