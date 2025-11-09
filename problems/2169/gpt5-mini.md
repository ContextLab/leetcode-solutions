# [Problem 2169: Count Operations to Obtain Zero](https://leetcode.com/problems/count-operations-to-obtain-zero/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
The problem describes repeatedly subtracting the smaller number from the larger until one becomes zero. The naive idea is to simulate the process: in each operation check which is larger and subtract. That would work but could be slow if one number is much larger than the other (many repeated subtractions). This pattern is exactly what the Euclidean algorithm's repeated-subtraction version does to compute gcd. We can compress multiple repeated subtractions into a single step using integer division: when a >= b > 0, subtracting b from a repeatedly is equivalent to doing a //= b times and then a %= b, adding a // b to the operation count.

Edge cases: if either number is zero initially return 0; equal numbers result in one operation.

## Refining the problem, round 2 thoughts
So the efficient approach is to loop while both numbers are positive and at each step add the quotient (larger // smaller) to the count and reduce the larger number with modulo. This mimics repeated subtraction in O(number of Euclidean steps) which is O(log(min(num1, num2))) in practice. Need to ensure we don't divide by zero — guard with while a and b. Complexity is good for the given constraints (<= 1e5) but the approach scales much larger as well.

## Attempted solution(s)
```python
class Solution:
    def countOperations(self, num1: int, num2: int) -> int:
        a, b = num1, num2
        ops = 0
        # While both are non-zero, compress repeated subtractions with division
        while a and b:
            if a >= b:
                ops += a // b
                a = a % b
            else:
                ops += b // a
                b = b % a
        return ops
```
- Notes:
  - Approach: simulate repeated subtraction but group many subtractions at once using integer division (quotient) and modulo to get the remainder — effectively the subtraction-based Euclidean algorithm.
  - Time complexity: O(log(min(num1, num2))) in practice (number of division/mod steps similar to Euclidean algorithm). Each loop iteration uses O(1) arithmetic operations.
  - Space complexity: O(1) extra space.
  - Implementation details: loop guarded by "while a and b" to avoid division by zero. If either input is 0 initially, the function immediately returns 0.