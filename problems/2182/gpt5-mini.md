# [Problem 2182: Construct String With Repeat Limit](https://leetcode.com/problems/construct-string-with-repeat-limit/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)
We want the lexicographically largest string possible while never repeating the same character more than repeatLimit times in a row. Lexicographically largest means prefer larger letters (z down to a). A greedy idea: always append the largest available character, up to repeatLimit times. If that character still remains after hitting the limit, we must insert some smaller character to break the run, then return to the larger character if still available. That suggests counting frequencies first and repeatedly picking the current largest available character; when blocked by repeatLimit and still more of that character remains, pick the next largest available single character as a breaker. Repeat until no characters remain or no breaker exists.

A max-heap (priority queue) of (char, count) also fits: pop the largest, append up to repeatLimit, if leftover push it back but only after using a smaller one in between. But because letters are only 26, a simple frequency array and scanning down from 'z' to 'a' is straightforward and fast.

## Refining the problem, round 2 thoughts
- Edge cases: if there is no smaller character available to break a blocked run, we must stop; we cannot use any more of that large character because it would violate the limit.
- Complexity: building counts is O(n). Each append step may require scanning up to 26 letters to find the largest or the next breaker; since alphabet size is constant, complexity is O(n) effectively. Implementing with a heap is also fine but slightly heavier.
- Implementation detail: after appending up to repeatLimit of a character i, if counts[i] > 0 we need to find a j < i with counts[j] > 0. Append exactly one of j (decrement its count), then continue the main loop to try i again.
- Alternative: use heap storing (-char_code, count) to avoid repeated scans; both are acceptable. I'll use the counts array approach for clarity and simplicity.

## Attempted solution(s)
```python
class Solution:
    def repeatLimitedString(self, s: str, repeatLimit: int) -> str:
        # Count frequencies of letters a..z
        counts = [0] * 26
        for ch in s:
            counts[ord(ch) - ord('a')] += 1

        res = []
        while True:
            # find largest available character index i (25 -> 0)
            i = -1
            for idx in range(25, -1, -1):
                if counts[idx] > 0:
                    i = idx
                    break
            if i == -1:
                break  # no characters left

            # append up to repeatLimit of this character
            use = min(repeatLimit, counts[i])
            res.append(chr(ord('a') + i) * use)
            counts[i] -= use

            # if still remaining of this char, need to insert one smaller char as a breaker
            if counts[i] > 0:
                j = -1
                for idx in range(i - 1, -1, -1):
                    if counts[idx] > 0:
                        j = idx
                        break
                if j == -1:
                    # no breaker available, can't append more
                    break
                # append one breaker character
                res.append(chr(ord('a') + j))
                counts[j] -= 1
                # continue loop; we'll try to use the large char i again next iteration
        return "".join(res)
```
- Notes on approach: This is a greedy construction: always try to append the highest letter possible up to the limit, and when blocked by the limit but more of that letter remains, insert the next-highest available single character to break the sequence.
- Time complexity: O(n + 26 * k) in the worst layout of operations where k is number of append-blocks, but since the alphabet size is constant (26) this is effectively O(n). Space complexity: O(n) for the output string plus O(1) extra for counts.
- Important implementation details: We must search for the current largest available character each iteration and, when a run is exhausted by the repeatLimit while leftovers remain, search for the next smaller character to insert one time. If no such smaller character exists, we must stop — further additions would violate the repeat limit.