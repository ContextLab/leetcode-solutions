# [Problem 1346: Check If N and Its Double Exist](https://leetcode.com/problems/check-if-n-and-its-double-exist/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
I need to determine whether there exist two indices i != j such that arr[i] == 2 * arr[j]. A straightforward idea is to check, for every value v in the array, whether 2*v also appears. Using a set would let me test membership quickly. But I must be careful about the case v == 0: 2*0 == 0, so a single zero in the set would incorrectly indicate a pair unless I ensure there are at least two zeros. That suggests using counts (a Counter or dictionary) so I can handle duplicates correctly. Alternatively, I could track seen values while scanning and check both directions (x*2 in seen or x is even and x//2 in seen), but using counts is simple and clear.

## Refining the problem, round 2 thoughts
- The required relation is directional (arr[i] == 2 * arr[j]) but checking for any pair is symmetric: for any element v we only need to see if 2*v exists.
- Edge case: v == 0 requires count >= 2.
- Negative numbers are fine; doubling preserves sign, and membership checks don't care about sign.
- Using a Counter (O(n) time and O(n) space) is simple and robust. Alternatively, a single-pass set approach also works (checking x*2 in seen or x is even and x//2 in seen).
- Constraints are small (n ≤ 500), so either approach is efficient.
- Complexity target: O(n) time, O(n) space.

## Attempted solution(s)
```python
from collections import Counter
from typing import List

class Solution:
    def checkIfExist(self, arr: List[int]) -> bool:
        cnt = Counter(arr)
        for v in cnt:
            # If 2*v exists and either it's a different value or there are at least two occurrences (handles v == 0)
            if 2 * v in cnt:
                if 2 * v != v or cnt[v] > 1:
                    return True
        return False
```
- Notes:
  - Approach: Count occurrences of each value. For each distinct value v, check if 2*v exists in the counts. If v == 0 (the only case where 2*v == v), ensure cnt[v] > 1 to guarantee two different indices.
  - Time complexity: O(n), where n = len(arr), because we build the counter and iterate over its keys.
  - Space complexity: O(n) for the counter in the worst case (all distinct values).
  - Implementation details: Using Counter simplifies handling duplicates (especially zero). This solution is concise and handles negatives and duplicates correctly.