# [Problem 273: Integer to English Words](https://leetcode.com/problems/integer-to-english-words/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- oh this one looks like fun as well. Interesting that it's labeled hard... on first glance it seems like it'll require a larger-than-usual amount of coding, but nothing particularly complex conceptually
- I think there's gonna be a few different reusable components I'll need:
  - a mapping from digits to their english word when in the ones place (e.g., `{'1': 'One', '2': 'Two', ...}`)
    - this will also give me the word representation of the hundreds place by just adding 'Hundred' after it
  - a mapping from digits to their english words when in the tens place (e.g., `{'2': 'Twenty', '3': 'Thirty', ...}`)
    - note: I'll need to handle the teens separately. While parsing the number, if I run into a 1 in the tens place, I'll use a specific helper function/mapping that consumes both the tens and ones place to get the correct word (e.g., '13' ➡️ 'Thirteen')
    - I think I'll define these mappings on the class so they can be reused across test cases without needing to redefine them
    - another note: it looks like the output is expected to be in title case, so I'll need to remember to set things up that way
  - a helper function that takes a sequence of 3 numbers and uses the mappings above to convert them to their combined english words (e.g., f('123') ➡️ 'One Hundred Twenty Three')
- and then my main function will:
  - convert the input number to a string
  - split it into groups of 3 digits, with the $\lt$ 3-letter group at the beginning if its length isn't divisible by 3
    - I can do both of the above steps using the ',' string format specifier to convert the int to a string with commas, and then splitting it into a list on the commas
  - process each of those groups independently using the helper function above, and add its appropriate "suffix" (e.g., 'Thousand', 'Million', etc.)
    - the constraints say `num` can be at most $2^{31} - 1$, which is 2,147,483,647, so I'll only need to handle up to 'Billion'
  - join the groups together and return the result
- I don't foresee any major issues with this approach, so I'm gonna go ahead and start implementing it

## Refining the problem, round 2 thoughts

- any edge cases to consider?
  - only potential "gotcha" I can think of is that typically 0s should lead to an empty string, or no aded output (e.g., 410000 ➡️ 'Four Hundred Ten Thousand'; 5002 ➡️ 'Five Thousand Two'), except for when the full number itself is 0, in which case the output should be 'Zero'. But I'll just add a check for this at the beginning of the main function
- what would the time and space complexity of this be?
  - I think the only part that scales with the input is looping over the 3-digit groups to process them, so the number of groups I need to process will increase by 1 as `num` increases by a factor of 1,000. I think this would mean both the time and space complexities are $O(\log n)$

## Attempted solution(s)

```python
class Solution:
    ones_mapping = {
        '0': '',
        '1': 'One',
        '2': 'Two',
        '3': 'Three',
        '4': 'Four',
        '5': 'Five',
        '6': 'Six',
        '7': 'Seven',
        '8': 'Eight',
        '9': 'Nine'
    }
    tens_mapping = {
        '2': 'Twenty',
        '3': 'Thirty',
        '4': 'Forty',
        '5': 'Fifty',
        '6': 'Sixty',
        '7': 'Seventy',
        '8': 'Eighty',
        '9': 'Ninety'
    }
    teens_mapping = {
        '10': 'Ten',
        '11': 'Eleven',
        '12': 'Twelve',
        '13': 'Thirteen',
        '14': 'Fourteen',
        '15': 'Fifteen',
        '16': 'Sixteen',
        '17': 'Seventeen',
        '18': 'Eighteen',
        '19': 'Nineteen'
    }
    group_suffixes = ('', ' Thousand', ' Million', ' Billion')

    def numberToWords(self, num: int) -> str:
        if num == 0:
            return 'Zero'
        result = ''
        for digit_group, suffix in zip(
            reversed(f'{num:,}'.split(',')),
            self.group_suffixes
        ):
            if digit_group != '000':
                group_words = self._process_digit_group(digit_group) + suffix
                result = f'{group_words} {result}'
        return result.strip()

    def _process_digit_group(self, digits):
        match len(digits):
            case 1:
                return self.ones_mapping[digits]
            case 2:
                if digits[0] == '1':
                    return self.teens_mapping[digits]
                return (
                    f'{self.tens_mapping[digits[0]]} '
                    f'{self.ones_mapping[digits[1]]}'
                ).rstrip()
        if digits[0] == '0':
            group_words = ''
        else:
            group_words = self.ones_mapping[digits[0]] + ' Hundred'
        match digits[1]:
            case '0':
                return f'{group_words} {self.ones_mapping[digits[2]]}'.strip()
            case '1':
                return f'{group_words} {self.teens_mapping[digits[1:]]}'.lstrip()
        return (
            f'{group_words} {self.tens_mapping[digits[1]]} '
            f'{self.ones_mapping[digits[2]]}'
        ).strip()
```

![](https://github.com/user-attachments/assets/71d3b83a-56de-48a2-8209-f787c0034b4d)
