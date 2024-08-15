# [Problem 860: Lemonade Change](https://leetcode.com/problems/lemonade-change/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
- What a breath of fresh air after yesterday's problem.
- This one seems very easy.  We could either solve this by using a list to track all of the bills in our collection, or (more efficiently) we could use a hash table to track the numbers of each possible type of bill.  There are only three, so we can initialize `register = {5: 0, 10: 0, 20: 0}`.
- Then we just step through one bill at a time, updating `register` as needed.  The amount of change is just `bill[i] - 5`.
- There are just a few options for how much change might be needed: 0, 5, or 15:
    - No change is needed if someone pays with a $5 bill.  There's no need to check the register, but we update `register[5] += 1`.
    - $5 in change is needed if someone pays with $10.  Update `register[10] += 1` and decrement `register[5] -= 1` (or return false if that dips `register[5]` below 0.
    - $15 in change is needed if someone pays with a $20.  This requires one of the following:
        - 1 $10 and 1 $5 bill if available
        - 3 $5 bills otherwise
        - We should always prefer giving change with larger bills, because this preserves our flexibility in later transactions

## Refining the problem, round 2 thoughts
- No edge cases I can think of...let's implement it!

## Attempted solution(s)
```python
class Solution:
    def lemonadeChange(self, bills: List[int]) -> bool:
        cost = 5
        register = {5: 0, 10: 0, 20: 0}
        
        for payment in bills:
            register[payment] += 1
            change = payment - cost
            if change == 0:
                continue
            elif change == 5:
                if register[5] <= 0:
                    return False
                register[5] -= 1
            elif change == 15:                
                if register[10] > 0 and register[5] > 0:  # try making change with $10 and $5
                    register[10] -= 1
                    register[5] -= 1
                elif register[5] >= 3:  # try making change with 3 $5 bills
                    register[5] -= 3
                else:  # correct change is not available
                    return False
        
        return True
```
- Given test cases pass
- Let's make up some new test cases:
    - `bills = [10, 5, 10, 5, 10, 20, 5, 5, 10, 5, 5, 5, 20, 20, 20, 10, 10, 10, 10, 5, 10, 10, 10, 10, 20, 5, 20, 10, 10, 10, 20, 10, 10, 5, 5, 20, 20, 5, 5, 10, 10, 5, 5, 5, 5, 10, 10, 20, 5, 5, 10, 20, 20, 5, 20, 5, 20, 10, 5, 20, 20, 5, 5, 5, 10, 5, 20, 10, 10, 10, 5, 10, 5, 5, 10, 20, 10, 10, 20, 10, 20, 20, 20, 10, 20, 5, 20, 5, 10, 10, 20, 5, 5, 20, 20, 5, 5, 10, 20, 20]`: pass
    - `bills = [5, 10, 5, 10, 5, 10, 20, 5, 5, 10, 5, 5, 5, 20, 20, 20, 10, 10, 10, 10, 5, 10, 10, 10, 10, 20, 5, 20, 10, 10, 10, 20, 10, 10, 5, 5, 20, 20, 5, 5, 10, 10, 5, 5, 5, 5, 10, 10, 20, 5, 5, 10, 20, 20, 5, 20, 5, 20, 10, 5, 20, 20, 5, 5, 5, 10, 5, 20, 10, 10, 10, 5, 10, 5, 5, 10, 20, 10, 10, 20, 10, 20, 20, 20, 10, 20, 5, 20, 5, 10, 10, 20, 5, 5, 20, 20, 5, 5, 10, 20, 20]`: pass
    - `bills = [5, 5, 10, 20, 20, 10, 10, 20, 20, 5, 5, 10, 20, 10, 20, 5, 10, 10, 20, 5]`: pass
    - `bills = [5, 5, 5, 5, 10, 20, 5, 5, 5, 5, 10, 5, 10, 10, 10, 20, 5]`: pass
- Ok...seems like it's working; let's submit...

![Screenshot 2024-08-14 at 11 55 03 PM](https://github.com/user-attachments/assets/1001e9e4-6917-4727-ab28-5523c342a859)

Solved!

