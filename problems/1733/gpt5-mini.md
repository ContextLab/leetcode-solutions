# [Problem 1733: Minimum Number of People to Teach](https://leetcode.com/problems/minimum-number-of-people-to-teach/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to pick a single language to teach to some users so every friendship pair can communicate. Two users can already communicate if they share any known language. So the only problematic friend pairs are those where the intersection of their language sets is empty. We only need to teach users involved in such problematic pairs.

A naive idea: for each language L (1..n), compute how many users (among those in problematic pairs) do not already know L — that's how many we'd teach if we chose L. Answer is min over languages. Need to correct for duplicate counting — teach distinct users (not pairs), so consider unique users in problematic pairs.

This suggests:
1. Build sets for languages each user knows.
2. Find all friendships where intersection is empty -> collect both users into a set bad_users.
3. For each language L, count bad_users who don't know L; pick minimum.

We can speed counting by computing for each language how many bad users already know it, then answer = |bad_users| - max_known_count.

## Refining the problem, round 2 thoughts
Edge cases:
- If there are no problematic friendships (all pairs share a language), answer is 0.
- Input uses 1-based user indices in friendships; convert to 0-based for Python lists.
- languages[i] can contain duplicates? Problem states it contains unique values. Still convert to set for membership tests.
- Complexity: m and n are up to 500, friendships up to 500 — O(n * m) or O(m * average languages) is fine. Using the language-count trick reduces repeated work.

Time complexity:
- Building sets: O(m * L_avg)
- Finding problematic pairs: O(f * L_check) but using set isdisjoint makes this efficient (amortized O(min(len(set1),len(set2)))).
- Counting known languages among bad users: O(|bad_users| * L_avg)
Overall O(m * L_avg + f * small + |bad_users| * L_avg) which is well within constraints.

Space complexity:
- O(m * L_avg) to hold sets and O(n) for language counts.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def minimumTeachings(self, n: int, languages: List[List[int]], friendships: List[List[int]]) -> int:
        # Convert each user's languages to a set for fast lookup
        lang_sets = [set(l) for l in languages]
        
        # Collect users involved in friendships who cannot currently communicate
        bad_users = set()
        for u, v in friendships:
            u -= 1  # convert to 0-based index
            v -= 1
            # if they share no language, they are a problematic pair
            if lang_sets[u].isdisjoint(lang_sets[v]):
                bad_users.add(u)
                bad_users.add(v)
        
        # If no problematic friendships, no one needs to be taught
        if not bad_users:
            return 0
        
        # Count for each language how many bad_users already know it
        known_count = [0] * (n + 1)  # languages numbered 1..n
        for user in bad_users:
            for lang in lang_sets[user]:
                known_count[lang] += 1
        
        # To minimize teaching, pick language with maximum known_count among bad_users
        max_known = max(known_count[1:])  # ignore index 0
        # need to teach remaining bad_users who don't know that language
        return len(bad_users) - max_known
```
- Notes:
  - Approach: Identify users in friendships that cannot communicate. For each candidate language, find how many of those users already know it; teach the rest. Choose the language that minimizes teachings.
  - Time complexity: O(m * L_avg + f * small + |bad_users| * L_avg) ≈ O(m * L_avg + f), where m = number of users, f = number of friendships, L_avg = average languages per user. Given constraints (<=500), this is efficient.
  - Space complexity: O(m * L_avg) for language sets and O(n) for language counts.