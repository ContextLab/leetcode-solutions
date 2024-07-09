# [Problem 1701: Average Waiting Time](https://leetcode.com/problems/average-waiting-time/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- Given the length of the customer list, I think we'll need to find an $O(n)$ solution
- Things to track:
    - Total wait time so far
    - Number of customers (this is just `len(customers)`, so we don't actually need to "track" it per se...but still)
    - Current time that the chef is occupied until
- Any special cases?  🤔...
    - What if all of the arrival times are the same?  --> Then the average wait time is just `sum([c[1] for c in customers]) / len(customers)`
    - Arrival times are already sorted, so no need to rearrange the list...

## Refining the problem, round 2 thoughts
- Let's start with `totalWait = 0` and `chefBusyUntil = 0`
- With each new customer (`[x, y]`):
    - If `x < chefBusyUntil`:
        - `totalWait += chefBusyUntil - x`  # wait until the chef is done with the current workload
    - Else:
        - `chefBusyUntil = x`  # need to wait until the next customer arrives to start on their request
    - `totalWait += y
    - `chefBusyUntil += y`
- Then return `totalWait / len(customers)`

## Attempted solution(s)
```python
class Solution:
    def averageWaitingTime(self, customers: List[List[int]]) -> float:
        totalWait = 0
        chefBusyUntil = 0
        
        for x, y in customers:
            if x < chefBusyUntil:
                totalWait += chefBusyUntil - x
            else:
                chefBusyUntil = x
            totalWait += y
            chefBusyUntil += y

        return totalWait / len(customers)
```
- given test cases pass
- `customers = [[5,2],[5,4],[10,3],[20,1],[21,10000],[21, 5]]`: pass
- `customers = [[1, 1000]]`: pass
- Ok, this seems fine...submitting...

![Screenshot 2024-07-08 at 10 43 28 PM](https://github.com/ContextLab/leetcode-solutions/assets/9030494/d5bcb9a8-1e6d-4867-9158-2a7d68f2b796)

solved!
