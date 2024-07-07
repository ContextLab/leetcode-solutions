# [Problem 1550: Three Consecutive Odds](https://leetcode.com/problems/three-consecutive-odds/description/)

## Initial thoughts (stream-of-consciousness)

- seems like a pretty easy one
- need to track the number of consecutive odds
  - if counter ever reaches 3, return True
  - if we encounter an even number, reset counter to 0

## Refining the problem

- I bet this will ultimately be slower, but I can think of a kinda fun, roundabout way solve this:
  - convert `arr` to a string
  - use regular expression to search for 3 consecutive occurrences of values that end in 1, 3, 5, 7, or 9, separated by a command and space
    - we know that all values are <= 1000, and 1000 is an even number, so all odd numbers will have 1, 2, or 3 digits -- so for each number we need to match 0, 1, or 2 digits of any value, followed by an odd digit: `[0-9]{0,2}[13579]`
    - base pattern would be `(?:[0-9]{0,2}[13579], ){3}` but:
      - this would fail for the last 3 values in the list because there's no trailing comma. So instead use `(?:[0-9]{0,2}[13579], ){2}[0-9]{0,2}[13579]`
      - Also for the first of the 3 odd numbers, we should only try to match the final digit rather than all digits, otherwise the search will be slower because the pattern will initially match all values in the list and waste a bunch of time backtracking. So instead use `[13579], [0-9]{0,2}[13579], [0-9]{0,2}[13579]` or `[13579](?:, [0-9]{0,2}[13579]){2}`

  - `re.search` returns a `Match` object as soon as it encounters the first match, and `None` if no match is found. So we should be able to just `bool()` the result and return it.
  - I wonder if compiling the pattern upfront would be faster than using using the module-level functions... depends on how leetcode runs the test cases, I guess. If I compile the expression in the class body outside the method definition, and all test case runs reuse the same instance of the class, then it should save time. Otherwise, it probably wouldn't. Maybe I'll just compile it in the global namespace and see.

## Attempted solution(s)

```python
class Solution:
    def threeConsecutiveOdds(self, arr: List[int]) -> bool:
        if len(arr) < 3:
            return False

        consec_odds = 0
        for val in arr:
            if val % 2:
                if consec_odds == 2:
                    return True
                consec_odds += 1
            else:
                consec_odds = 0
        return False
```

![](https://github.com/paxtonfitzpatrick/leetcode-solutions/assets/26118297/c45d108c-b23b-48d8-bc14-13a2cdc0cc06)

```python
from re import compile

pattern = compile(r"[13579](?:, [0-9]{0,2}[13579]){2}")

class Solution:
    def threeConsecutiveOdds(self, arr: List[int]) -> bool:
        return bool(pattern.search(str(arr)))
```

![](https://github.com/paxtonfitzpatrick/leetcode-solutions/assets/26118297/88d07bb2-f252-4797-81e4-33793acaeae4)
