# [Problem 1653: Minimum Deletions to Make String Balanced](https://leetcode.com/problems/minimum-deletions-to-make-string-balanced/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- This doesn't seem so bad-- I think we can solve it in $O(n)$ time (where $n$ is the length of the string)
- Let's keep track of the number of `b`s strictly to the left of index `i`, and the number of `a`s strictly to the right of index `i`.  We can fill these in iteratively (the `b`s are filled in using a forward pass through `s` and the `a`s are filled in using a backward pass).
- Then we can initialize the number of moves to `float('inf')`.  Now, loop through each index (`i`) in `s` again, and see if `left_bs[i] + right_as[i] < min_moves`.

## Refining the problem, round 2 thoughts
- Let's just go with this...I can't think of any edge cases that will affect how we solve this

## Attempted solution(s)
```python
class Solution:
    def minimumDeletions(self, s: str) -> int:
        left_bs = [0] * len(s)
        right_as = left_bs.copy()

        b_count = int(s[0] == 'b')
        for i in range(1, len(s)):
            left_bs[i] = b_count
            if s[i] == 'b':
                b_count += 1
        
        a_count = int(s[-1] == 'a')
        for i in range(len(s) - 2, -1, -1):
            right_as[i] = a_count
            if s[i] == 'a':
                a_count += 1

        min_moves = float('inf')
        for i in range(len(s)):
            min_moves = min(min_moves, left_bs[i] + right_as[i])

        return min_moves
```
- Given test cases pass
- New test cases (let's just generate random strings of `a`s and `b`s...):
    - `s = "baabbbbbbaaaabaaabbbbaaabbbabaabbaababaaaaabbaabaabbbbabbabaabbaabbbbaaabbaaaaaaaaaabbababbabbaaaaba"`: pass
    - `s = "aaabaabbaabbaabbaababaaabaaabababababaaaaabbababbbabaaaabababbbabbaabbbbaaababaaabbbabbbabbbabbbaabbaaabbbabaabbbaaababbbaaabbaaaabbbaaaaabbabbbbabaaabbaaabababaabaaaabaabbbabbabbbababbaaabaaaabbaabaabaaaaabbbaaaaaaabaababaabbaababaababbabbabbaababbabbabaabbaaaaaaaabbaababbbaababababbabbabbbababbaabbbbbbbbabbbaaaabaaaaaabbaaabbbababaaababaabababaabababbbaaaabbbaabaabbaaaaabbabbbbabbbaaaaaaabaabaabbabbababbababbbbbbaaaaaabbbababbaababbabbaaaabbaabbbbbbbaabbbbaabaaabbaaaabbabbbaababbabbaabbbbaabababbaaaaabbaaaababbabbabbbbaaaabaabbaaaababbbbbabbabbbababbabbbbbbbbaabbabaabbbabbbaabababbbabbbbabbabbaaaaabbabbbbabbabbabaabbaaaaaabbbabbaaabaabaaaababbababaabbaabbababaaabbbbaaaababababbabbaabbbbbabbaababaaabbbaabaaabaabaabbaababbababababaaabaabaaaaabbabbbaaabbabababbababababbbbaababaabbbabaaaaaabaaaabaaaabaaabaabaababbbbbabbbbaaabbbbababaabbbbbaaabababbababaabbbbbbbbabbbabbaabbbabbbabaabbbaabbbbabbbaaaaaaabbaaaabaabbabbbbbbabababbabaabaabaabaaaaabaaabbbbabbabbbbabbaaaabbababbabbbaaabbaabbbbba"`: pass
- Ok, let's submit!

![Screenshot 2024-07-29 at 8 36 08 PM](https://github.com/user-attachments/assets/3087d858-0c58-434a-aab0-e2a0f937b044)

Solved 🥳!
