# [Problem 3514: Number of Unique XOR Triplets II](https://leetcode.com/problems/number-of-unique-xor-triplets-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the number of distinct values obtainable as nums[i] XOR nums[j] XOR nums[k] for i <= j <= k. Because XOR is associative and commutative, the order of the three values doesn't matter. Also, since indices are allowed to be equal (i<=j<=k) and you may pick the same index multiple times, any triple of values chosen from the array (with repetition allowed) is valid. So the set of achievable XORs is exactly {x ^ y ^ z | x, y, z are elements of nums, repetitions allowed}.

A direct triple loop would be O(n^3) (n up to 1500) — too slow. But we can precompute all pairwise XORs and then XOR each with each single element. That gives O(n^2 + n * U) work where U is the number of distinct pairwise XOR values (bounded by the maximum possible XOR value, which is small because nums[i] ≤ 1500). Using a boolean/byte array or a small set for pairwise results keeps this efficient.

## Refining the problem, round 2 thoughts
- We can compute pairwise XORs for i <= j to respect that repetition is allowed; this yields roughly n*(n+1)/2 computations.
- nums[i] ≤ 1500 implies XOR results fit within 11 bits, so max XOR < 2048. We can safely use an array of size 2048 to mark which XOR values exist.
- After collecting pairwise XORs (unique), iterate over each element z in nums and for each pairwise XOR p mark p ^ z as achievable. Keep a boolean/byte array for final results.
- Complexity: O(n^2 + n * M) where M ≤ 2048. Memory: O(M).
- Edge cases: small n works; duplicates handled because repetition allowed (using i<=j in pair computation is fine).

## Attempted solution(s)
```python
from typing import List

class Solution:
    def countTriplets(self, nums: List[int]) -> int:
        if not nums:
            return 0
        n = len(nums)
        # Upper limit for XOR values. nums[i] <= 1500 so XOR < 2048
        LIMIT = 2048
        
        # boolean array for pairwise XOR existence
        pair_exist = bytearray(LIMIT)
        # compute pairwise XORs for i <= j (repetition allowed)
        for i in range(n):
            ai = nums[i]
            for j in range(i, n):
                pair_exist[ai ^ nums[j]] = 1
        
        # collect distinct pairwise XOR values to iterate faster
        pair_values = [v for v, present in enumerate(pair_exist) if present]
        
        # boolean array for resulting triple XORs
        result_exist = bytearray(LIMIT)
        for z in nums:
            for p in pair_values:
                result_exist[p ^ z] = 1
        
        # count distinct results
        return sum(result_exist)
```
- Notes:
  - We compute pairwise XORs for i <= j to respect the allowed repetitions. Any triple x,y,z (with repetition) can be formed because indices can be equal, so this covers all valid triples.
  - Using bytearray of size 2048 keeps memory small and operations fast; extracting pair_values reduces the inner loop cost.
  - Time complexity: O(n^2 + n * M) where M ≤ 2048 (practically O(n^2) dominated by pairwise loop). For n ≤ 1500 this is easily within limits.
  - Space complexity: O(M) for the boolean arrays (M = 2048).