# [Problem 2418: Sort the People](https://leetcode.com/problems/sort-the-people/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
This is straightforward: we need to reorder names according to heights in descending order. Since heights are distinct, sorting by height uniquely determines the order. Immediate approach: pair each name with its height (zip), sort the pairs by height descending, then extract the names. Alternative approaches: sort indices by heights or use a heap, but simple sort is enough given n ≤ 1000. Watch out for preserving the correct pairing between names and heights.

## Refining the problem, round 2 thoughts
- Edge cases: n small (1 or 2), duplicate names allowed but heights are distinct so ordering is well-defined.
- Complexity: sorting gives O(n log n) time and O(n) additional space (for zipped list or index list).
- Implementation choices: zip as (height, name) and sort reverse=True, or zip (name, height) and use key=lambda x: x[1] with reverse=True. Both are fine; using heights first and extracting names is concise.

## Attempted solution(s)
```python
from typing import List

class Solution:
    def sortPeople(self, names: List[str], heights: List[int]) -> List[str]:
        # Pair heights with names, sort by height descending, then extract names.
        pairs = sorted(zip(heights, names), reverse=True)  # sorts by height (first element) desc
        return [name for _, name in pairs]
```
- Notes:
  - Approach: Pair heights with names using zip, sort pairs in descending order by height, extract the names in that order.
  - Time complexity: O(n log n) due to sorting.
  - Space complexity: O(n) for the list of pairs and the output list.
  - Implementation detail: Using (height, name) tuples and reverse=True ensures sorting by height descending; heights are distinct, so no tie-breaking concerns.