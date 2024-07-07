# [Problem 1518: Water Bottles](https://leetcode.com/problems/water-bottles)

## Initial thoughts (stream-of-consciousness)

- seems pretty simple...
- when exchanging empties for fulls, will need to use floor division to figure out how many fulls we can get and also modulo to figure out how many empties couldn't be echanged
- also need to keep track of unexchanged empties in case we can accumulate enough for another full (`numExchange`)
- stop when we have no more fulls and not enough empties to exchange for a full
- I think I'll structure this as a `while` loop where each time through the loop we can drink fulls and/or exchange empties
  - There's probably a more efficient way to do this without looping, where we calculate everything from the initial values (so, $O(1)$), but this seems like an easier place to start.
  - I bet there's also a way to set this up recursively, which could be interesting, but unlikely to be optimal

## Refining the problem, round 2 thoughts

- Version 2: I noticed some small tweaks I could make to the logic that I think would speed up the `while` loop version slightly
  - note: key to not having to modify `n_empties` twice each iteration is updating `n_fulls` and `n_empties` simultaneously. New values for both variables depend on the old value of the other, so updating both on the same line ensures both calculations use the "old" values. Could also have stored `n_empties + n_fulls` in a temporary variable, but that would've taken a teeny bit more time & memory.

## Attempted solution(s)

Version 1:

```python
class Solution:
    def numWaterBottles(self, numBottles: int, numExchange: int) -> int:
        n_fulls = numBottles
        n_empties = 0
        n_drank = 0
        while True:
            n_drank += n_fulls
            n_empties += n_fulls
            if n_empties < numExchange:
                return n_drank
            n_fulls = n_empties // numExchange
            n_empties = n_empties % numExchange
```

![Version 1 results](https://github.com/paxtonfitzpatrick/leetcode-solutions/assets/26118297/08d502ae-a947-49fc-89a9-fb578ea937a6)

Version 2:

```python
class Solution:
    def numWaterBottles(self, numBottles: int, numExchange: int) -> int:
        n_drank = numBottles
        n_fulls = numBottles // numExchange
        n_empties = numBottles % numExchange
        while n_fulls > 0:
            n_drank += n_fulls
            n_fulls, n_empties = (n_empties + n_fulls) // numExchange, (n_empties + n_fulls) % numExchange
        return n_drank
```

![Version 2 results](https://github.com/paxtonfitzpatrick/leetcode-solutions/assets/26118297/ba0ca272-8761-4cc5-9c2f-9deb12d40361)
Appears to be slower than version 1, but probably just due to random variation runtime of the test cases. Pretty confident that in reality, version 2 is marginally faster.
