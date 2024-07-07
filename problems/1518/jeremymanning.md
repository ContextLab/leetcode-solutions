# [Problem 1518: Water Bottles](https://leetcode.com/problems/water-bottles)

## Initial thoughts (stream-of-consciousness)
- There's almost certainly an analytic solution to this problem-- something like (number of bottles) + (log (base exchange rate) number of bottles) + 1...but probably not *quite* that simple
- The naive solution would be to do something like:
    - keep a running total of the number of bottles that have been drunk
    - then, until there are fewer than `numExchange` bottles left:
        - exchange as many bottles as possible and add that to the total
        - update the number of remaining bottles
- If `numExchange` was 1, we'd get an infinite loop, but it looks like this isn't allowed (`2 <= numExchange <= 100`)


## Refining the problem, round 2 thoughts
- I'll start by implementing the naive solution.  Given the problem specification (maximum `numBottles` is 100, minimum `numExchange` is 2), I don't think we'll run out of compute time...
- Updating the number of remaining bottles should work as follows:
    - Exchange whatever we can.  The number of bottles now in our collection is `availableBottles // numExchange`
    - Also track what's left over (`availableBottles % numExchange`)

## Attempted solution(s)
```python
class Solution:
    def numWaterBottles(self, numBottles: int, numExchange: int) -> int:        
        drinkableTotal = numBottles
        bottlesAvailable = numBottles

        while bottlesAvailable >= numExchange:
            nextExchange = bottlesAvailable // numExchange
            drinkableTotal += nextExchange
            
            bottlesAvailable %= numExchange
            bottlesAvailable += nextExchange

        return drinkableTotal
```
- All given test cases pass
- Other test cases:
    - `numBottles = 100, numExchange = 2`: passes
    - `numBottles = 100, numExchange = 3`: passes
    - `numBottles = 100, numExchange = 4`: passes
    - `numBottles = 48, numExchange = 7`: passes
- Seems ok...submitting...

![Screenshot 2024-07-06 at 11 47 50 PM](https://github.com/ContextLab/leetcode-solutions/assets/9030494/66a9540c-5afc-4cd4-9652-6e8aa99ab59d)

Slow, but I'll take it-- solved!
