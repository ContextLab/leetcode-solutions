# [Problem 1945: Sum of Digits of String After Convert](https://leetcode.com/problems/sum-of-digits-of-string-after-convert/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- Another easy one 🥳!
- Let's hard code in the lowercase letters (`letters = 'abcdefghijklmnopqrstuvwxyz'`)
- Then we can make a `letter2num` decoder: `letter2num = {c: str(i + 1) for i, c in enumerate(letters)}`
- Next, we just replace each letter with it's number, stitch it into a string, and convert to an integer: `num = int("".join([letter2num[c] for c in s]))`
- Finally, loop through `k` times to sum the digits:
```python
for _ in range(k):
    num = str(sum([int(i) for i in str(num)]))
```
- And then we just return `int(num)`

## Refining the problem, round 2 thoughts
- There are no tricky edge cases, as far as I can tell; `k` is always at least 1, and the strings aren't super long so we don't need to worry about overflow issues
- Let's try it!


## Attempted solution(s)
```python
class Solution:
    def getLucky(self, s: str, k: int) -> int:
        letters = 'abcdefghijklmnopqrstuvwxyz'
        letter2num = {c: str(i + 1) for i, c in enumerate(letters)}

        num = int("".join([letter2num[c] for c in s]))
        for _ in range(k):
            num = str(sum([int(i) for i in str(num)]))

        return int(num)
```
- Given test cases pass
- Let's try some other random ones:
    - `s = "asdlkoifhawioefuh", k = 5`: pass
    - `s = "dkfjkjdfijshdeweskjhaskljdfhjsldkjf", k = 4`: pass
- I think we're good; submitting...

![Screenshot 2024-09-02 at 8 41 31 PM](https://github.com/user-attachments/assets/0a1d3f63-c163-4bfb-a8ec-286ee3b9c0cc)

Solved!
