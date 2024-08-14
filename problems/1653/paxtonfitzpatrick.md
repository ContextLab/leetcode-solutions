# [Problem 1653: Minimum Deletions to Make String Balanced](https://leetcode.com/problems/minimum-deletions-to-make-string-balanced/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- okay I don't see an immediately obvious solution to this one
- one initial idea I have is that the closer to the "wrong" end of the string a character is (i.e., closer to the front for b's and the back for a's), the more confident we are that we'll want to delete it. So maybe I could do something like:
  - initialize 2 indices into the string: `i = 0` and `j = len(s) - 1`, and a counter `n_deletions = 0`
  - `while s[i] == 'a'`, consume a character from the front of the string and incrememnt `i` by 1
  - `if s[i+1] == 'b'`, switch to consuming characters from the back of the string and decrementing `j` by 1
  - `if s[j-1] == 'a'`, switch back to the front of the string, consume the `'b'` we stopped at before, increment `n_deletions` by 1, continue consuming `'a'`s, and so on...
  - stop when `i + 1 == j` or `j - 1 == i` and return `n_deletions`
  - I'm not sure this will work though... I think I'll try playing this out with the two examples and see what happens:
    - Example 1:
      - `s = "aababbab"`; `i = 0`; `j = 7`; `n_deletions = 0`
      - consume `s[0]`
      - consume `s[1]`
        - `s[2]` would be a `"b"` so switch to consuming from the right
      - consume `s[7]`
        - `s[6]` would be an `"a"` so switch back to consuming from the left
      - consume `s[2]` and update `n_deletions` to 1
      - consume `s[3]`
        - `s[4]` would be a `"b"` so switch to consuming from the right
      - consume `s[6]` and update `n_deletions` to 2
      - consume `s[5]`
      - consume `s[4]`
      - `i == 3`, so instead of consuming `s[3]`, `return n_deletions`
    - Example 2:
      - `s = "bbaaaaabb"`; `i = 0`; `j = 8`; `n_deletions = 0`
        - `s[0]` would be a `"b"` so switch to right
      - consume `s[8]`
      - consume `s[7]`
        - `s[6]` would be an `"a"` so switch to left
      - consume `s[0]` and update `n_deletions` to 1
        - `s[1]` would be an `"b"` so switch to right
      - consume `s[6]` and update `n_deletions` to 2
        - `s[5]` would be an `"a"` so switch to left
      - consume `s[1]` and update `n_deletions` to 3
      - ...
  - Okay so it worked for the first example but not the second. I thought that might happen, because this approach assumes there are both a's in the "b section" and b's in the "a section" of the string, which isn't necessarily true. I think I could tweak the rules I used for consuming characters/"looking ahead" to make this work for the 2nd example, but I don't think it'll work in the general case.
- So that approach didn't work because it assumed there was a 1:1 relationship between a's to be removed from the back and b's to be removed from the front. But the minimum number of deletions can involve all a's, all b's, or some uneven combination of them. So what if instead, I iterate through the string and, for each index, count the number of a's to the right and b's to the left (which are what would have to be removed), and then just return the min of those counts?
  - This seems promising, but I'd have to figure out how to do it efficiently... the simplest approach would involve something like, e.g., for each index `i`, doing `sum(1 for i in range(i) if s[i] == 'b') + sum(1 for i in range(i+1, len(s)) if s[i] == 'a')`. But that'd take $O(n^2)$ time...
  - Ah -- I could figure out the number of b's to the left of each index in $O(n)$ time by looping through the string and tracking the cumulative count of b's, and storing that in some list. And then since every letter in the string is either an a or a b, for each index `i`, the number of a's to the left of it would be `i - n_left_bs`. Then once I get to the end of the string I'll know the total number b's and therefore the total number of a's, so the number of a's to the right of each index would be the total number of a's minus the number of a's to the left of each index.
    - ... or I could just use `str.count()` instead 🤦 duh. Either that or looping through the list of cumulative b-counts to figure out the a-counts for each index would take $O(n)$ time, but `str.count()` is a C function so it'll be much faster than a Python loop. In fact it might end up being faster than the math logic I'd do at each iteration. Maybe I'll try both ways.
    - In fact, I don't even think I'd have to store the cumulative count(s) in a list; I could just track a running minimum with a variable. That's reduce the space complexity from $O(n)$ to $O(1)$.
    - should the current index be included in the count of a's/b's to the left or right? I don't think it matters.
  - I can't think of any edge cases that would potentially trip me up here... I think the only thing worth doing is checking whether the string is all a's or all b's, in which case I can just return 0.

## Refining the problem, round 2 thoughts

## Attempted solution(s)

```python
class Solution:
    def minimumDeletions(self, s: str) -> int:
        total_as = s.count('a')
        if total_as == 0 or total_as == len(s):
            return 0

        n_bs_left = 0
        min_deletions = len(s)
        for i in range(len(s)):
            if s[i] == 'b':
                n_bs_left += 1
            # n_as_left = i + 1 - n_bs_left
            # n_as_right = total_as - n_as_left
            # n_deletions = n_bs_left + n_as_right
            # simplified equivalent:
            n_deletions = 2 * n_bs_left + total_as - i - 1
            if n_deletions < min_deletions:
                min_deletions = n_deletions

        return min_deletions
```

![](https://github.com/user-attachments/assets/44cace17-7991-4f81-8ca2-e04bbad1bd0b)

That's weird... I wonder what hapened there. I don't think there's something fundamental wrong with the logic of my solution itself if it passed 155/157 test cases, but I'll try to figure out what's unique about this one.

Ah -- since I treat the "current" character as one of the characters "to the left" of the current position, I never consider the case where all characters are on the right and none are on the left. And because of that, I miss instances where the minimum deletion is deleting all a's.

I can fix this pretty easily by just returning the minimum of the `min_distance` my approach identifies and the `total_as` in the string.

```python
class Solution:
    def minimumDeletions(self, s: str) -> int:
        total_as = s.count('a')
        if total_as == 0 or total_as == len(s):
            return 0

        n_bs_left = 0
        min_deletions = len(s)
        for i in range(len(s)):
            if s[i] == 'b':
                n_bs_left += 1
            if 2 * n_bs_left + total_as - i - 1 < min_deletions:
                min_deletions = 2 * n_bs_left + total_as - i - 1

        if min_deletions < total_as:
            return min_deletions
        return total_as
```

![](https://github.com/user-attachments/assets/cb112e59-24fe-4245-976f-35c1747d32cd)
