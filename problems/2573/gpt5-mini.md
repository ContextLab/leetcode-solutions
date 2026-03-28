# [Problem 2573: Find the String with LCP](https://leetcode.com/problems/find-the-string-with-lcp/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are given an n x n LCP matrix describing pairwise longest common prefixes between suffixes word[i:] and word[j:]. The matrix imposes equalities between characters: if lcp[i][j] > 0 then word[i] == word[j]; more generally if lcp[i][j] >= k then word[i+k-1] == word[j+k-1]. Also if lcp[i][j] = L and both i+L and j+L are valid indices, then word[i+L] != word[j+L]. So constraints are "must-equal" (connect indices into components) and "must-differ" (edges between components). We must find the lexicographically smallest lowercase string satisfying them or return "" if impossible.

A straightforward approach is:
- Validate obvious properties of lcp (diagonal and symmetry and bounds).
- Use DSU to union indices that must be equal (union i and j whenever lcp[i][j] > 0 — note we don't need to union every shifted pair explicitly because those shifted pairs will appear as (i+1, j+1) etc in the matrix).
- Build "must-differ" constraints between DSU components using the lcp values (for lcp[i][j] = L, if i+L<n and j+L<n then comp(i+L) != comp(j+L)).
- Assign letters to components in the order of appearance (i from 0..n-1) picking the smallest available letter not used by already-assigned neighbors to keep the string lexicographically smallest.
- Finally compute the LCP matrix from the constructed string using DP (dp[i][j] = 1 + dp[i+1][j+1] if s[i]==s[j] else 0) and compare to the given lcp. If match, return the string, else "".

This gives an overall O(n^2) algorithm (dominated by scanning lcp and validating via DP), which is fine for n ≤ 1000.

## Refining the problem, round 2 thoughts
Edge cases/consistency checks to handle early:
- lcp[i][i] must equal n - i for all i (suffix compared to itself).
- lcp must be symmetric and values cannot exceed n - max(i, j).
- When building "must-differ" edges, if two indices that must differ end up in the same DSU component, it's impossible.
- When assigning letters, we have only 26 lowercase letters; if a component needs a 27th distinct letter (due to constraints), that's impossible and we return "".
- After producing the candidate string, we must validate it by recomputing the lcp via DP. This both checks all constraints and catches subtle inconsistencies not caught before.

This approach avoids the naive O(n^3) unioning across every shifted index by relying on the fact that lcp entries themselves cover the shifted equalities (the pair (i+1, j+1) will be present and unioned if needed).

Now implement.

## Attempted solution(s)
```python
# Python 3 solution

class DSU:
    def __init__(self, n):
        self.p = list(range(n))
        self.r = [0]*n
    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x
    def union(self, a, b):
        ra = self.find(a); rb = self.find(b)
        if ra == rb:
            return False
        if self.r[ra] < self.r[rb]:
            self.p[ra] = rb
        elif self.r[rb] < self.r[ra]:
            self.p[rb] = ra
        else:
            self.p[rb] = ra
            self.r[ra] += 1
        return True

class Solution:
    def findTheString(self, lcp):
        n = len(lcp)
        # Basic validation: diagonal and symmetry and bounds
        for i in range(n):
            if lcp[i][i] != n - i:
                return ""
        for i in range(n):
            for j in range(n):
                if lcp[i][j] != lcp[j][i]:
                    return ""
                if lcp[i][j] > n - max(i, j):
                    return ""
                if lcp[i][j] < 0:
                    return ""
        # Build DSU: if lcp[i][j] > 0 then s[i] == s[j]
        dsu = DSU(n)
        for i in range(n):
            for j in range(n):
                if lcp[i][j] > 0:
                    dsu.union(i, j)
        # Build "must-differ" edges between components
        comp_index = {}
        for i in range(n):
            comp_index[dsu.find(i)] = True
        # Map components to 0..m-1
        comp_list = list(comp_index.keys())
        comp_id = {c: idx for idx, c in enumerate(comp_list)}
        m = len(comp_list)
        neigh = [set() for _ in range(m)]
        for i in range(n):
            for j in range(n):
                L = lcp[i][j]
                pi = i + L
                pj = j + L
                if pi < n and pj < n:
                    ci = comp_id[dsu.find(pi)]
                    cj = comp_id[dsu.find(pj)]
                    if ci == cj:
                        # they must differ but are same component -> impossible
                        return ""
                    neigh[ci].add(cj)
                    neigh[cj].add(ci)
        # Assign letters to components in order of first occurrence in string to ensure lexicographic minimality
        comp_of_pos = [comp_id[dsu.find(i)] for i in range(n)]
        assigned = [-1] * m  # store int 0..25 for 'a'..'z' or -1 if unassigned
        for i in range(n):
            c = comp_of_pos[i]
            if assigned[c] != -1:
                continue
            # gather forbidden letters from already assigned neighbors
            forbidden = [False]*26
            for nb in neigh[c]:
                if assigned[nb] != -1:
                    forbidden[assigned[nb]] = True
            # choose smallest available letter
            letter = -1
            for k in range(26):
                if not forbidden[k]:
                    letter = k
                    break
            if letter == -1:
                return ""  # more than 26 distinct required in conflicting neighbors
            assigned[c] = letter
        # Build string
        s_chars = []
        for i in range(n):
            s_chars.append(chr(ord('a') + assigned[comp_of_pos[i]]))
        s = "".join(s_chars)
        # Validate by recomputing lcp via DP O(n^2)
        dp = [[0]*n for _ in range(n)]
        for i in range(n-1, -1, -1):
            for j in range(n-1, -1, -1):
                if s[i] == s[j]:
                    if i+1 < n and j+1 < n:
                        dp[i][j] = 1 + dp[i+1][j+1]
                    else:
                        dp[i][j] = 1
                else:
                    dp[i][j] = 0
        # compare dp with given lcp
        for i in range(n):
            for j in range(n):
                if dp[i][j] != lcp[i][j]:
                    return ""
        return s

# For LeetCode usage:
# sol = Solution()
# print(sol.findTheString([[4,0,2,0],[0,3,0,1],[2,0,2,0],[0,1,0,1]]))  # should output "abab"
```

- Notes about approach:
  - Union indices i and j whenever lcp[i][j] > 0 to capture "first character equal" equalities. The shifted equalities are covered because the matrix contains entries for shifted pairs too (e.g., (i+1, j+1)).
  - Create "must-differ" edges from lcp[i][j] = L by connecting components of i+L and j+L (if those indices exist). If those two indices are in the same component, contradiction: return "".
  - Assign letters greedily in order of first position appearance to achieve lexicographically smallest string. For each component pick the smallest letter not used by already-assigned neighbors.
  - Finally compute the LCP matrix from constructed string using DP and compare; if mismatch, return "".
- Complexity:
  - Time: O(n^2) to validate and process the lcp matrix and to compute/compare the DP LCP (DSU operations add near-constant overhead). n ≤ 1000 fits.
  - Space: O(n^2) only for the input and the DP validation; DSU and adjacency take O(n) and O(m^2) in worst-case but in our adjacency we store edges only implied by lcp, which is at most O(n^2) entries in practice; overall dominated by O(n^2).