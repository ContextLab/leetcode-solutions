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

---

# Thinking more about this...

- Let's see if we can come up with an analytic solution
- We can initially drink `numBottles` (let's write this as $B$ to simplify notation)
- After that, every `numExchange` bottles (we'll write this as $E$ to simplify notation) turns into a full bottle (which can be added to the total) and then an empty bottle (which can be exchanged in the next round)

So the total drinkable number of bottles can be given by the series: $\text{total} = B + \left\lfloor \frac{B}{E} \right\rfloor + \left\lfloor \frac{\left\lfloor \frac{B}{E} \right\rfloor + (B \mod E)}{E} \right\rfloor + \left\lfloor \frac{\left\lfloor \frac{\left\lfloor \frac{B}{E} \right\rfloor + (B \mod E)}{E} \right\rfloor + ((B \mod E) \mod E)}{E} \right\rfloor + \ldots$

In other words:
  - Start by drinking $B$ bottles, which yields $B$ empty bottles
  - Those empties can be exchanged for $\left\lfloor \frac{B}{E} \right\rfloor$ new full bottles
  - There are $B \mod E$ additional empty bottles left after that exchange
  - In each subsequent round, we can repeat this same process (divide by $E$, take the floor, add this to the total number of drinks, add the remainder to the total number of empties)

Interestingly, we can see that $\left\lfloor \frac{\left\lfloor \frac{B}{E} \right\rfloor + (B \mod E)}{E} \right\rfloor$ simplifies to $\left\lfloor \frac{\left\lfloor \frac{B}{E} \right\rfloor}{E} \right\rfloor$:
  - $B \mod E$ is always less than $E$
  - Therefore $(B \mod E) / E$ is always less than 1, which means we can get rid of it in the "floor" operation

So now we have $\left\lfloor \frac{\left\lfloor \frac{B}{E} \right\rfloor}{E} \right\rfloor$, which simplifies to $\left\lfloor \frac{B}{E^2} \right\rfloor$.  In general (as the number of exchanges approaches infinity) we can see that
the exponent in the demoninator will keep growing (equal to the number of exchanges): $\sum_{k = 1}^\infty \left\lfloor \frac{B}{E^k} \right\rfloor$.  The demonitor is increasing exponentially, so the series will converge to...something.  I wish
I remembered my calculus better 🙃.

Doing some Googling, it looks like the series $\sum_{k = 0}^\infty x r^k$ converges to $\frac{x}{1 - r}$ if $|r| < 1$.  So...let's see...

We can take $x = B$ and $r = \frac{1}{E}$ (which is less than 1, since we know that $E \geq 2$).  So the series will converge to 

$\frac{B}{1 - \frac{1}{E}} = $B \frac{1}{1 - \frac{1}{E}} = B \frac{E}{E - 1}$.

Now we can split the fraction:

$B\frac{E}{E - 1} = B \left( 1 + \frac{1}{E - 1} \right)$

Which simplifies to:

$B \left( 1 + \frac{1}{E - 1} \right) = B + \frac{B}{E - 1}$.  Since we can only exchange "whole" bottles, we need to round down to the nearest integer:

$\frac{BE}{E - 1} \approx \left\lfloor \frac{B -1}{E - 1} \right\rfloor$.  So the *total* number of drinks is $B + \left\lfloor \frac{B -1}{E - 1} \right\rfloor$.

Finally(!!), we can turn this back into Python code:
```python
class Solution:
    def numWaterBottles(self, numBottles: int, numExchange: int) -> int:        
        return numBottles + (numBottles - 1) // (numExchange - 1)
```
- Test cases pass!!
- Checking a random additional test case: `numBottles = 48, numExchange = 7` (passes!)
- I'm just gonna submit this instead of checking in more detail...

![Screenshot 2024-07-07 at 2 47 33 PM](https://github.com/ContextLab/leetcode-solutions/assets/9030494/b17fec58-14a2-4faa-9f22-0bf1cdc13455)

Woo!  Go math 🎉!

