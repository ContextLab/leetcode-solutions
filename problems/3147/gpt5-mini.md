# [Problem 3147: Taking Maximum Energy From the Mystic Dungeon](https://leetcode.com/problems/taking-maximum-energy-from-the-mystic-dungeon/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I notice that from a starting index i you always visit indices i, i+k, i+2k, ... until you go out of bounds. So indices that share the same i % k form independent chains. For each such chain (residue class r), if you start at some position inside that chain you will pick the suffix sum from that position to the end of the chain. So the problem reduces to computing, for every index i, the total energy collected when starting at i which is energy[i] plus the total for i+k if it exists. That yields a simple recurrence dp[i] = energy[i] + dp[i+k] (or 0 if i+k out of bounds). The answer is the maximum dp[i] over all i.

This is linear-time doable by iterating from the end of the array backward and using previously computed dp values for i+k.

## Refining the problem, round 2 thoughts
- Edge cases: all negatives — we must still pick a starting point; dp handles that because dp[i] could be negative and we take the maximum (largest, i.e., least negative) value.
- Complexity: we can compute dp in O(n) time. Memory can be O(n) if we create a separate dp array, or O(1) extra if we overwrite the input array (if mutating input is allowed). I'll keep a dp copy for clarity.
- There is no need for complex data structures (like deques or heaps) because we are not choosing any subpath; it's fixed jumps of size k and the chain structure decouples residues.
- Implementation detail: just loop i from n-1 down to 0 and use dp[i+k] when available.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def maxEnergy(self, energy: List[int], k: int) -> int:
        """
        Compute maximum energy obtainable by starting at any index and jumping by k each time.
        dp[i] = energy[i] + (dp[i+k] if i+k < n else 0)
        Answer is max(dp[i]) for all i.
        """
        n = len(energy)
        # dp copy to avoid mutating input; could use energy in-place to save space
        dp = energy[:]  
        ans = -10**18  # sufficiently small sentinel
        for i in range(n - 1, -1, -1):
            if i + k < n:
                dp[i] = dp[i] + dp[i + k]
            # update answer
            if dp[i] > ans:
                ans = dp[i]
        return ans

# Example quick test
if __name__ == "__main__":
    sol = Solution()
    print(sol.maxEnergy([5,2,-10,-5,1], 3))  # expected 3
    print(sol.maxEnergy([-2,-3,-1], 2))      # expected -1
```
- Approach: Dynamic programming using the recurrence dp[i] = energy[i] + dp[i+k] when applicable. Iterate from right to left so dp[i+k] is already computed.
- Time complexity: O(n), where n = len(energy), because each index is processed once.
- Space complexity: O(n) due to the dp copy. This can be reduced to O(1) extra space by modifying the input array in-place (i.e., updating energy[i] instead of dp[i]).