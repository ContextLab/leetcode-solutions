# [Problem 1358: Number of Substrings Containing All Three Characters](https://leetcode.com/problems/number-of-substrings-containing-all-three-characters/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the number of substrings that contain at least one 'a', one 'b', and one 'c'. Brute force would check all O(n^2) substrings and test counts, which is too slow for n up to 5e4. This smells like a two-pointer / sliding-window problem where we maintain a window that contains all three characters; for each right end we can count how many starting positions produce valid substrings ending at that right.

Specifically: if for a given right index r there is a smallest left index l such that s[l..r] contains all three characters, then any start i with 0 <= i <= l will produce s[i..r] that still contains all three (extending left doesn't remove characters). So the number of valid substrings ending at r is l + 1. We can maintain counts of 'a','b','c' and shrink the window from the left as much as possible while keeping all three.

This should yield an O(n) solution with constant extra space (counts for three chars).

## Refining the problem, round 2 thoughts
Edge cases: if string never contains all three characters at any point, we should return 0. The algorithm naturally handles that because we only add to answer when the window has all three.

Implementation details:
- Use two pointers l, r.
- Use an array or dict for counts of 'a','b','c'.
- For each r from 0..n-1, increment count for s[r]. While counts for all three > 0, move l forward (but we need l to be the smallest index that still keeps all three, so shrink inside a while that checks all counts>0 and stop when one would become 0).
- After shrinking to minimal l (i.e., while counts all > 0 we try to shrink until removing s[l] would break the condition), we add (l + 1) to result (number of possible starts).
  - Careful ordering: increment counts, then while condition true, we try to increment l only while counts remain > 0 after decreasing; a clearer way: after incrementing r, while counts[a]>0 and counts[b]>0 and counts[c]>0: we can try to move l forward by decrementing count[s[l]] and l += 1, but that would make window invalid. So better approach is: while counts all >0, we decrement counts[s[l]] and l += 1 to make window minimal, then after loop we've moved l just past the point where it's invalid, so the minimal valid left is l-1. Simpler and less confusing approach: maintain while counts all > 0: update answer by adding current l+1 then move left? Wait canonical approach is:
    - For each r, increment count[s[r]].
    - While window contains all three, move left forward (decrement counts[s[l]], l += 1) to shrink as much as possible; but we want the minimal l that still keeps all three, so we should stop shrinking when some count becomes zero, meaning the last l that kept it valid was l-1. So better to shrink while all counts > 0, but before decrementing the count we should record something. To avoid confusion, the more common and correct formula: while window contains all three, we can count that for this particular window there are (n - r) substrings starting at current left? No that's different variant where count substrings starting at left. Let's stick to the common consistent method:
    - Use l as minimal left such that window [l..r] contains all three. To maintain minimality, after increasing r and updating counts, while counts of the char at l > 1 (meaning we can remove it and still have all three), decrement counts[s[l]] and l += 1. Now if all counts>0, l is minimal. If some count is 0 then window is invalid and we don't add.
    - But checking counts[s[l]] > 1 is not sufficient because that only ensures removing the char at l doesn't zero out its category; but other categories might be zero already. Simpler and less error-prone is the widely used technique:
        - Expand r and increment counts.
        - While counts of all three > 0:
            - add (l + 1) to answer (because minimal l currently ensures all three, and all starts from 0..l are valid), then shrink from left by decrementing counts[s[l]] and l += 1.
      This works because each time the window is valid you count substrings ending at r for all start positions up to current l, then you move l forward to possibly count further with a larger l (which will give additional valid starts for same r until window invalid). But note: adding (l + 1) multiple times for same r will overcount — let's revisit canonical known solution: The well-known solution is:
        - For each right, while window valid, increment answer by (n - r) and shrink left (this counts substrings starting at left with any right >= current r). Hmm multiple variants exist.
Let's recall precise correct known solution for this exact problem:
Common accepted method: For each left pointer, find the minimal right pointer such that substring contains all three, then add (n - right) to answer (because any extension to right will also contain all three). That is iterate left, move right forward as needed, then if valid, add n - right. That's equivalent and easier to implement cleanly:
    - r starts at 0.
    - For l in 0..n-1:
        - while r < n and window [l..r] does not contain all three, increment count and r.
        - if window contains all three then add (n - r) to answer because any substring starting at l with end >= r is valid.
        - before moving l to l+1, decrement count of s[l].
This is simpler and avoids tricky double-counting. Time is O(n) because r only moves forward.

I'll implement the left-iterating approach.

Time complexity O(n), space O(1).

## Attempted solution(s)
```python
class Solution:
    def numberOfSubstrings(self, s: str) -> int:
        n = len(s)
        count = {'a': 0, 'b': 0, 'c': 0}
        res = 0
        r = 0

        def has_all():
            return count['a'] > 0 and count['b'] > 0 and count['c'] > 0

        for l in range(n):
            # expand r until window [l..r] (inclusive) contains all three or r == n
            while r < n and not has_all():
                count[s[r]] += 1
                r += 1
            # if window has all three, any end index from r-1 to n-1 works,
            # so there are (n - (r-1)) = n - r + 1 substrings starting at l that are valid.
            # But note r was incremented after adding s[r], so the minimal valid right index is r-1.
            # Therefore number of valid substrings starting at l is n - (r-1) = n - r + 1.
            # We can equivalently add (n - r + 1). If r == n and has_all() is False, skip.
            if has_all():
                res += n - (r - 1)
            # before moving l forward, remove s[l] from the window
            count[s[l]] -= 1

        return res
```
- Notes about approach:
  - This implementation iterates left pointer l from 0..n-1 and advances right pointer r only forward; r never moves left, so total moves of r are O(n). For each l we ensure r is the minimal index > = l such that [l..r] contains all three (r is one past the current right in the code because we increment r after including s[r]).
  - Complexity: Time O(n), Space O(1) (only three counters).
  - Careful detail: r is maintained as an exclusive end index in the loop (we increment r after counting s[r]). When window is valid, the minimal inclusive right index is r-1, so number of valid substrings starting at l is n - (r-1) = n - r + 1. If r == n and still not valid, has_all() is False so we don't add.
  - This is a standard two-pointer sliding window counting technique that avoids nested loops by ensuring both pointers only move forward.