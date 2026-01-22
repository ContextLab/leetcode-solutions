# [Problem 1405: Longest Happy String](https://leetcode.com/problems/longest-happy-string/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We need the longest string using at most a 'a's, b 'b's, c 'c's that never contains "aaa", "bbb", or "ccc". This suggests a greedy strategy: at each step try to append the character with the largest remaining count, unless doing so would make three in a row. If the most frequent character is forbidden by the last two characters, pick the next most frequent. Use a max-structure keyed by remaining counts to always pick the best available choice. Since there are only three characters, a small heap or manual comparisons suffice.

## Refining the problem, round 2 thoughts
- Edge cases: when the most frequent character is currently forbidden and there is no other character left -> stop.
- If the most frequent char is allowed, we might consider adding it twice in a row when it has a lot more count than others, but adding step-by-step with greedy (choosing the largest allowed each time) naturally allows sequences like "aa" but prevents "aaa" by the check.
- Using a max-heap (with negative counts) makes this straightforward and concise. Because the heap size is at most 3, heap operations are effectively constant-time, and the overall complexity is linear in the total characters placed.
- Alternative solutions: repeatedly choose top two and append patterns like "aab" etc., but the heap approach is simpler and robust.
- Complexity: O(n log k) where n = a + b + c and k <= 3 (so effectively O(n)). Space: O(1) extra besides output.

## Attempted solution(s)
```python
import heapq

def longestDiverseString(a: int, b: int, c: int) -> str:
    # Max-heap using negative counts
    heap = []
    for count, ch in ((a, 'a'), (b, 'b'), (c, 'c')):
        if count > 0:
            heapq.heappush(heap, (-count, ch))

    res = []
    while heap:
        cnt, ch = heapq.heappop(heap)  # cnt is negative
        # If last two characters are same as ch, we cannot append ch now
        if len(res) >= 2 and res[-1] == res[-2] == ch:
            if not heap:
                # No alternative character to use -> stop building
                break
            cnt2, ch2 = heapq.heappop(heap)
            res.append(ch2)
            # Used one of ch2, increment its negative count
            cnt2 += 1
            if cnt2 < 0:
                heapq.heappush(heap, (cnt2, ch2))
            # push back the original top choice for future consideration
            heapq.heappush(heap, (cnt, ch))
        else:
            # We can use ch
            res.append(ch)
            cnt += 1  # used one, so negative count moves toward zero
            if cnt < 0:
                heapq.heappush(heap, (cnt, ch))

    return ''.join(res)


# Example usage:
if __name__ == "__main__":
    print(longestDiverseString(1, 1, 7))  # e.g., "ccaccbcc" or similar valid answer
    print(longestDiverseString(7, 1, 0))  # "aabaa"
```
- Notes on approach: Use a max-heap keyed by remaining counts. Always try to append the character with the largest remaining count unless that would form three identical characters in a row; in that case use the next best character. Reinsert characters with remaining counts back into the heap after using one.
- Time complexity: O(n log k) where n = a + b + c and k <= 3 (so effectively O(n)).
- Space complexity: O(1) extra (heap of up to 3 elements) plus O(n) for the output string.