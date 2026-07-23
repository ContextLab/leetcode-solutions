# [Problem 3513: Number of Unique XOR Triplets I](https://leetcode.com/problems/number-of-unique-xor-triplets-i/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We are given a permutation nums of 1..n. Triplets allowed have indices i <= j <= k, so because the array is a permutation (all values distinct), duplicates of values occur only when indices are equal. Observing XOR properties:
- If i = j = k, result is nums[i].
- If two indices are equal and one is different, the equal pair cancels (x^x=0) leaving the lone value -> again a single element from the array.
- If all three indices are distinct, the result is XOR of three distinct numbers from 1..n.

Therefore the set of obtainable XOR values is exactly:
- all single elements (i.e., {1,2,...,n}), and
- all XORs of three distinct elements from {1..n}.

We need to count the number of distinct values among these. Brute forcing all triples is O(n^3) (or O(n^2) with pairwise precomputation) which is infeasible for n up to 1e5. We need a structural observation about which values become obtainable when we allow XORs of three distinct numbers from the full set 1..n.

I tried small n by hand:
- n=1 -> {1} => 1
- n=2 -> {1,2} => 2
- n=3 -> achievable values {0,1,2,3} => 4
- n=4 -> achievable values 0..7 => 8
- n=5 -> still 0..7 => 8

That suggests a pattern tied to powers of two and the highest bit available in numbers 1..n.

## Refining the problem, round 2 thoughts
Let b = floor(log2(n)), and p = 2^b. All numbers in nums are < 2^{b+1}. The maximum possible XOR of any numbers from 1..n is < 2^{b+1}, so potential values lie in [0, 2^{b+1}-1]. We always have singles {1..n}. For n >= 3 we can also form 0 (e.g., 1^2^3 = 0). A constructive argument shows that for every x in [0, 2^{b+1} - 1], we can realize x either as a single element when x <= n, or as XOR of three distinct elements when x > n (and n >= 3). Sketch of constructive method for x >= p (i.e., having the top bit set):
- write x = p + y with 0 <= y < p.
- if y = 0 then x = p <= n (since p <= n) we are done by single element;
- otherwise pick u ∈ {1,2} with u != y (if y=1 pick u=2, else pick u=1). Then set triple (p, u, u^y). Because u^y < p <= n and is != u, and p is distinct, we get three distinct values and p ^ u ^ (u ^ y) = p ^ y = x.

This covers all x in [p, 2p - 1]. Combining with x < p covered by singles and 0 covered by 1^2^3 when n>=3, we obtain the entire interval [0, 2^{b+1}-1] when n >= 3. So:
- If n == 1 => answer = 1.
- If n == 2 => cannot have three distinct indices -> only singles {1,2} => answer = 2.
- If n >= 3 => answer = 2^{b+1} where b = floor(log2(n)) -> equivalently 1 << (n.bit_length()) because bit_length = b+1 and we want 2^{b+1}.

Time/space: O(1) time, O(1) space.

## Attempted solution(s)
```python
class Solution:
    def countTriplets(self, nums: list[int]) -> int:
        # nums is a permutation of 1..n
        n = len(nums)
        if n <= 2:
            return n
        # For n >= 3, answer = 2^(floor(log2(n)) + 1)
        # bit_length gives floor(log2(n)) + 1, so:
        return 1 << (n.bit_length())
```
- Notes:
  - The reasoning uses XOR linearity and a constructive argument to show that for n >= 3 every value in [0, 2^{b+1}-1] is achievable either as a single element (if ≤ n) or as XOR of three distinct elements (if > n).
  - Complexity: O(1) time and O(1) extra space.
  - Implementation detail: Python's int.bit_length() returns floor(log2(n)) + 1 for n > 0. We return 1 << (n.bit_length()) which equals 2^{floor(log2(n)) + 1}. Special-case n <= 2 to handle small n where three-distinct-element constructions are impossible.