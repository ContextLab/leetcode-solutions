# [Problem 1598: Crawler Log Folder](https://leetcode.com/problems/crawler-log-folder/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- looks like another easy one...
- I'll just iterate through the list and keep track of how many steps we currently are from the main folder.
- oh I wonder what Pyhon version leetcode uses. If 3.10+, this is a good use case for structural pattern matching
  - cool, [looks like it's 3.11](https://support.leetcode.com/hc/en-us/articles/360011833974-What-are-the-environments-for-the-programming-languages)
    - huh, some other useful info from that page: "most" standard library modules are already imported, and also you can `import sortedcontainers`, which is 3rd party
    - no idea how the execution speed of `match`/`case` statements compares to that of standard `if`/`elif`/`else`. My guess would be any difference is minimal, but if anything it might be a little faster since it's a more specific "case" of a conditional, so the instructions it's compiled to might be more specific? OTOH it's a newer feature so it might not be as optimized.
- I *could* pre-filter the list and remove all `"./"`'s, since they do nothing, but I doubt this would actually be faster since it'd essentially entail looping through twice
  - unless I converted the whole list object to a string, used `.replace()`, and converted the result back to a list. Maybe this would ultimately save some time if the list was very long *and* contained a sufficiently large number of `"./"`'s... but I think it's probably not worth it in the general case.

## Refining the problem, round 2 thoughts

## Attempted solution(s)

```python
class Solution:
    def minOperations(self, logs: List[str]) -> int:
        steps_away = 0
        for log in logs:
            match log:
                case "../":
                    if steps_away > 0:
                        steps_away -= 1
                case "./":
                    continue
                case _:
                    steps_away += 1
        return steps_away
```

![](https://github.com/paxtonfitzpatrick/leetcode-solutions/assets/26118297/40647d9b-543e-47f9-b97b-a6f182c0140d)
