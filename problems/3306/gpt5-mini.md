# [Problem 3306: Count of Substrings Containing Every Vowel and K Consonants II](https://leetcode.com/problems/count-of-substrings-containing-every-vowel-and-k-consonants-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need substrings that include all five vowels at least once and contain exactly k consonants. Exactly-k-consonants constraints suggest either enumerating windows that contain exactly k consonants (using consonant indices), or converting "exactly k" into a difference of two "at most" counts: exactly k = at most k - at most (k-1). The latter often simplifies two-pointer approaches because "at most t consonants" is monotonic when expanding the right pointer.

We also need the substring to contain all five vowels — also a monotonic property when expanding right. So we can maintain two sliding-window processes for "at most t consonants" and "at most (t-1) consonants" simultaneously (or run the same routine twice) to compute counts of substrings that contain all vowels and have at most t consonants. Answer = count(at_most_k) - count(at_most_k-1).

We must be careful to implement the sliding windows efficiently: for each left index L, we want the minimal R_v (>= L) such that [L..R_v] contains all vowels, and the maximal R_max (>= L) such that [L..R_max] has at most t consonants. If R_v exists and R_max >= R_v, then number of valid substrings starting at L is R_max - R_v + 1. Maintain two separate windows (counts) with two right pointers R_v and R_max; both move only forward across L iterations — overall O(n).

## Refining the problem, round 2 thoughts
- Convert "exactly k consonants" into f(k) - f(k-1), where f(t) counts substrings that contain all vowels and have at most t consonants.
- Implement f(t) with two pointers and two tracked windows:
  - Rv: smallest right index where vowel coverage is satisfied (we expand until all 5 vowels present).
  - Rmax: largest right index that keeps consonant count <= t (we expand while adding the next char would not exceed t consonants).
- For each L, after advancing both Rv and Rmax (they don't move backward), if vowels are covered (Rv valid) and Rmax >= Rv then add Rmax - Rv + 1 to result.
- Maintain per-window vowel frequencies and consonant counts; when L increases, remove s[L] from both windows if they include it.
- Edge case: k = 0 => compute f(0) - f(-1) with f(-1) = 0.
- Complexity: O(n) time (each right pointer moves at most n steps), O(1) extra space (constant-sized vowel counters).

## Attempted solution(s)
```python
class Solution:
    def countVowelConsonantSubstrings(self, word: str, k: int) -> int:
        # Wrapper to match LeetCode problem name if required externally.
        return self.countSubstrings(word, k)

    def countSubstrings(self, word: str, k: int) -> int:
        def is_vowel(ch: str) -> bool:
            return ch in vowel_set

        def count_at_most(t: int) -> int:
            # If t < 0, no substring can have <= t consonants.
            if t < 0:
                return 0

            n = len(word)
            # Two right pointers:
            Rv = -1    # minimal right to satisfy vowels for current L
            Rmax = -1  # maximal right to satisfy <= t consonants for current L

            # vowel counts and consonant counts for each of the two windows
            vc_v = [0] * 5   # for window [L..Rv]
            vc_m = [0] * 5   # for window [L..Rmax]
            have_v = 0       # number of vowel types present in [L..Rv]
            have_m = 0       # number of vowel types present in [L..Rmax]
            cons_v = 0       # consonant count in [L..Rv]
            cons_m = 0       # consonant count in [L..Rmax]

            ans = 0
            for L in range(n):
                # Expand Rv until vowel coverage satisfied (or end)
                while Rv + 1 < n and have_v < 5:
                    Rv += 1
                    c = word[Rv]
                    if is_vowel(c):
                        idx = vowel_index[c]
                        vc_v[idx] += 1
                        if vc_v[idx] == 1:
                            have_v += 1
                    else:
                        cons_v += 1
                    # no constraint on cons_v here; Rv can go beyond t, Rmax will limit final count

                # Expand Rmax while we can keep consonant count <= t
                while Rmax + 1 < n:
                    nxt = word[Rmax + 1]
                    if is_vowel(nxt):
                        Rmax += 1
                        idx = vowel_index[nxt]
                        vc_m[idx] += 1
                        if vc_m[idx] == 1:
                            have_m += 1
                    else:
                        # next is consonant: check if adding it would exceed t
                        if cons_m + 1 <= t:
                            cons_m += 1
                            Rmax += 1
                        else:
                            break

                # If vowel coverage exists and Rmax >= Rv, we have (Rmax - Rv + 1) valid substrings starting at L
                if have_v == 5 and Rmax >= Rv:
                    ans += (Rmax - Rv + 1)

                # Move left bound forward: remove word[L] from both windows if included
                if L <= Rv:
                    ch = word[L]
                    if is_vowel(ch):
                        idx = vowel_index[ch]
                        vc_v[idx] -= 1
                        if vc_v[idx] == 0:
                            have_v -= 1
                    else:
                        cons_v -= 1
                # else Rv < L: nothing to remove for Rv window

                if L <= Rmax:
                    ch = word[L]
                    if is_vowel(ch):
                        idx = vowel_index[ch]
                        vc_m[idx] -= 1
                        if vc_m[idx] == 0:
                            have_m -= 1
                    else:
                        cons_m -= 1
                # else Rmax < L: nothing to remove for Rmax window

                # Note: we do NOT move Rv or Rmax left; they only advance.
            return ans

        vowel_set = set('aeiou')
        vowel_index = {'a':0, 'e':1, 'i':2, 'o':3, 'u':4}

        # answer is f(k) - f(k-1)
        return count_at_most(k) - count_at_most(k - 1)


# Example usage:
# sol = Solution()
# print(sol.countSubstrings("aeiou", 0))  # -> 1
# print(sol.countSubstrings("aeioqq", 1)) # -> 0
# print(sol.countSubstrings("ieaouqqieaouqq", 1)) # -> 3
```

- Notes on approach:
  - I compute f(t) = number of substrings that contain all five vowels and have at most t consonants using two monotonic right pointers per left index.
  - The answer for exactly k consonants equals f(k) - f(k-1).
  - Each right pointer (Rv and Rmax) only moves forward overall, and each left iteration does O(1) work (updates and checks). Thus the algorithm runs in linear time.

- Complexity:
  - Time: O(n), where n = len(word). Each of the two right pointers advances at most n steps, and the left pointer runs n iterations; per step we do constant-time updates (vowel map of size 5).
  - Space: O(1) extra space (constant arrays / counters for five vowels and a few integers), aside from the input string.

This solution is efficient and handles k = 0 correctly (by subtracting f(-1) = 0).