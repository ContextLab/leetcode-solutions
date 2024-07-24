# [Problem 2191: Sort the Jumbled Numbers](https://leetcode.com/problems/sort-the-jumbled-numbers/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- this seems pretty easy... there was a problem the other day where we had to sort one array based on the sorted values in another array -- I think it was sorting people's names by their heights. The main addition here is finding a way to efficiently apply `mapping` to `nums`.
- I'll convert `nums` to a string, then loop through `mapping` and replace each digit in `nums` with its corresponding index. Then I can use `ast.literal_eval()` to convert the stringified list back to a list, sort it, and return it.
- One sneaky potential "gotcha" is that Python doesn't like converting strings with leading zeros to integers. So I'll need to manually remove those from the stringified list before evaluating it. I think the easiest way will be to split the string on `, ` to get each item, then `.lstrip('0')` from each of those. Also I'll want to remove the leading `[` from the stringified list before splitting it so `.lstrip('0')` handles the first item correctly.
- ah actually, there's one more thing to account for -- items in `nums` can be `0`, so I'll need to remove leading 0s IFF they're followed by a non-zero digit. So I think instead of splitting the stringified list and using `.lstrip('0')`, I'll use a regular expression with `re.sub()` to remove leading zeros. This will involve (1) a positive lookahead assertion to match 0s IFF they're followed by a non-zero digit, and (2) a positive lookbehind assertion to match 0s IFF they're preceded by a space, so I think the pattern will be `(?<= )0+(?=[1-9])`. To deal with the first element in the stringified list potentially having leading 0s, I could make the lookbehind assertion `(?<= \[)`, but I think it'll be faster to just replace the opening bracket with a space and then undo it after the substitution, rather than give the regex engine additional checks to run.

## Refining the problem, round 2 thoughts

- I'm realizing there was a silly error in my initial thinking -- if I loop through `mapping` and replace digits one at a time, I'll end up replacing already-replaced digits in later iterations. So I'll want to use a translation table instead to make multiple simultaneous replacements.

## Attempted solution(s)

### expanded version

```python
from ast import literal_eval
from re import compile


class Solution:
    pattern = compile(r'(?<= )0+(?=[1-9])')

    def sortJumbled(self, mapping: List[int], nums: List[int]) -> List[int]:
        if mapping == list(range(10)):
            return sorted(nums)

        mapped_nums = str(nums)
        trans_table = str.maketrans('0123456789', ''.join(map(str, mapping)))
        mapped_nums = mapped_nums.translate(trans_table)
        mapped_nums = self.pattern.sub('', mapped_nums.replace('[', ' '))
        mapped_nums = literal_eval('[' + mapped_nums[1:])
        mapped_ixs = sorted(range(len(mapped_nums)), key=mapped_nums.__getitem__)
        return [nums[i] for i in mapped_ixs]
```

### condensed, optimized version

```python
from ast import literal_eval
from re import compile


class Solution:
    pattern = compile(r'(?<= )0+(?=[1-9])')

    def sortJumbled(self, mapping: List[int], nums: List[int]) -> List[int]:
        if mapping == [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            yield from sorted(nums)
        else:
            mapped_nums = literal_eval(
                '[' + self.pattern.sub('', str(nums).translate(
                    str.maketrans('0123456789', ''.join(map(str, mapping)))
                ).replace('[', ' '))[1:]
            )
            for i in sorted(range(len(mapped_nums)), key=mapped_nums.__getitem__):
                yield nums[i]
```

![](https://github.com/user-attachments/assets/66825ef9-f9b6-4c70-a12c-61bdb37ba116)

Yikes, pretty poor memory usage on this one... probably because of the regular expression. But I'll stick with it for tonight.
