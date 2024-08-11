# [Problem 1105: Filling Bookcase Shelves](https://leetcode.com/problems/filling-bookcase-shelves/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- this is an interesting problem. We need to divide the sequences of books into subsequences of shelves, optimizing for the minimum sum of the shelves' heights we can achieve with shelves that are at most `shelfWidth` wide.
- okay my initial thought is that a potential algorithm could go something like this:
  - We know the first book **must** go on the first shelf, so place it there. The height of the first shelf is now the height of the first book.
  - Then, for each subsequent book:
    - if the book can fit on the same shelf as the previous book without increasing the shelf's height (i.e., its height is $\le$ the curent shelf height (the height of the tallest book on the shelf so far) and its with + the width of all books placed on the shelf so far is $\le$ `shelfWidth`), then place it on the same shelf.
    - elif the book can't fit on the same shelf as the previous without exceeding `shelfWidth`, then we **must** place it on the next shelf
      - I think we'll then have to tackle the sub-problem of whether moving some of the preceding books from the last shelf to this next shelf would decrease the height of that last shelf without increasing the height of this next shelf... or maybe it's okay to increase this next shelf's height if doing so decreases the previous one's by a larger amount? This feels like it could get convoluted fast...
    - else, the book *can* fit on the same shelf as the previous but *would* increase the shelf's height, so we need to determine whether it's better to place it on the current shelf or start a new shelf.
      - is this conceptually the same sub-problem as the one above? Not sure...
- I think the basic thing we're optimizing for is having tall books on the same shelf as other tall books whenever possible. This makes me think we might want to try to identify "optimal runs" of books in the array containing as many tall books as possible whose total width is $\le$ `shelfWidth`. Maybe I could:
  - sort a copy of the input list by book height to find the tallest books
  - then in the original list, search outwards (left & right) from the index of each tallest book to try to create groupings of books that contain as many tall books as possible.
    - How would I formalize "as many tall books as possible"? Maximizing the sum of the grouped books' heights doesn't seem quite right...
    - Since I want tall books together *and* short books together, maybe I could come up with a scoring system for groupings that penalizes books of different heights being in the same group? Something like trying to minimize the sum of the pairwise differences between heights of books in the same group?
      - anything that involves "pairwise" raises a red flag for me though because it hints at an $O(n^2)$ operation, which I'd like to avoid
  - Though I'm not sure how I'd do this without leaving the occasional odd short book on its own outside of any subarray, meaning it'd end up on its own shelf, which isn't good...
- the general steps I wrote out above also make me think of recursion, since they entail figuring out which of two options is better (place a book on the current shelf or start a new shelf when either is possible) by optimizing the bookshelf downstream of both decisions and then comparing the result.
  - I think framing this as a recursion problem also resolves my confusion about the potential need to "backtrack" in the case where we're forced by `shelfWidth` to start a new shelf, in order to determine wether it'd be better to have placed some previous books on that new shelf as well -- if we simply test out the result of placing each book on the same shelf and on a new shelf, then we wouldn't have to worry about that because all of those combinations of books on a shelf would be covered.
  - the downside that testing both options (same shelf and new shelf) for *every* book, for *every other* would make the runtime $O(2^n)$, I think, which is pretty rough.
  - although... maybe I could reduce this significantly? Say we put book $n$ on a given shelf, then put book $n+1$ on that same shelf, then put book $n+2$ on a new shelf. Or, we put book $n$ on a given shelf, then put book $n+1$ on a new shelf, then also put book $n+2$ on a new shelf. In both cases, all subsequent calls in that branch of the recursion tree follow from a shelf that starts with book $n+2$. So if I can set up the recursive function so that it depends only on the current book and the amount of room left on the current shelf, then I could use something like `functools.lru_cache()` to memoize the results of equivalent recursive calls. I think this would end up covering the vast majority of calls if I can set it up right.
    - actually, I think `functools.lru_cache()` would be overkill since it adds a lot of overhead to enable introspection, discarding old results, etc. I think I'd be better off just using a regular dict instead.
  - also, even before the memoization, I think it should be slightly better than $O(2^n)$ because there will be instances of the second case I noted above where the next book *can't* be placed on the current shelf and **must** be placed on the next shelf.
  - I'm not 100% sure the recursive function can be written to take arguments that'll work for the memoization (hashable, shared between calls that should share a memoized result and not those that don't, etc.) the memoization, but I think I'll go with this for now and see if I can make it work
- so how would I set this up recursively?
  - I think the "base case" will be when I call the recursive function on the last book. At that point, I'll want to return the height of the current shelf so that in the recursive case, I can add the result of a recursive call to the current shelf's height to get the height of the bookshelf past the current book.
    - actually, what I do will be slightly different for the two possible cases, because I'll need to compare the rest-of-bookshelf height between the two options to choose the optimal one:
      - if placing the next book on a new shelf, the rest-of-bookshelf height will be the current shelf's height plus the returned height
      - if placing the next book on the current shelf, the rest-of-bookshelf height will be the larger of the current shelf's height and the book's height, plus the returned height

<!-- - okay my initial thought is that a potential algorithm could go something like this:
  - first, find an initial "naïve" total height and then see if it's possible to optimize from there. The initial total height is the bookshelf height we get if we fill each shelf with as many books as possible without exceeding `shelfWidth`.
  - to see if we can do better than this inital height, move the last book we placed on the first shelf to the second shelf, the last book on the second shelf to the third shelf, and so on. Repeat until there's only one book left on the first shelf.
  - Then -->

## Refining the problem, round 2 thoughts

## Attempted solution(s)

```python
class Solution:
    def minHeightShelves(self, books: List[List[int]], shelfWidth: int) -> int:

```
