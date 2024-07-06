# [Problem 2582: Pass the Pillow](https://leetcode.com/problems/pass-the-pillow)

## Initial thoughts (stream-of-consciousness)

- seems pretty straightforward
- definitely going to be using modulo operator
  - both for figuring out how many people from one end or the other who has the pillow and figuring out whether the current direction is forwards or backwards
- actually, it's probably not optimal, but `itertools.cycle` could do this pretty easily
  - let's try that approach first as a baseline
  - trick here is to start with an iterable of `n` elements, but then extend it with items at indices `n-2` backwards through `1` so we don't repeat the first and last elements
  - I think I can use `itertools.chain` to extend the iterable with a reversed partial copy like this without ever actually constructing it in memory.
  - Also, `n` and/or `time` are really large, it might be better to use `itertools.islice` rather than acutally running the loop `time` times...

## Refining the problem

- Let's try the non-`itertools` way now.
  - first figure out how many people from one end or the other the pillow will be at time `time`
  - then figure out whether we're currently going in the forward or backward direction

## Attempted solution(s)

```python
from itertools import chain, cycle, islice

class Solution:
    def passThePillow(self, n: int, time: int) -> int:
        return next(islice(cycle(chain(range(1, n + 1), reversed(range(2, n)))), time, None))
```

![](https://github.com/paxtonfitzpatrick/leetcode-solutions/assets/26118297/07156d7a-fa66-49a7-b6fb-389acaf66907)

```python
class Solution:
    def passThePillow(self, n: int, time: int) -> int:
        offset = time % (n - 1)
        return (n - offset) if time // (n - 1) % 2 else (offset + 1)
```

![](https://github.com/paxtonfitzpatrick/leetcode-solutions/assets/26118297/a96a6dc1-0852-4d3b-8c60-d1c997aea142)
