# [Problem 1622: Fancy Sequence](https://leetcode.com/problems/fancy-sequence/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need to support append, addAll, multAll, and getIndex efficiently. Naively applying addAll or multAll to every element is O(n) per operation and too slow (up to 1e5 ops). The operations are linear transforms on values: each element's value is transformed by x -> x * m + a for sequences of multiplies and adds. That suggests keeping a global linear transformation state (mul, add) that represents how to convert a stored "base" value to its current value. When appending, we can store a normalized base so that current value after the global transform equals the appended value. When retrieving, apply the global transform to the stored base. That avoids touching all stored elements on addAll/multAll.

I recall two equivalent ways:
- Store for each appended element the global (mul, add) at its append time and the original value, then invert the per-append transform when computing current value.
- Or normalize the appended value at append-time by applying the inverse of current global mul/add, i.e., store base = (val - add) * inv(mul) so that current = base * mul + add.

I'll use the second (store normalized base) because it's simpler: only need a global mul and add, and per-append compute one modular inverse.

Careful: operations are modulo MOD = 10^9+7. The multiplicative inverse exists because m in operations is between 1 and 100 and MOD is prime, so mul (product of ms modulo MOD) will never be 0 modulo MOD (can't get a factor of MOD from small integers). Use pow(mul, MOD-2, MOD) for inverse.

## Refining the problem, round 2 thoughts
Refinements and edge cases:
- getIndex must return -1 if idx out of bounds.
- Maintain arr of stored normalized bases (one per append). For append(val): compute base = (val - add) * inv(mul) mod MOD and append.
- For addAll(inc): update add = (add + inc) % MOD.
- For multAll(m): update mul = mul * m % MOD and add = add * m % MOD (since (x * mul + add) * m = x * (mul*m) + add*m).
- For getIndex(idx): compute (base * mul + add) % MOD.
- Need to handle negative (val - add) with modulo.
- Complexity: each operation O(1) except append does modular inverse with pow (O(log MOD) ~ 30), which is fine for <=1e5 operations.

Alternative approach: store (value, mul_at_append, add_at_append) and compute factor = current_mul * inv(mul_at_append) to reconstruct. Complexity similar.

Now implement the class with Python, using pow for modular inverse.

## Attempted solution(s)
```python
MOD = 10**9 + 7

class Fancy:
    def __init__(self):
        # stores normalized base values for each appended element
        self.arr = []
        # global transformation: current_value = base * mul + add (mod MOD)
        self.mul = 1
        self.add = 0

    def append(self, val: int) -> None:
        # store base such that base * mul + add == val (mod MOD)
        # base = (val - add) * inv(mul) mod MOD
        base = (val - self.add) % MOD
        inv_mul = pow(self.mul, MOD - 2, MOD)
        base = (base * inv_mul) % MOD
        self.arr.append(base)

    def addAll(self, inc: int) -> None:
        self.add = (self.add + inc) % MOD

    def multAll(self, m: int) -> None:
        self.mul = (self.mul * m) % MOD
        self.add = (self.add * m) % MOD

    def getIndex(self, idx: int) -> int:
        if idx < 0 or idx >= len(self.arr):
            return -1
        base = self.arr[idx]
        return (base * self.mul + self.add) % MOD
```
- Notes:
  - Approach: normalize stored values on append so that no per-element updates are necessary on addAll/multAll. Maintain global linear transform (mul, add).
  - Time complexity: append is O(log MOD) due to modular inverse pow (≈ O(30) operations), addAll and multAll are O(1), getIndex is O(1).
  - Space complexity: O(n) where n is the number of appended elements (stored normalized bases).
  - Implementation details: use pow(self.mul, MOD-2, MOD) to compute modular inverse. Ensure subtraction uses modulo to avoid negatives.