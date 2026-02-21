# [Problem 762: Prime Number of Set Bits in Binary Representation](https://leetcode.com/problems/prime-number-of-set-bits-in-binary-representation/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to count numbers in [left, right] whose binary representation contains a prime number of 1-bits. The constraints are small: right ≤ 1e6 and the range width ≤ 1e4, so iterating each number in the interval is fine. For each number, I need the number of set bits — Python's bin(x).count('1') or int.bit_count() will do. The maximum number of bits for numbers up to 1e6 is about 20 (2^20 = 1,048,576), so primes to check are only up to 20. I can precompute a small set of primes {2,3,5,7,11,13,17,19} and check membership for each count.

## Refining the problem, round 2 thoughts
Edge cases: single number intervals (left == right) should work. We should remember that 1 is not prime. Use a constant set of primes for speed and simplicity. Time complexity will be linear in the number of integers in the range times the cost to count bits (≈O(20) per integer). Space is O(1). Alternative would be a sieve for primes up to 20, but a hard-coded set is simpler and sufficient.

## Attempted solution(s)
```python
class Solution:
    def countPrimeSetBits(self, left: int, right: int) -> int:
        # Precomputed primes up to 20 (sufficient for numbers <= 10^6)
        prime_set = {2, 3, 5, 7, 11, 13, 17, 19}
        count = 0
        for x in range(left, right + 1):
            # Use int.bit_count() if available; fallback to bin().count('1')
            bits = x.bit_count() if hasattr(int, "bit_count") else bin(x).count("1")
            if bits in prime_set:
                count += 1
        return count
```
- Notes:
  - Approach: iterate each integer in the range, count its set bits, and check if that count is prime via a small precomputed set.
  - Time complexity: O(n * b) where n = right - left + 1 and b is the number of bits (~≤20). Practically O(n).
  - Space complexity: O(1) extra space.
  - Implementation detail: int.bit_count() is used when available (faster); otherwise bin(x).count('1') is used. The prime set covers all possible bit counts for the input constraints.