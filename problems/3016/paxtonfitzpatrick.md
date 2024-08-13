# [Problem 3016: Minimum Number of Pushes to Type Word II](https://leetcode.com/problems/minimum-number-of-pushes-to-type-word-ii/description/?envType=daily-question)

## Initial thoughts (stream-of-consciousness)

- oh this looks fun
- okay we have 8 keys to work with, and we want to minimize the number of pushes to type the given word, which means we want to prioritize letter that we type more often being the first asigned to a key
- okay my immediate idea is:
  - initialize variables `total_presses` to 0 and `key_slot` to 1
  - use a `collections.Counter` to get the count of each letter in `word`, and the `.most_common()` method to get those counts ordered by frequency
  - assign the most commonly used letter to the first slot of key 2, the second to the first slot of key 3, and so on. After assigning the first slot of key 9, start assigning letters to keys' 2nd slots and increment `key_slot` by 1
  - each time a letter is assigned to a key, increment `total_presses` by the number of times it occurs in `word` times `key_slot`
  - when we reach the end of of the `.most_common()` list, return `total_presses`
- I can't think of any edge cases or scenarios that'd break this logic... and also this *seems* to be what's happening in the examples... plus the runtime is $O(n) space complexity is $O(1)$, which is just about the best we could possibly do here... so I'm going to go ahead and implement it.
  - (the `Counter` object takes $O(n)$ space and the sorting required for `.most_common()` takes $O(n \log n)$ with respect to the number of items in it, but in this case that number is guaranteed to always be $\le$ 26, so it's effectively $O(1)$)
  - ah, actually -- now that I think of it, the fact that this container's size is fixed means I don't actually have to use a `Counter` at all, I can just pre-allocate a list of 26 0s and increment the value at each given letter's index as I iterate through the input word. I'll still need to sort the list (in reverse order) just like I would the counter, but this way I avoid the overhead of the `Counter` object itself.

## Refining the problem, round 2 thoughts

## Attempted solution(s)

```python
class Solution:
    def minimumPushes(self, word: str) -> int:
        letter_counts = [0] * 26
        for letter in word:
            # 97 is ord('a')
            letter_counts[ord(letter) - 97] += 1
        letter_counts.sort(reverse=True)
        total_presses = 0
        key_slot = 1
        curr_key = 2
        for count in letter_counts:
            if count == 0:
                return total_presses
            total_presses += count * key_slot
            if curr_key == 9:
                curr_key = 2
                key_slot += 1
            else:
                curr_key += 1
        return total_presses
```

![](https://github.com/user-attachments/assets/15ebd036-fd52-4606-9028-4ebaacc50e31)

- huh... that's an interesting bimodal distribution. Seems like people are using one of two approaches to solve this, but I can't immediately think of a more efficient way than what I did... I guess I'll check the editorial and see
- ah, another heap solution. I really should learn how those work at some point.
