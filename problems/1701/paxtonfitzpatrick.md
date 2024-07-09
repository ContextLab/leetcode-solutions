# [Problem 1701: Average Waiting Time](https://leetcode.com/problems/average-waiting-time/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- this one looks fun! Seems like it shouldn't be too tricky to implement the "actually play everything out" solution, but significantly harder to come up with a formulaic solution -- if possible at all.
- could be fun to do this in a "proper" OOP way, where we create and store `Customer` objects who record their arrival times, "meal finished" times, etc. Might try practicing that instead of optimizing for efficiency on this one.
- actually... I think the "trick" for this problem might be that we can figure out each customer's wait time by taking the total time needed to cook all preceding orders, adding the time needed to cook the current customer's order, and subtracting the current customer's arrival time (edit: oh, and ~~subtracting~~ adding the first customer's arrival time)
  - hmmm but does this still work if the chef ends up with "idle" time at some point? e.g., if `customers[0]` is `[1, 2]` and `customers[1]` is `[4, 5]`
  - nope, this gives `-5` for the 4th customer in example 2, which is obviously wrong.
- instead, let's loop through customers and keep track of the time when the chef is free to start the next order. Then on the next iteration:
  - if the customer's arrival time is less than that (i.e., before the chef is available), we can add the current customer's meal prep time to it, and subtract their arrival time to get their wait time
  - otherwise, if the customer's arrival time is greater than that (i.e., the chef can start their order as soon as they arrive), then their wait time is just their meal prep time minus their arrival time
- I'll keep a running total of customers' wait times so I can divide it by the number of customers at the end and return that

## Refining the problem, round 2 thoughts
- I was originally going to set the logic in the loop up as an `if`/`else` statement but noticed some of it oculd be simplified. I'm sure there's a more efficient way to do this, but I've gotta move on for now so I'll come back to this later if I have time.

## Attempted solution(s)

```python
class Solution:
    def averageWaitingTime(self, customers: List[List[int]]) -> float:
        total_wait_time = 0
        chef_available_at = 0

        for (arrival_time, prep_time) in customers:
            prep_start_time = max(arrival_time, chef_available_at)
            chef_available_at = prep_start_time + prep_time
            total_wait_time += chef_available_at - arrival_time

        return total_wait_time / len(customers)
```
![](https://github.com/paxtonfitzpatrick/leetcode-solutions/assets/26118297/f76e56e3-d17a-485a-9a3f-1b2b6f9f364c)
