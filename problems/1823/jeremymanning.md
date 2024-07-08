# [Problem 1823: Find the Winner of the Circular Game](https://leetcode.com/problems/find-the-winner-of-the-circular-game/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- The first solution that comes to mind is to just run out the "game" until there is only one friend remaining
- It might be useful to copy the list to a circular linked list (so that the last element links back to the first).  This would take $O(n)$ time (where $n$ is the number of friends in the circle), and the final algorithm will almost certainly have worse complexity, so it would be "cheap" to do this.
- On the other hand, we could also just use `del` or `pop` to remove the relevant item with each round.  We'd need to keep track of where in the list we are ($i$), and just subtract the current list length from $i$ whenever $i$ exceeds $n$.
- I could potentially add a class to do this:
    - wraps `list`
    - adds an "index" to track where we are in the list
    - adds a function for incrementing the index (wrapping if needed)
    - adds a function for removing an element and updating the length accordingly
- Or this could be done using a `set`:
    - start with `x = set(range(1, n + 1))` and `i = 0`...or actually, that won't work, since `set`s are unordered.
- So let's say we start with `x = list(range(1, n + 1))` and `i = 0`
    - until `len(x) == 1`:
        - increment $i$ by $k - 1$ (the -1 is to account for counting the "current" friend)
        - wrap $i$ (i.e., `i %= len(x)`)
        - remove `x[i]`
    - Return the remaining friend
 
## Refining the problem, round 2 thoughts
- If $k == 1$ then the "winner" has to just be $n$.  If $k == 2$, the winner would be the second-to-last odd number.  Maybe there's a pattern here...🤔
- Let's go with the "easy" solution first and then refine if needed

## Attempted solution(s)
```python
class Solution:
    def findTheWinner(self, n: int, k: int) -> int:
        friends = list(range(1, n + 1))
        i = 0
        while len(friends) > 1:
            i = (i + k - 1) % len(friends)
            del friends[i]
        
        return friends[0]
```
- given test cases pass
    - `n = 49, k = 6`: pass
    - `n = 100, k = 17`: pass
    - `n = 302, k = 302`: pass
    - `n = 2, k = 1`: pass
- seems promising; submitting...

![Screenshot 2024-07-07 at 11 30 13 PM](https://github.com/ContextLab/leetcode-solutions/assets/9030494/ff26e9c1-db59-49d9-8d94-021804e5c53d)

Slow and inefficient...but solved!
