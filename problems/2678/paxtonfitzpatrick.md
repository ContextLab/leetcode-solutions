# [Problem 2678: Number of Senior Citizens](https://leetcode.com/problems/number-of-senior-citizens/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- yay, finally an easy one for a change. This is just a one-liner summing a generator expression that filters based on the age characters in the string.

## Refining the problem, round 2 thoughts

- little hacky optimization: since the ages are always 2 characters long, we know they must always be between `1` and `99`, and 1-digit ages must have leading zeros. This means we can just compare the age strings to `"60"` instead of converting them to ints and comparing them to `60`, because Python compares sequences by their lexicographical ordering -- in the case of string, using each character's unicode code point.
- this could reduce the runtime by *hundreds* of nanoseconds!!! 🏃‍♂️💨

## Attempted solution(s)

```python
class Solution:
    def countSeniors(self, details: List[str]) -> int:
        return sum(d[11:13] > '60' for d in details)

```

![](https://github.com/user-attachments/assets/ce9815a7-4ed1-421f-96ca-84bf07571bd6)
