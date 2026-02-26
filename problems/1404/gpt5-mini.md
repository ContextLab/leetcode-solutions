# [Problem 1404: Number of Steps to Reduce a Number in Binary Representation to One](https://leetcode.com/problems/number-of-steps-to-reduce-a-number-in-binary-representation-to-one/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are given a binary string s (most significant bit first). We must count steps to reduce the represented integer to 1 using: if even divide by 2, if odd add 1. Converting to integer may overflow (s length up to 500) and is unnecessary. We can simulate operations on the binary representation. A straightforward simulation would repeatedly modify the string: if last bit 0 -> remove it (divide), if last bit 1 -> add 1 (propagate a carry). That simulation is correct but doing string modifications per step could be O(n^2) in worst case if done naively.

I recall there's a linear trick: process bits from right to left, keeping a "carry" that represents whether we've had a +1 overflow to higher bits. For each bit (except the highest), depending on bit + carry we know whether we need 1 step (divide) or 2 steps (add then divide) and how the carry evolves. At the end, if carry remains, it affects the highest bit and may add one more step.

## Refining the problem, round 2 thoughts
Consider a single bit position i (starting from least significant, i = n-1 down to 1). Let val = int(s[i]) + carry where carry is 0 or 1.
- If val == 0: the current number is even at this low part, so one divide by 2 step removes this bit => steps += 1, carry stays 0.
- If val == 1: odd => we must add 1 (one step) making it even, then divide by 2 (another step). The add produces a carry into the next bit => steps += 2 and carry becomes 1.
- If val == 2: bit was 1 and carry 1 => value 2 (even), so dividing by 2 consumes this digit in one step; carry remains 1 (since bit+carry was 2 => after dividing the carry still propagates as 1 to higher bits). So steps += 1, carry stays 1.

We stop at index 0 after handling indices n-1 down to 1. For the most significant bit:
- If carry == 0 => top bit remains '1' -> we're at 1 -> no extra steps.
- If carry == 1 => top becomes '10' (i.e., value 2), which needs one final divide to become 1 -> steps += 1. So we can add carry to steps at the end.

This yields a single pass O(n) solution and O(1) extra space.

Edge cases: s == "1" -> 0 steps. All zeros except leading 1 not allowed by constraints. Works for maximal length.

## Attempted solution(s)
```python
class Solution:
    def numSteps(self, s: str) -> int:
        """
        Compute number of steps to reduce binary string s to "1" using:
        - if even: divide by 2
        - if odd: add 1
        Approach: scan from right to left, track carry (0/1). For each bit except the MSB,
        derive steps based on bit + carry:
          sum == 0 -> one divide (steps += 1), carry = 0
          sum == 1 -> add then divide (steps += 2), carry = 1
          sum == 2 -> one divide (steps += 1), carry = 1
        Finally add carry for MSB (if carry == 1 we need one extra divide).
        """
        n = len(s)
        # Quick handle trivial case
        if n == 1:
            return 0

        steps = 0
        carry = 0
        # Process from least significant bit to the second-most-significant bit
        for i in range(n - 1, 0, -1):
            bit = 1 if s[i] == '1' else 0
            total = bit + carry
            if total == 0:
                # even -> divide by 2
                steps += 1
                # carry stays 0
            elif total == 1:
                # odd -> add 1 then divide -> 2 steps, produces carry 1
                steps += 2
                carry = 1
            else:  # total == 2
                # 2 is even -> divide -> 1 step, carry remains 1
                steps += 1
                carry = 1

        # handle most significant bit: if there's a remaining carry, it turns '1' -> '10',
        # which requires one final divide to reach '1'. So add carry.
        steps += carry
        return steps
```
- Notes about the solution:
  - Time complexity: O(n) where n = len(s) because we make a single pass over the bits.
  - Space complexity: O(1) extra space (only counters and carry).
  - The solution avoids big integer conversion and avoids per-step string modifications; it leverages bitwise reasoning to count steps directly.