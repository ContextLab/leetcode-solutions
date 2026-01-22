# [Problem 2043: Simple Bank System](https://leetcode.com/problems/simple-bank-system/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This looks straightforward: we need to simulate a simple bank with deposit, withdraw, and transfer operations. The key detail is 1-indexed account numbers versus the 0-indexed input balance array. Each operation must check account validity (1..n) and for withdraw/transfer also check sufficient balance. No tricky data structures are needed — just keep balances in a list and update on valid ops. Watch out for large money values (up to 1e12) but Python integers handle that. Also consider operations where account1 == account2 for transfer (should be allowed if funds sufficient, but effectively no net change).

## Refining the problem, round 2 thoughts
- Validate account indices at start of each method.
- For transfer: check both accounts valid and that source has enough money before doing any updates.
- For withdraw: check account valid and enough balance.
- For deposit: just check valid account and add money.
- Complexity: each operation is O(1) time and O(1) extra space; initial storage is O(n).
- Edge cases: money == 0 (valid), accounts out of range, transferring to same account (allowed if funds available).
- Implementation detail: convert 1-indexed account to 0-indexed index when accessing the internal list.

## Attempted solution(s)
```python
class Bank:
    def __init__(self, balance: list[int]):
        # store balances in a 0-indexed list
        self.balances = balance
        self.n = len(balance)

    def _valid(self, account: int) -> bool:
        # account is 1-indexed; valid if 1 <= account <= n
        return 1 <= account <= self.n

    def transfer(self, account1: int, account2: int, money: int) -> bool:
        if not self._valid(account1) or not self._valid(account2):
            return False
        i = account1 - 1
        j = account2 - 1
        if self.balances[i] < money:
            return False
        # perform transfer
        self.balances[i] -= money
        self.balances[j] += money
        return True

    def deposit(self, account: int, money: int) -> bool:
        if not self._valid(account):
            return False
        self.balances[account - 1] += money
        return True

    def withdraw(self, account: int, money: int) -> bool:
        if not self._valid(account):
            return False
        i = account - 1
        if self.balances[i] < money:
            return False
        self.balances[i] -= money
        return True
```
- Notes about the solution:
  - Approach: Keep the balances in a list and perform simple index checks and arithmetic for each operation.
  - Time complexity: O(1) per operation (transfer, deposit, withdraw).
  - Space complexity: O(n) to store the balances (where n is number of accounts); additional space O(1).
  - Implementation details: convert 1-indexed account numbers to 0-indexed list indices. Use a helper _valid to centralize account-range checking. Python's int handles the large money ranges specified.